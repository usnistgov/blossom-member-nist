AA_LAMBDA_DIR:=$(DASHBOARD_DIR)/automation/lambdas/ec2-lambda


.PHONY: help
# Run "make" or "make help" to get a list of user targets
# Adapted from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | awk 'BEGIN { \
	 FS = ":.*?## "; \
	 printf "\033[1m%-30s\033[0m %s\n", "TARGET", "DESCRIPTION" \
	} \
	{ printf "\033[32m%-30s\033[0m %s\n", $$1, $$2 }'


BUILD_PACKAGE_SCRIPT_OUTPUT:=$(shell ./pack_aa.sh)
.PHONY: build
build: ## Build the lambda source	
	@echo "$(BUILD_PACKAGE_SCRIPT_OUTPUT)" | sed 's/ / /g'


CLEAN_OLD_PACKAGES_OUTPUT:=$(shell ./clean_aa.sh)
.PHONY: clean
clean: # Clean up previous package versions and build dir
