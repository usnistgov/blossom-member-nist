# Design Information
for automated assessment lambda of the blossom system

- The communication of the dashboard is relying on the following: 
  - dashboard hosted by S3 bucket, 
  - lambda communicates leveraging SSM-Agent, 
  - AMB VPC and Member EC2-peer setup,
  - AMB chaincode EC2-peer


### How to verify ssm-agent EC2 Setup:
- Verify AWS ssm-agent is installed and running using the following command inside EC2 instance:
```
sudo systemctl status amazon-ssm-agent
```
- If it doesn't work - try starting the service:
```
sudo systemctl start amazon-ssm-agent
```
- For  guidance on more complicated issues refer to:
  - [AWS Session Manager (SSM) with EC2 Instances](https://www.cloudyali.io/blogs/the-power-of-aws-session-manager-ssm-with-ec2-instances) from cloud-yali
  - More high-level [AWS guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) 
  - More [technical AWS-guide](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/connect-to-an-amazon-ec2-instance-by-using-session-manager.html)
  - Step-by-step [guide from Medium](https://medium.com/@dorianferguson/use-ssm-instead-of-ssh-to-access-ec2-instances-c0d2fe1be0d5)



### cURL-Testing of Lambda
```

curl \
-X POST "https://pix35w1qac.execute-api.us-east-1.amazonaws.com/dev/blossom-ec2-assessment/transaction" \
-H 'Content-Type: application/json' \
-H "Cookie": "access_token=---token---" \
-d {"type":"Assess"}
```
```
-H 'Authorization: Bearer ---token---' \
```

### Prepare AWS lambda deployment ZIP-file
