## The lambdas code has the code for 

- #### `s3-lambda` that needs to be deployed to the `blossom-s3-watcher` Lambda body
- #### `ec2-lambda` that needs to be deployed to the `blossom-ec2-assessment` Lambda body


## The Lambda `blossom-s3-watcher` is the part of the GitHub integration for user management
#### The configuration of lambda must have the following triggers on S3 Bucket observed:
#### 1. Event types: s3:ObjectCreated:*
#### 2. s3:ObjectRemoved:Delete 