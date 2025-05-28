#!/usr/bin/env bash
# Wrapper for Terraform that checks for valid credentials

set -Eeuo pipefail

msg() {
  echo >&2 -e "${1-}"
}


if ! [ -x "$(command -v terraform)" ]; then
  msg 'Error: Python (terraform) is not in the PATH, is it installed?'
  exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

# AWS_PROFILE="saml" terraform "$@"
# echo "  ter.sh:  AWS_PROFILE=$AWS_PROFILE"
# msg "  ter.sh:  BASH_SOURCE[0]=${BASH_SOURCE[0]}"
# msg "  ter.sh:  SCRIPT_DIR=${SCRIPT_DIR}"
# msg "  ter.sh:  COMMAND=$@"

(
    cd $SCRIPT_DIR

    ./../util/aws_okta_test.sh

    AWS_PROFILE="saml" terraform "$@"
)
