package pdp

import (
	"github.com/PM-Master/policy-machine-go/pip"
	"github.com/PM-Master/policy-machine-go/pip/memory"
	"github.com/stretchr/testify/require"
	"github.com/usnistgov/blossom/chaincode/mocks"
	"github.com/usnistgov/blossom/chaincode/model"
	"github.com/usnistgov/blossom/chaincode/ngac/operations"
	assetpap "github.com/usnistgov/blossom/chaincode/ngac/pap/asset"
	"github.com/usnistgov/blossom/chaincode/ngac/pap/policy"
	"testing"
)

func TestOnboardLicense(t *testing.T) {
	mock := mocks.New()

	err := initLicenseTestGraph(t, mock)
	require.NoError(t, err)

	asset := &model.Asset{
		ID:                "",
		Name:              "",
		TotalAmount:       0,
		Available:         0,
		Cost:              0,
		OnboardingDate:    "",
		Expiration:        "",
		Licenses:          make([]string, 0),
		AvailableLicenses: make([]string, 0),
		CheckedOut:        make(map[string]map[string]model.DateTime),
	}

	decider := NewAssetDecider()

	t.Run("test super", func(t *testing.T) {
		mock.SetUser(mocks.Super)

		err = decider.OnboardAsset(mock.Stub, asset)
		require.NoError(t, err)
	})

	t.Run("test a1 system owner", func(t *testing.T) {
		mock.SetUser(mocks.A1SystemOwner)

		err = decider.OnboardAsset(mock.Stub, asset)
		require.Error(t, err)
	})
}

func TestOffboardLicense(t *testing.T) {
	mock := mocks.New()

	err := initLicenseTestGraph(t, mock)
	require.NoError(t, err)

	decider := NewAssetDecider()
	require.NoError(t, err)

	t.Run("test super", func(t *testing.T) {
		mock.SetUser(mocks.Super)

		err = decider.OffboardAsset(mock.Stub, "test-asset-id")
		require.NoError(t, err)
	})

	t.Run("test a1 system owner", func(t *testing.T) {
		mock.SetUser(mocks.A1SystemOwner)

		err = decider.OffboardAsset(mock.Stub, "test-asset-id")
		require.Error(t, err)
	})
}

func TestCheckoutLicense(t *testing.T) {
	mock := mocks.New()

	t.Run("test checkout active", func(t *testing.T) {
		// initialize the test graph with an onboarded license
		err := initLicenseTestGraph(t, mock)
		require.NoError(t, err)

		// request account
		account := &model.Account{
			Name:  "A1",
			ATO:   "ato",
			MSPID: "A1MSP",
			Users: model.Users{
				SystemOwner:           "a1_system_owner",
				SystemAdministrator:   "a1_system_admin",
				AcquisitionSpecialist: "a1_acq_spec",
			},
			Status: "status",
			Assets: make(map[string]map[string]model.DateTime),
		}

		mock.SetUser(mocks.A1SystemOwner)

		accountDecider := NewAccountDecider()
		err = accountDecider.RequestAccount(mock.Stub, account)
		require.NoError(t, err)

		mock.SetGraphState(accountDecider.pap.Graph())

		// approve account
		mock.SetUser(mocks.Super)
		accountDecider = NewAccountDecider()
		err = accountDecider.UpdateAccountStatus(mock.Stub, account.Name, model.Approved)
		require.NoError(t, err)

		mock.SetGraphState(accountDecider.pap.Graph())

		mock.SetUser(mocks.A1SystemAdmin)
		licenseDecider := NewAssetDecider()
		err = licenseDecider.Checkout(mock.Stub, "A1", "test-asset-id",
			map[string]model.DateTime{"1": ""})
		require.NoError(t, err)
	})

	t.Run("test checkout inactive", func(t *testing.T) {
		// initialize the test graph with an onboarded license
		err := initLicenseTestGraph(t, mock)
		require.NoError(t, err)

		// request account
		account := &model.Account{
			Name:  "A1",
			ATO:   "ato",
			MSPID: "A1MSP",
			Users: model.Users{
				SystemOwner:           "a1_system_owner",
				SystemAdministrator:   "a1_system_admin",
				AcquisitionSpecialist: "a1_acq_spec",
			},
			Status: "status",
			Assets: make(map[string]map[string]model.DateTime),
		}

		err = mock.SetUser(mocks.A1SystemOwner)
		require.NoError(t, err)

		accountDecider := NewAccountDecider()
		err = accountDecider.RequestAccount(mock.Stub, account)
		require.NoError(t, err)

		mock.SetGraphState(accountDecider.pap.Graph())

		// do not approve account

		// checkout license as pending
		mock.SetUser(mocks.A1SystemAdmin)
		licenseDecider := NewAssetDecider()
		err = licenseDecider.Checkout(mock.Stub, "A1", "test-asset-id",
			map[string]model.DateTime{"1": ""})
		require.Error(t, err)
	})
}

