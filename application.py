from flask import Flask, request, jsonify
from service import process_image_prediction, PatientResource
import json

# EB looks for an 'app' callable by default.
app = Flask(__name__)

version = "0.4"
# add a rule for the index page.
app.add_url_rule('/', 'index', (lambda: "<html><body> version: " + version +  "</body></html>"))


@app.route('/process_image', methods=['POST'])
def handle_json():
    if request.is_json:
        data = request.get_json()
        result = process_image_prediction(data)
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Invalid content type'}), 400

@app.route('/patients/get_by_patientid', methods=['GET'])
def get_by_patientid():
    if request.method == 'GET':
        patient_id = int(request.args.get('patient_id', 0))
        result = PatientResource.get_by_patientid(patient_id)
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Invalid method call on GET request.  Method executed' + request.method}), 400
    

@app.route('/doctor/patients', methods=['GET'])
def get_patient_by_doctor_id():
    if request.method == 'GET':
        doctor_id = request.args.get('key', '')
        result = PatientResource.get_patient_by_doctor_id(doctor_id)
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Invalid method call on GET request.  Method executed' + request.method}), 400
    
# create user data.
@app.route('/patients/create', methods=['POST'])
def create_patient():
    if request.is_json:
        data = request.get_json()
        result = PatientResource.post(data)
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Invalid content type'}), 400
    
@app.route('/patients/update', methods=['PUT'])
def update_patient():
    if request.is_json:
        data = request.get_json()
        result = PatientResource.update(data)
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Invalid content type'}), 400
    

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()