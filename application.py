from http.client import HTTPException
from flask import Flask, request, jsonify
from service import process_image_prediction, PatientResource, DoctorResource
import json

# EB looks for an 'app' callable by default.
app = Flask(__name__)

version = "0.4"
# add a rule for the index page.
app.add_url_rule('/', 'index', (lambda: "<html><body> version: " + version +  "</body></html>"))

## global exception

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    print('error=' + str(e))
    return jsonify(error=str(e)), code

def build_response(payload):
    if isinstance(payload, dict):
        return payload
    json_data = json.dumps(payload, default=lambda o: o.__dict__)
    return json_data

## ROUTE doctors

@app.route('/doctors/find_by_id/<doctor_id>', methods=['GET'])
def doctors_find_by_id(doctor_id):
    if request.method == 'GET':
        result = DoctorResource.find_by_id(int(doctor_id))
        return jsonify(build_response(result)), 200
    else:
        return jsonify({'error': 'Invalid method call request.  Method executed' + request.method}), 400


@app.route('/doctors/create', methods=['POST'])
def doctors_create():
    if request.method == 'POST':
        data = request.get_json()
        result = DoctorResource.create(data)
        return jsonify(build_response(result)), 200
    else:
        return jsonify({'error': 'Invalid method call request. Method executed' + request.method}), 400

@app.route('/doctors/update/<doctor_id>', methods=['POST'])
def doctors_update(doctor_id):
    if request.method == 'POST':
        data = request.get_json()
        result = DoctorResource.update(int(doctor_id, data))
        return jsonify(build_response(result)), 200
    else:
        return jsonify({'error': 'Invalid method call request.  Method executed' + request.method}), 400

## ROUTE patients
@app.route('/process_image', methods=['POST'])
def patients_process_image():
    if request.is_json:
        data = request.get_json()
        result = process_image_prediction(data)
        return jsonify({'payload':json.dumps(result)}), 200
    else:
        return jsonify({'error': 'Invalid content type'}), 400

@app.route('/patients/get_by_patientid', methods=['GET'])
def patients_get_by_patientid():
    if request.method == 'GET':
        patient_id = int(request.args.get('patient_id', 0))
        result = PatientResource.get_by_patientid(patient_id)
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Invalid method call request.  Method executed' + request.method}), 400
        
# create user data.
@app.route('/patients/create', methods=['POST'])
def patients_create():
    if request.is_json:
        data = request.get_json()
        result = PatientResource.post(data)
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Invalid content type'}), 400
    
@app.route('/patients/update', methods=['PUT'])
def patients_update():
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