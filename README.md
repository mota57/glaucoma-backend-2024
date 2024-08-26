
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

## find environment variable
printenv | grep AWS_DEFAULT_PROFILE

## activate environment 
source .venv/bin/activate

# References

### How to install python
* https://realpython.com/installing-python/#how-to-install-python-on-linux
* https://plainenglish.io/community/how-to-install-python-3-11-with-pip-on-amazon-linux-2023-9ab2ed

