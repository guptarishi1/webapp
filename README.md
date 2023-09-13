# webapp
I have build an GET api using Flask. 


Git Commands to clone the repositories:
-  git clone ssh-key   (Organization Repo)

To host the API:
Command to run the python file to host the API in local server:

```code
python GET_API.py
```

Test the below endpoints:

```code
http://127.0.0.1:5000/healthz
```

Built CI pipline and we can check workflow in actions.

Basic auth is implemented in GET and PUT API's-  


Without auth POST API is implemented:
- Encrypted password with Bcrypt with salt

username should be unique and http response is managed for this as well.
If user try to retrieve more impormation than the http response is also managed. 

http responses are managed like: 
- 201, 400, 204, 401, 403





# Infrastructure
Infrastructure as Code with CloudFormation

To create stack run the below command in AWS CLI:
'''aws cloudformation create-stack  \
 --stack-name myteststack   --template-body file://csye6225-infra.yml \
 --parameters ParameterKey=VpcCIDR,ParameterValue="10.0.0.0/16" ParameterKey=PublicSubnet1CIDR,ParameterValue="10.0.3.0/24" ParameterKey=PublicSubnet2CIDR,ParameterValue="10.0.4.0/24" ParameterKey=PublicSubnet3CIDR,ParameterValue="10.0.5.0/24"  --profile Dev_Admin --region us-east-1'''

To delete stack run the below command in AWS CLI:

'''aws cloudformation delete-stack --stack-name myteststack1 --profile Dev_Admin --region us-east-1'''

check the status of stack in AWS console. 

create stack for Assignment 5-
aws cloudformation create-stack  \
 --stack-name myteststack2  --template-body file://csye6225-infra.yml \
 --parameters ParameterKey=VpcCIDR,ParameterValue="10.0.0.0/16" ParameterKey=PublicSubnet1CIDR,ParameterValue="10.0.3.0/24" ParameterKey=PublicSubnet2CIDR,ParameterValue="10.0.4.0/24" ParameterKey=PublicSubnet3CIDR,ParameterValue="10.0.5.0/24" ParameterKey=PrivateSubnet1CIDR,ParameterValue="10.0.6.0/24" ParameterKey=PrivateSubnet2CIDR,ParameterValue="10.0.7.0/24" ParameterKey=PrivateSubnet3CIDR,ParameterValue="10.0.8.0/24" ParameterKey=AMIID,ParameterValue="ami-0618003f89f084843" ParameterKey=MyKeyPair,ParameterValue="CSYE6225" --profile demo1 --region us-east-1 --capabilities CAPABILITY_NAMED_IAM










 




  

