""" module contains the necesary functions for patient """
import json
import base64
import uuid
import io
import traceback
#import tensorflow as tf
import numpy as np
#import keras
import joblib
from PIL import Image
import boto3
from config import GlaucomaConfig

s3 = boto3.client("s3")
#MODEL_DIR = "./data/"

def process_image_prediction(json_data):
    """
    - get the prediction of the file from json_data.get('file').
    - save the file on s3.
    - append the filename, the prediction to the files of the patient.
    """
    try:

        # Decode base64 file content
        file_content = base64.b64decode(json_data.get('file').split(',')[1])
        file_name = json_data.get("fileName")

        # Generate a unique filename for the S3 object
        filename = str(uuid.uuid4()) + '.' + file_name.split(".")[1]
        print(file_name + " ---> " + filename)

        # call prediction
        # Upload the file to S3
        s3.put_object(
            Bucket=GlaucomaConfig.EB_GLAUCOMA_API_WEBSITE_STATIC_S3,
            Key="images/" + filename,
            Body=file_content,
        )
        prediction = __get_prediction_with_knn(file_content)
        return {
            "success": True,
            "message": "Processed image file name " + filename,
            "prediction": prediction,
            "fileName":filename
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