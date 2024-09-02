
  
## TODO 9/29/2024 PART 2
    - [x] test /doctors/find_by_id
    - [x] test /doctors/find_by_id  with patient files
    - [x] At /doctors/find_by_id  Load patient_files.status = pfile.file_status.name
    - [] test /doctors/create
    - [] test /doctors/update
    
## TODO 8/27/2024 PART 1
* [X] - create CREATE, GET, UPDATE methods for patient 
  - [x] test /patients/create
  - [x] test /patients/get_by_patientid
  - [x] test /patients/update

## backlog
- implement email address to the user table. For both patient and doctor.
- implement amazon cognito to log user with google account and secure route.
- create unique for identiciation number.
    - validate you cant create more than one user with the same identification number when creating a patient, doctor and so on.
- Add validation for required parameters at /patients/post
    - [] Add validation required for patient_doctor_id
- [] return the files for /patients/get_by_patientid
- [] test /patients/delete
    - basically we are going to add a new column in the database where we add the is_deleted
    - add a global query where is_deleted objects cant be pull with orm.

- [] - implement the following template https://github.com/tomasrasymas/flask-restful-api-template/blob/master/endpoints/users/resource.py

## Todo 8/23/2024
* [x] - login as user in with aws

## todo past
* create a repository in github in order to upload the code. total (60m)
    * upload the code 10m
    * create a file where you have repository environment variables. 40m
* read the documentation how to deploy flask applications.   60m
    *  https://www.geeksforgeeks.org/how-to-deploy-flask-app-on-aws-ec2-instance/
* give permission to ec2 the permission to put_object, get_object for the s3 glaucoma-website-107594336623 total 20m
* write the instruction to recreate an environment of ec2 1h
    * todo - create instruction to install python, git aws cli
    * todo - recreate and redeploy.

* create a docker of the application 4h
* create a pipeline for the application 8h