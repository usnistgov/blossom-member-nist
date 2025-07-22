SHELL:=/bin/bash
AWS_PROFILE:=saml
TERRAFORM_CMD:=./tok.sh
# The relative PATH to the lambda function code (Currently local)
LAMBDA_DIR:=./lambda

# Profile-specific settings
CONNECTION_PROFILES_DIR:=./connection_profiles
CONNECTION_PROFILE:=./connection_profiles/$(shell $(TERRAFORM_CMD) workspace show).json
ENVIRONMENT_CONFIGURATION:=./configurations/$(shell $(TERRAFORM_CMD) workspace show).json
# Profile-specific info
$(info CONNECTION_PROFILES_DIR: $(CONNECTION_PROFILES_DIR))
$(info ENVIRONMENT_CONFIGURATION: $(ENVIRONMENT_CONFIGURATION))
$(info CONNECTION_PROFILE: $(CONNECTION_PROFILE))

###
### The path to the Particular DashBoard you mean to build and deploy to your infrastructure
###
### !!!Warning!!! 
### Path values are space sensitive! 
### Spaces in the beginning or end of path can break script
###
### Generic Dashboard
DASHBOARD_DIR:= ../../blossom-dashboard
### ~/github/blossom-dashboard
### Particular ORG-Member Dashboard, preferably forked form blossom-dashboard [This one is NIST]
# DASHBOARD_DIR:=../../blossom-dashboard-nist

# Use this makefile to ensure the lambda and dashboard have been built before provisioning

.PHONY: help
# Run "make" or "make help" to get a list of user targets
# Adapted from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | awk 'BEGIN { \
	 FS = ":.*?## "; \
	 printf "\033[1m%-30s\033[0m %s\n", "TARGET", "DESCRIPTION" \
	} \
	{ printf "\033[32m%-30s\033[0m %s\n", $$1, $$2 }'

.PHONY: init
# Initializes Terraform environment and updates the list of providers required for configuration
# Do not .gitignore the .terraform.lock.hcl file, but pay attention if it changes unexpectedly !!!! 
# See https://stackoverflow.com/questions/67963719/should-terraform-lock-hcl-be-included-in-the-gitignore-file
init: ## Init terraform  configuration
	$(TERRAFORM_CMD) init

.PHONY: plan
plan: build ## Preview the Terraform plan
	$(TERRAFORM_CMD) plan

.PHONY: apply
apply: build ## Apply the Terraform plan
	$(TERRAFORM_CMD) apply

.PHONY: refresh
refresh: ## Refresh Terraform outputs
	@echo Refreshing terraform outputs...
	$(TERRAFORM_CMD) refresh

.PHONY: build
build: build-lambda build-dashboard connection-profile ## Build all dependencies

.PHONY: clean
clean: clean-dashboard clean-lambda clean-connection-profile ## Clean dependencies of all artifacts

# Dashboard

DASHBOARD_DEVENV_FILE:=$(DASHBOARD_DIR)/.env.development
DASHBOARD_PRODENV_FILE:=$(DASHBOARD_DIR)/.env.prod

.PHONY: build-dashboard
build-dashboard: $(DASHBOARD_PRODENV_FILE) ## Build the dashboard
	@echo "🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟n"
	@echo "🌟 🚀  Building the dashboard project with following configuration:"
	@echo "🌟	aws_profile = $(AWS_PROFILE)"
	@echo "🌟	dashboard_at = $(DASHBOARD_DIR)"
	@echo "🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟"
	$(MAKE) -C "$(DASHBOARD_DIR)" build AWS_PROFILE="$(AWS_PROFILE)"

.PHONY: environment-dashboard
environment-dashboard: $(DASHBOARD_DEVENV_FILE) $(DASHBOARD_PRODENV_FILE) ## Produce dashboard environment files
$(DASHBOARD_DEVENV_FILE):
	$(TERRAFORM_CMD) output -raw vite_dev_env > "$(DASHBOARD_DEVENV_FILE)"
$(DASHBOARD_PRODENV_FILE):
	$(TERRAFORM_CMD) output -raw vite_prod_env > "$(DASHBOARD_PRODENV_FILE)"



.PHONY: clean-dashboard
clean-dashboard: ## Clean dashboard build artifacts and environment files
	$(MAKE) -C "$(DASHBOARD_DIR)" clean
	rm -f "$(DASHBOARD_DEVENV_FILE)"
	rm -f "$(DASHBOARD_PRODENV_FILE)"

# Lambda

.PHONY: build-lambda
build-lambda: ## Build the lambda source
	@echo "🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟"
	@echo "🌟 🚀  Starting Building the lambda project with following configuration:"
	@echo "🌟	aws_profile = $(AWS_PROFILE)"
	@echo "🌟	lambda_at = $(LAMBDA_DIR)"
	@echo "🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟"
	$(MAKE) -C "$(LAMBDA_DIR)" build AWS_PROFILE="$(AWS_PROFILE)"

.PHONY: clean-lambda
clean-lambda: ## Clean lambda build artifacts
## @echo "Beginning Task: [clean-lambda]"
## @echo "LAMBDA_DIR=$(LAMBDA_DIR)"
## @echo "Executing Task: $(LAMBDA_DIR)/Makefile clean"
	$(MAKE) -C "$(LAMBDA_DIR)" clean


.PHONY: connection-profile
connection-profile:  ## Generate the connection profile for the given workspace
	## $(CONNECTION_PROFILE)
	## Beginning Building Connection Profile  $(CONNECTION_PROFILE)
	@echo "🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟"
	@echo "🌟 🚀 	Starting gen-config-profile with the following data:"
	@echo "🌟 🚀	Making DIR:	$(CONNECTION_PROFILES_DIR) "
	@echo "🌟 🚀	For FILE:	$(CONNECTION_PROFILE) "
	@echo "🌟 🚀	From ENV:	$(ENVIRONMENT_CONFIGURATION) "
	@echo "🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟"
	$(shell mkdir -p $(CONNECTION_PROFILES_DIR))
	$(shell set pipefail; ../util/gen-connection-profile.sh \
		--member_id "$$(jq -r .member_id $(ENVIRONMENT_CONFIGURATION))" \
		--network_id "$$(jq -r .network_id $(ENVIRONMENT_CONFIGURATION))" \
		--channels "$$(jq -r .all_channels $(ENVIRONMENT_CONFIGURATION))" \
		--tlsCaCertPath "./managedblockchain-tls-chain.pem" \
	> $(CONNECTION_PROFILE))

##
##../util/gen-connection-profile.sh \
##		--member_id "$(shell jq -r .member_id $(ENVIRONMENT_CONFIGURATION))" \
##		--network_id "$(shell jq -r .network_id $(ENVIRONMENT_CONFIGURATION))" \
##		--channels "$(shell jq -r .all_channels $(ENVIRONMENT_CONFIGURATION))" \
##		--tlsCaCertPath "./managedblockchain-tls-chain.pem" \
##	> $(CONNECTION_PROFILE)
##

.PHONY: clean-connection-profile
clean-connection-profile: ## Clean the connection profile
	rm -f $(CONNECTION_PROFILE)