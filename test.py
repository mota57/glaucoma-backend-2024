import unittest
import requests
import json
import os
import random

DOMAIN_URL = os.getenv('GLAUCOMA_DOMAIN_URL', 'http://127.0.0.1:5000')

class DoctorApiHttpHelper:
    def __init__(self):
        print('init doctor api helper')

    def find_by_id(id):
        res = requests.get(DOMAIN_URL + '/doctors/find_by_id/'+str(id))
        assert res.status_code == 200
        return json.loads(res.json())
    
    def update(doctor_data):
        res = requests.put(DOMAIN_URL + '/doctors/update', json=doctor_data)
        assert res.status_code == 200
        return res.json()
    def create(doctor_data):
        res = requests.post(DOMAIN_URL + '/doctors/create', json=doctor_data)
        assert res.status_code == 200
        return res.json()

class PatientApiHttpHelper:
    def get_by_patientid(patient_id):
        res = requests.get(DOMAIN_URL + '/patients/get_by_patientid?patient_id='+str(patient_id))
        return res
    def update(patient_data):
        res = requests.put(DOMAIN_URL + '/patients/update', json=patient_data)
        return res
    def create(patient_data):
        res = requests.post(DOMAIN_URL + '/patients/create', json=patient_data)
        return res

class TestUserAccountMethods(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('init setup called')
    
    def test_create_doctor(self):
        # test create doctor
        doctor_req = {
            'first_name' : "zaman-" + str(random.randrange(0, 1000)) ,
            'last_name' : "test-" + str(random.randrange(0, 1000)), 
            'identification_number': str(random.randrange(0, 1000)) + str(random.randrange(0, 1000))
        }
        json_data = DoctorApiHttpHelper.create(doctor_req)
        print(json.dumps(json_data, indent=2))
        self.assertTrue(json_data.get('data')['doctor_id'] >= 0)
        # update doctor
        doctor_req = {
            'first_name' : "zaman-" + str(random.randrange(0, 1000)) ,
            'last_name' : "test-update-" + str(random.randrange(0, 1000)), 
            'identification_number': str(random.randrange(0, 1000)) + str(random.randrange(0, 1000))
        }
        json_data = DoctorApiHttpHelper.update(doctor_req)

        # test get doctor
        doctor_id = json_data.get('data')['doctor_id']
        json_data = DoctorApiHttpHelper.find_by_id(doctor_id)
        print(json.dumps(json_data, indent=2))
        self.assertTrue(json_data.get('user_account_id') == doctor_id)
        self.assertTrue(json_data.get('first_name') == doctor_req.get('first_name'))
        self.assertTrue(json_data.get('last_name') == doctor_req.get('last_name'))
        self.assertTrue(json_data.get('user_type_id') == 1)

    def test_patient_service(self):
        """
        call create, update and delete a patient. Assuming there is a doctor in the database with ID=1
        """
        data_req = {
            'first_name' : "hector" ,
            'last_name' : "mota", 
            'user_type_id' : 2,  #patient
            'patient_doctor_id' : 1, #doctor number 1
            'identification_number':'00118753250'
        }
        # test create patient
        print('call create patient')
        response = PatientApiHttpHelper.create(data_req)
        self.assertTrue(response.status_code == 200)
        data_json = response.json()
        print(data_json)
        user_account_id = data_json.get('data').get('user_account_id')
        
        # get by patientid
        print('call get_by_patient_id: '+str(user_account_id))
        response = PatientApiHttpHelper.get_by_patientid(user_account_id)
        self.assertTrue(response.status_code == 200)
        patient_json = response.json()
        self.assertTrue(patient_json.get('user_account_id') == user_account_id)
        print(patient_json)

        # test update patient
        print('call update patient_id: '+str(user_account_id))
        patient_update_request = {
            'user_account_id': user_account_id,
            'first_name': 'hector_update_test',
            'last_name': 'modata_update_test',
            'identification_number': '00_test_update'
        }

        response = PatientApiHttpHelper.update(patient_update_request)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json().get('success'))
        # check update has correct values
        print('call get_by_patient_id: '+str(user_account_id))
        response = PatientApiHttpHelper.get_by_patientid(user_account_id)
        self.assertTrue(response.status_code == 200)
        patient_response = response.json()
        print('logging response:: ' + json.dumps(patient_response, indent=2))
        self.assertTrue(patient_response.get('first_name') == patient_update_request.get('first_name'))
        self.assertTrue(patient_response.get('last_name') == patient_update_request.get('last_name'))
        self.assertTrue(patient_response.get('identification_number') == patient_update_request.get('identification_number'))


if __name__ == '__main__':
    unittest.main()