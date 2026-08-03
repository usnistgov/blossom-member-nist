#!/usr/bin/env bash

###############################################################
# This script packages auto_assessment lambda into zip-file
###############################################################

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# If for some reason the file doesn't execute - remember to 
# run the execution granting command for the file:
#           chmod +x pack_aa.sh
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
set -x ## Debug the commands in verbose form

_lambda_dest_stem_=".aa_lambda"

## _lambda_zip_timed_name_="../${_lambda_dest_stem_}-$(date +"%Y-%m-%d@%H-%M-%S").zip"
_lambda_older_="$_lambda_dest_stem_"
_lambda_latest_="${_lambda_dest_stem_}(latest).zip"
# Step 1: ===============================================================
# Clean up previous deployments and create new directory
echo "Step 1: Cleaning ./.package directory and all it's sub-directories"
rm -rf .package*

echo "Latest ./${_lambda_latest_}"
rm -rf "./${_lambda_latest_}"

echo "Older: ./${_lambda_older_}"*.zip
rm -rf "./${_lambda_older_}"*.zip

echo "Step 1: DONE!!! Cleaning ./.package directory and all it's sub-directories"
