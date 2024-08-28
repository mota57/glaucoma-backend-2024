import unittest
import requests

class PatientApiHttpHelper:
    def get_by_patientid(patient_id):
        res = requests.get('http://127.0.0.1:5000/patients/get_by_patientid?patient_id='+str(patient_id))
        return res
    def update(patient_data):
        res = requests.put('http://127.0.0.1:5000/patients/update', json=patient_data)
        return res
    def create(patient_data):
        res = requests.post('http://127.0.0.1:5000/patients/create', json=patient_data)
        return res

class TestPatientMethods(unittest.TestCase):

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
        self.assertTrue(patient_response.get('first_name') == patient_update_request.get('first_name'))
        self.assertTrue(patient_response.get('last_name') == patient_update_request.get('last_name'))
        self.assertTrue(patient_response.get('identification_number') == patient_update_request.get('identification_number'))


if __name__ == '__main__':
    unittest.main()