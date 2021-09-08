package pdp

import (
	"github.com/PM-Master/policy-machine-go/pip"
	"github.com/PM-Master/policy-machine-go/pip/memory"
	"github.com/stretchr/testify/require"
	"github.com/usnistgov/blossom/chaincode/mocks"
	"github.com/usnistgov/blossom/chaincode/model"
	"github.com/usnistgov/blossom/chaincode/ngac/operations"
	"github.com/usnistgov/blossom/chaincode/ngac/pap/policy"
	swidpap "github.com/usnistgov/blossom/chaincode/ngac/pap/swid"
	"testing"
)

func TestReportSwID(t *testing.T) {
	mock := mocks.New()

	initSwidTestGraph(t, mock)

	// set user as super
	err := mock.SetUser(mocks.Super)
	require.NoError(t, err)

	// update account status
	accountDecider := NewAccountDecider()
	err = accountDecider.UpdateAccountStatus(mock.Stub, "A1", model.Approved)
	require.NoError(t, err)

	// update graph state
	mock.SetGraphState(accountDecider.pap.Graph())

	// change user to a1 sys sdmin
	err = mock.SetUser(mocks.A1SystemAdmin)
	require.NoError(t, err)

	licenseDecider := NewAssetDecider()
	err = licenseDecider.Checkout(mock.Stub, "A1", "test-asset-id",
		map[string]model.DateTime{"1": ""})
	require.NoError(t, err)

	mock.SetGraphState(licenseDecider.pap.Graph())

	// report swid
	swidDecider := NewSwIDDecider()
	swid := &model.SwID{
		PrimaryTag:      "pt1",
		XML:             "xml",
		Asset:           "test-asset-id",
		License:         "1",
		LeaseExpiration: "",
	}
	err = swidDecider.ReportSwID(mock.Stub, swid, "A1")
	require.NoError(t, err)

	// report swid on license key that the user does not have access to
	swid = &model.SwID{
		PrimaryTag:      "pt1",
		XML:             "xml",
		Asset:           "test-asset-id",
		License:         "2",
		LeaseExpiration: "",
	}
	err = swidDecider.ReportSwID(mock.Stub, swid, "A1")
	require.Error(t, err)
}

func initSwidTestGraph(t *testing.T, mock mocks.Mock) {
	graph := memory.NewGraph()

	// configure the policy
	err := policy.Configure(graph)
	require.NoError(t, err)

	// add an account
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

	mock.SetGraphState(graph)

	// add account as the a1 system owner
	err = mock.SetUser(mocks.A1SystemOwner)
	require.NoError(t, err)

	accountDecider := NewAccountDecider()
	err = accountDecider.RequestAccount(mock.Stub, account)
	require.NoError(t, err)

	mock.SetGraphState(accountDecider.pap.Graph())

	// set up the mock identity as the org1 admin
	err = mock.SetUser(mocks.Super)
	require.NoError(t, err)

	// create a test asset
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

	licenseDecider := NewAssetDecider()
	err = licenseDecider.OnboardAsset(mock.Stub, asset)
	require.NoError(t, err)

	mock.SetGraphState(licenseDecider.pap.Graph())
}

func TestFilterSwID(t *testing.T) {
	graph := memory.NewGraph()
	pcNode, err := graph.CreateNode("pc1", pip.PolicyClass, nil)
	require.NoError(t, err)
	oa1, err := graph.CreateNode("oa1", pip.ObjectAttribute, nil)
	require.NoError(t, err)
	oa2, err := graph.CreateNode("oa2", pip.ObjectAttribute, nil)
	require.NoError(t, err)
	swid1, err := graph.CreateNode(swidpap.ObjectAttributeName("swid1"), pip.ObjectAttribute, nil)
	require.NoError(t, err)
	swid2, err := graph.CreateNode(swidpap.ObjectAttributeName("swid2"), pip.ObjectAttribute, nil)
	require.NoError(t, err)
	err = graph.Assign(oa1.Name, pcNode.Name)
	require.NoError(t, err)
	err = graph.Assign(oa2.Name, pcNode.Name)
	require.NoError(t, err)
	err = graph.Assign(swid1.Name, oa1.Name)
	require.NoError(t, err)
	err = graph.Assign(swid2.Name, oa2.Name)
	require.NoError(t, err)

	ua1, err := graph.CreateNode("ua1", pip.UserAttribute, nil)
	require.NoError(t, err)
	u1, err := graph.CreateNode("super:BlossomMSP", pip.User, nil)
	require.NoError(t, err)
	err = graph.Assign(u1.Name, ua1.Name)
	require.NoError(t, err)
	err = graph.Assign(ua1.Name, pcNode.Name)
	require.NoError(t, err)

	err = graph.Associate("ua1", "oa1", pip.ToOps(operations.ViewSwID))
	require.NoError(t, err)

	swids := []*model.SwID{
		{PrimaryTag: "swid1"},
		{PrimaryTag: "swid2"},
	}

	mock := mocks.New()

	mock.SetGraphState(graph)
	err = mock.SetUser(mocks.Super)
	require.NoError(t, err)

	swids, err = NewSwIDDecider().FilterSwIDs(mock.Stub, swids)
	require.NoError(t, err)
	require.Equal(t, 1, len(swids))
}
