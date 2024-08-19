import json
import boto3
import base64
import uuid
import tensorflow as tf
import numpy as np
import keras
import io
from config import GlaucomaConfig

s3 = boto3.client("s3")
MODEL_DIR = "./data/"


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
        prediction = __get_prediction(file_content)
        # Upload the file to S3
        s3.put_object(
            Bucket=GlaucomaConfig.EB_GLAUCOMA_API_WEBSITE_STATIC_S3(),
            Key="images/" + filename,
            Body=file_content,
        )
        return {
            "success": True,
            "message": "Processed image file name " + filename,
            "prediction": str(prediction[0][0]),
            "fileName":filename
        }
    except Exception as e:
        return {"success": False, "message": json.dumps({"error": str(e)})}


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
