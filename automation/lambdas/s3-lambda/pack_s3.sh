#!/usr/bin/env bash

###############################################################
# This script packages auto_assessment lambda into zip-file
###############################################################

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# If for some reason the file doesn't execute - remember to 
# run the execution granting command for the file:
#           chmod +x pack_aa.sh
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
_lambda_source_="./blossom-s3-watcher.py"
_lambda_dest_stem_=".s3_lambda"

_lambda_zip_timed_name_="../${_lambda_dest_stem_}-$(date +"%Y-%m-%d@%H-%M-%S").zip"
_lambda_latest_="${_lambda_dest_stem_}(latest).zip"
# Step 1: ===============================================================
# Clean up previous deployments and create new directory
echo "Step 1: Cleaning ./.package directory and all it's sub-directories"
rm -rf ./.package/*
rm -rf .package
rm -rf "./${_lambda_latest_}"
mkdir ./.package
echo "Step 1: DONE!!! Cleaning ./.package directory and all it's sub-directories"


# Step 2: ===============================================================
### Copy the lambda function main body 
echo "Step 2: Copying the lambda body into ./.package/"
cp -f $_lambda_source_  ./.package/
echo "Step 2: DONE!!! Copying the lambda body into ./.package/"
# OPTIONAL, but !!!!!! IMPORTANT !!!!!! 
# [Repeat cp-command for every component Python-file if/as needed]


# Step 3: ===============================================================
### Install dependencies (make sure you maintain the dependencies as well)
### !!! Depending on your Python environment setup you may need to:

### Option #1: Use pip3 to install requirements
# pip3  install -r ./requirements.txt --target ./.package  

### Option #2: [fastest if uv is installed] Use uv pip to install requirements
echo "Step 3: UV-Installing python dependencies into ./.package/"
uv pip install -r ./requirements.txt --target ./.package
echo "Step 3: DONE!!! UV-Installing python dependencies into ./.package/"

### Option #3: [slowest] Use python -m pip to install requirements
# python -m pip install -r ./requirements.txt --target ./.package


# Step 4: ===============================================================
### Get into the Package directory and zip the package up
### Package the resulting flat Python into ZIP
echo "Step 4: Packaging the ${_lambda_zip_timed_name_}"
cd .package
zip -r ${_lambda_zip_timed_name_} .
echo "Step 4: DONE!!! Packaging the  ${_lambda_zip_timed_name_}"


# Step 5: ===============================================================
### Get into the Package directory and zip the package up
### Package the resulting flat Python into ZIP
echo "Step 5: DONE!!! Packaging the  ${_lambda_zip_timed_name_}"
cp ${_lambda_zip_timed_name_} "../${_lambda_latest_}"
cd ..
echo "Step 5: DONE!!! Packaging the  ${_lambda_zip_timed_name_} and copying to into "../${_lambda_latest_}""