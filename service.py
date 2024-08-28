""" module contains the necesary functions for patient """
import json
import base64
import uuid
import io
import traceback
import numpy as np
import joblib
from PIL import Image
import boto3
from config import GlaucomaConfig
from models import user_account
#import keras
#import tensorflow as tf

s3 = boto3.client("s3")

#MODEL_DIR = "./data/"

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, update
from models import user_type

class DBUtils:
    def create_engine():
        engine = create_engine(GlaucomaConfig.DB_CONNECTION, echo=True)
        return engine

class PatientResource():
    def get_by_patientid(patient_id: int):
        try:
            with Session(DBUtils.create_engine()) as session:
                patient = session.scalars(select(user_account).filter_by(user_account_id=patient_id)).first()
                return {
                    'user_account_id': patient.user_account_id
                    ,'first_name': patient.first_name
                    ,'last_name': patient.last_name
                    ,'patient_doctor_id': patient.patient_doctor_id
                    ,'user_type_id': patient.user_type_id
                    ,'identification_number': patient.identification_number
                    # todo get files
                }
        except Exception as e:
            traceback.print_exc()
            return {"success": False, "message": json.dumps({"error": str(e)})}

    def get_patient_by_doctor_id(doctor_id):
        try:
            with Session(DBUtils.create_engine()) as session:
                result = session.scalars(select(user_account).filter_by(patient_doctor_id=doctor_id)).all()
                return result
        except Exception as e:
            traceback.print_exc()
            return {"success": False, "message": json.dumps({"error": str(e)})}

    def post(json_data):
        try:
            engine = DBUtils.create_engine()
            with Session(engine) as session:
                patient = user_account()
                patient.first_name = json_data.get('first_name')
                patient.last_name = json_data.get('last_name')
                patient.patient_doctor_id = json_data.get('patient_doctor_id')
                patient.identification_number = json_data.get('identification_number')
                row_value = session.scalars(select(user_type.user_type_id).filter_by(name="patient")).first()
                patient.user_type_id = row_value
                session.add(patient)
                session.commit()
                return {
                    "success": True,
                    "data":  {
                        "user_account_id" : patient.user_account_id
                    }
                }
        except Exception as e:
            traceback.print_exc()
            return {"success": False, "message": json.dumps({"error": str(e)})}

    def update(json_data):
        try:
            with Session(DBUtils.create_engine()) as session:
                userid = json_data.get('user_account_id')
                if userid is None or userid == 0:
                    raise Exception('userid not set in the request')

                if not session.scalar(select(select(user_account.user_account_id).filter_by(user_account_id=userid).exists())):
                    raise Exception("User doesn't exists")

                session.query(user_account) \
                .filter_by(user_account_id=userid) \
                .update({
                    'first_name': json_data.get('first_name'),
                    'last_name': json_data.get('last_name'),
                    'identification_number': json_data.get('identification_number')
                })
                session.commit()
                return {"success":True, 'user_account_id': userid}
        except Exception as e:
            traceback.print_exc()
            return {"success": False, "message": json.dumps({"error": str(e)})}
    

def process_image_prediction(json_data):
    """
    - get the prediction of the file from json_data.get('file').
    - save the file on s3.
    - append the filename, the prediction to the files of the patient.
    """
    try:

        # Decode base64 file content
        file_content = base64.b64decode(json_data.get('file').split(',')[1])
        file_extension = json_data.get("fileName").split(".")[1]
        # Generate a unique filename for the S3 object
        file_name = str(uuid.uuid4()).replace('-','') + '.' + file_extension 
        print('file_name ==> '+ file_name)

        # call prediction
        # Upload the file to S3
        s3.put_object(
            Bucket=GlaucomaConfig.GLAUCOMA_STATIC_S3,
            Key="images/" + file_name,
            Body=file_content,
        )
        prediction = __get_prediction_with_knn(file_content)
        return {
            "success": True,
            "message": "Processed image file name " + file_name,
            "prediction": prediction,
            "file_name":file_name,
            "path": GlaucomaConfig.STATIC_S3_IMAGE_DIRECTORY + "/" + file_name
        }
    except Exception as e:
        traceback.print_exc()
        return {"success": False, "message": json.dumps({"error": str(e)})}


def __get_prediction_with_knn(file_content):
    # from image to image array
    img_array = __from_image_to_array(file_content)
    print(img_array)
    # load the model
    loaded_model = joblib.load('./data/knn_model.joblib')
    # Make predictions on new data
    prediction = str(loaded_model.predict([img_array])[0])
    return prediction

# Function to preprocess a single image
def __from_image_to_array(file_content):
    img = Image.open(io.BytesIO(file_content)).convert('L')  # Convert to grayscale
    img = img.resize((64, 64))  # Resize to 64x64 pixels
    img_array = np.array(img).flatten()  # Flatten the image to a 1D array
    return img_array


"""
def __get_prediction(file_content):
    ## get bytes from file content and pass that to
    image_path = io.BytesIO(file_content)

    image_size = 256
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(image_size, image_size))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize the image

    # load the modal
    model = keras.models.load_model(f"{MODEL_DIR}pretrained2.h5")
    model.load_weights(f"{MODEL_DIR}val-best.h5")

    # Make predictions
    predictions = model.predict(img_array)
    return predictions
"""