// initialize a test graph to be used by test methods
func initLicenseTestGraph(t *testing.T, mock mocks.Mock) error {
	// create a new ngac graph and configure it using the blossom policy
	graph := memory.NewGraph()
	err := policy.Configure(graph)
	require.NoError(t, err)

	// set the ngac graph as the result of get state
	// later when OnboardAsset is called, this graph will be used to determine if
	// the super has permission to onboard a license
	mock.SetGraphState(graph)

	// set up the mock identity as the super
	mock.SetUser(mocks.Super)

	// create a test license
	asset := &model.Asset{
		ID:                "test-asset-id",
		Name:              "test-asset",
		TotalAmount:       5,
		Available:         5,
		Cost:              20,
		OnboardingDate:    "2021-5-12",
		Expiration:        "2026-5-12",
		Licenses:          []string{"1", "2", "3", "4", "5"},
		AvailableLicenses: []string{"1", "2", "3", "4", "5"},
		CheckedOut:        make(map[string]map[string]model.DateTime),
	}

	// onboard the license as the super
	licenseDecider := NewAssetDecider()
	err = licenseDecider.OnboardAsset(mock.Stub, asset)
	require.NoError(t, err)

	// re marshal the graph bytes using the PAP's graph
	// this will have the graph that includes the onboarded license
	// this is the graph the tests will operate on
	mock.SetGraphState(licenseDecider.pap.Graph())
	return nil
}

func TestFilterLicense(t *testing.T) {
	graph := memory.NewGraph()
	pcNode, err := graph.CreateNode("pc1", pip.PolicyClass, nil)
	require.NoError(t, err)
	oa1, err := graph.CreateNode("oa1", pip.ObjectAttribute, nil)
	require.NoError(t, err)
	oa2, err := graph.CreateNode("oa2", pip.ObjectAttribute, nil)
	require.NoError(t, err)
	l1, err := graph.CreateNode(assetpap.ObjectAttribute("test-asset-1"), pip.ObjectAttribute, nil)
	require.NoError(t, err)
	l2, err := graph.CreateNode(assetpap.ObjectAttribute("test-asset-2"), pip.ObjectAttribute, nil)
	require.NoError(t, err)
	err = graph.Assign(oa1.Name, pcNode.Name)
	require.NoError(t, err)
	err = graph.Assign(oa2.Name, pcNode.Name)
	require.NoError(t, err)
	err = graph.Assign(l1.Name, oa1.Name)
	require.NoError(t, err)
	err = graph.Assign(l2.Name, oa2.Name)
	require.NoError(t, err)

	ua1, err := graph.CreateNode("ua1", pip.UserAttribute, nil)
	require.NoError(t, err)
	u1, err := graph.CreateNode("super:BlossomMSP", pip.User, nil)
	require.NoError(t, err)
	err = graph.Assign(u1.Name, ua1.Name)
	require.NoError(t, err)
	err = graph.Assign(ua1.Name, pcNode.Name)
	require.NoError(t, err)

	err = graph.Associate("ua1", "oa1", pip.ToOps(operations.ViewAsset))
	require.NoError(t, err)
	err = graph.Associate("ua1", "oa2", pip.ToOps(operations.ViewAsset, operations.ViewAllLicenses,
		operations.ViewAvailableLicenses, operations.ViewCheckedOut))
	require.NoError(t, err)

	testTime := model.DateTime("01-01-2000")
	assets := []*model.Asset{
		{
			ID:                "test-asset-1",
			Name:              "test-asset-1",
			TotalAmount:       5,
			Available:         4,
			Cost:              99,
			OnboardingDate:    testTime,
			Expiration:        testTime,
			Licenses:          []string{"1", "2", "3", "4", "5"},
			AvailableLicenses: []string{"2", "3", "4", "5"},
			CheckedOut: map[string]map[string]model.DateTime{
				"account1": {"test-asset-1": testTime},
			},
		},
		{
			ID:                "test-asset-2",
			Name:              "test-asset-2",
			TotalAmount:       5,
			Available:         4,
			Cost:              99,
			OnboardingDate:    "",
			Expiration:        "",
			Licenses:          []string{"1", "2", "3", "4", "5"},
			AvailableLicenses: []string{"2", "3", "4", "5"},
			CheckedOut: map[string]map[string]model.DateTime{
				"account1": {"test-asset-2": testTime},
			},
		},
	}

	mock := mocks.New()

	mock.SetGraphState(graph)
	mock.SetUser(mocks.Super)

	assets, err = NewAssetDecider().FilterAssets(mock.Stub, assets)
	require.NoError(t, err)
	require.Equal(t, 2, len(assets))

	license := assets[0]
	require.Equal(t, "test-asset-1", license.ID)
	require.Equal(t, "test-asset-1", license.Name)
	require.Equal(t, 5, license.TotalAmount)
	require.Equal(t, 4, license.Available)
	require.Equal(t, float64(99), license.Cost)
	require.Equal(t, []string{}, license.Licenses)
	require.Equal(t, []string{}, license.AvailableLicenses)
	require.Equal(t, map[string]map[string]model.DateTime{}, license.CheckedOut)

	license = assets[1]
	require.Equal(t, "test-asset-2", license.ID)
	require.Equal(t, "test-asset-2", license.Name)
	require.Equal(t, 5, license.TotalAmount)
	require.Equal(t, 4, license.Available)
	require.Equal(t, float64(99), license.Cost)
	require.Equal(t, []string{"1", "2", "3", "4", "5"}, license.Licenses)
	require.Equal(t, []string{"2", "3", "4", "5"}, license.AvailableLicenses)
	require.Equal(t, map[string]map[string]model.DateTime{
		"account1": {"test-asset-2": testTime},
	}, license.CheckedOut)
}
