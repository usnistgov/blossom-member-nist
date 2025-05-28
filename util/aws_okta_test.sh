#!/usr/bin/env bash

# Tests AWS CLI for valid credentials and reauthenticates if credentials are
# invalid or expired.
# This script also manages the creation of a Python virtual environment.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
source "${SCRIPT_DIR}/aws_okta_util.sh"

# Verify that Python3 is installed
if ! [ -x "$(command -v python3)" ]; then
  msg 'Error: Python (python3) is not in the PATH, is it installed?'
  exit 1
fi

# Verify that AWS-CLI is installed
if ! [ -x "$(command -v aws)" ]; then
  msg 'Error: AWS-CLI (aws) is not in the PATH, is it installed?'
  exit 1
fi

# Verify that OKTA-AWS-CLI is installed
if ! [ -x "$(command -v okta-aws-cli)" ]; then
  msg 'Error: OKTA-AWS-CLI (okta-aws-cli) is not in the PATH, is it installed?'
  msg 'On MacOS use command:'
  msg '     brew install okta-aws-cli)'
  exit 1
fi

if aws sts get-caller-identity --profile=$AWS_PROFILE > /dev/null 2>&1; then
    # Credentials are valid, no need to continue
    exit 0
fi

# Reuse function from ./util/util-common.bash
test_setup_venv

show_env_info "File: $0 at Line: $LINENO"

# Run shell subprocess
(
  cd "$SCRIPT_DIR"

  source ./venv/bin/activate

  msg "Proceeding to OKTA-based authentication:"
  python3 aws_okta_auth.py
)
