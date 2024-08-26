* at the terminal enter the following.
* aws configure sso
* SSO session name (Recommended): dev
* SSO start URL [None]: https://d-9067ec8d2e.awsapps.com/start
* SSO region [None]: us-east-1

aws
# append secret and access key config
* go to ~/.aws/credentials 
* edit config and paste credentials from  https://d-9067ec8d2e.awsapps.com/start


## snippet to run
import os
os.environ['AWS_DEFAULT_PROFILE'] = 'AdministratorAccess-107594336623'