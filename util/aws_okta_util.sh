set -Eeuo pipefail

# The AWS profile section to which the OKTA credentials in file
# ~/.aws/credentials are written after OKTA Auth
export AWS_PROFILE="saml"

# Reusable Message function
msg() {
  echo >&2 -e "${1-}"
}

# Display AWS and OKTA setting from ENV
show_env_info(){
  echo
if [ $# -gt 0 ]; then
  msg "Selected Environment Variables [AWS, OKTA,] from $1:"
else
  msg "Selected Environment Variables [AWS, OKTA,]:"
fi
env | grep AWS
env | grep OKTA

}

function stack_trace() {
  local -a stack=("Stack trace:")
  local stack_size=${#FUNCNAME[@]}
  local -i i

  for ((i = 1; i < stack_size; i++)); do
    local func="${FUNCNAME[$i]:-(top level)}"
    local line="${BASH_LINENO[$((i - 1))]}"
    local src="${BASH_SOURCE[$i]:-(no file)}"
    stack+=(" ($i) $func $src:$line")
  done

  (IFS=$'\n'; echo "${stack[*]}")
}

# This will fail if SCRIPT_DIR
test_setup_venv() {
  local SOURCE_DIR
  SOURCE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
  (
    cd "$SOURCE_DIR"

    if [ ! -d "$SOURCE_DIR"/venv ] ; then
        msg "Setting up the Python virtual environment"

        if ! [ -x "$(command -v python3)" ]; then
          msg 'Error: Python (python3) is not in the PATH, is it installed?'
          exit 1
        fi

        python3 -m venv venv
        source ./venv/bin/activate
        python3 -m pip install -r ./requirements.txt
        msg ""
    fi
  )
}