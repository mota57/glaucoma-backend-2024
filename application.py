from flask import Flask, request, jsonify
import patient_service

# EB looks for an 'app' callable by default.
app = Flask(__name__)

version = "0.3"
# add a rule for the index page.
app.add_url_rule('/', 'index', (lambda: "<html><body> version: " + version +  "</body></html>"))


@app.route('/process_image', methods=['POST'])
def handle_json():
    if request.is_json:
        data = request.get_json()
        result = patient_service.process_image_prediction(data)
        # Return a response
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Invalid content type'}), 400

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()