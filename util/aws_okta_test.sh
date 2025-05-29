#!/usr/bin/env bash

# Tests AWS CLI for valid credentials and reauthenticates if credentials are
# invalid or expired.
# This script also manages the creation of a Python virtual environment.
echo "In $(basename ${BASH_SOURCE[0]}) script in $( dirname ${BASH_SOURCE[0]} ) dir"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
source "${SCRIPT_DIR}/aws_okta_util.sh"
echo "  1: Verifying that Python/Python3 is installed in PATH"
# Verify that Python3 is installed
if ! [ -x "$(command -v python3)" ]; then
  msg 'Error: Python (python3) is not in the PATH, is it installed?'
  exit 1
fi

echo "  2: Verifying that AWS-CLI is installed and is in PATH"
# Verify that AWS-CLI is installed
if ! [ -x "$(command -v aws)" ]; then
  msg 'Error: AWS-CLI (aws) is not in the PATH, is it installed?'
  exit 1
fi

echo "  3: Verifying that OKTA-AWS-CLI is installed and is in PATH"
# Verify that OKTA-AWS-CLI is installed
if ! [ -x "$(command -v okta-aws-cli)" ]; then
  msg 'Error: OKTA-AWS-CLI (okta-aws-cli) is not in the PATH, is it installed?'
  msg 'On MacOS use command:'
  msg '     brew install okta-aws-cli)'
  exit 1
fi

echo "  4: Checking if there is a currently active logged-in user"
if aws sts get-caller-identity --profile=$AWS_PROFILE > /dev/null 2>&1; then
    # Credentials are valid, no need to continue
    exit 0
fi

echo "  5: Setting everything for the python virtual environment"
# Reuse function from ./util/util-common.bash
test_setup_venv

echo "  6: Show environment context"
show_env_info "File: $0 at Line: $LINENO"
echo "$SCRIPT_DIR=${SCRIPT_DIR}"
# Run shell subprocess
(
  echo "  7: Activate virtual environment and run login "
  cd "$SCRIPT_DIR"

  source ./venv/bin/activate

  python3 aws_okta_auth.py
)
