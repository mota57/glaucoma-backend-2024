
- follow the following tutorial 60m
https://github.com/baibhavsagar/Deploy-Flask-App-on-AWS-EC2-Instance

# zip
git archive -v -o myapp.zip --format=zip HEAD


# become a root after log in ssh elastic beanstalk
sudo su -

# current directoy
pwd

# Total RAM
free -h

# Total Available Storage
df -h /

# Total Storage
sudo fdisk -l

# uninstall all packages
python -m pip uninstall -y -r .\requierments.txt


# References

### How to install python
* https://realpython.com/installing-python/#how-to-install-python-on-linux
* https://plainenglish.io/community/how-to-install-python-3-11-with-pip-on-amazon-linux-2023-9ab2ed



## Todo
* create a repository in github in order to upload the code. total (60m)
    * upload the code 10m
    * create a file where you have repository environment variables. 40m
* read the documentation how to deploy flask applications.   60m
    *  https://www.geeksforgeeks.org/how-to-deploy-flask-app-on-aws-ec2-instance/
* give permission to ec2 the permission to put_object, get_object for the s3 glaucoma-website-107594336623 total 20m
* write the instruction to recreate an environment of ec2 1h
    * todo - create instruction to install python.
    * todo - create instruction to install git.
    * todo - create instruction to install aws cli
    * todo - recreate and redeploy.

* create a docker of the application 4h
* create a pipeline for the application 8h