from flask import Flask, request, jsonify, render_template
#import os
import numpy as np
from PIL import Image
import keras
import requests
#import gdown

#os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'




def normalization1(array):
    return array / array.max()




#def download_keras_model_from_drive(drive_url, output_path):
    #gdown.download(drive_url, output_path, quiet=False)

# Example usage
url = "https://drive.google.com/uc?id=1EuonbsCgLzPqiiIfJ-xIQBuETxV6EgmR"  # Replace with your actual URL
output_path = "my_model.keras"
#https://drive.google.com/file/d/1EuonbsCgLzPqiiIfJ-xIQBuETxV6EgmR/view?usp=sharing
#download_keras_model_from_drive(url, output_path)


# Check if file exists
##    print(f"File exists: {output_path}")
#else:
#    print(f"File not found at {output_path}")

# Verify file size or integrity
#file_size = os.path.getsize(output_path)
#print(f"Downloaded file size: {file_size} bytes")

# Load your Keras model
#model = keras.models.load_model(output_path)

app = Flask(__name__)
@app.route('/')
def upload_form():
    return render_template('upload.html')  # Render the upload form


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image = Image.open(file)

        #image.show()
        new_img = image.resize((256, 256))
        image_array = [np.array(new_img)]
        inputs = np.array(image_array)

        # Prepare the input for the model

        inputs_reshaped = inputs.reshape(inputs.shape[0], (256 * 256 * 3))

        inputsNormalised = normalization1(inputs_reshaped)

        #predicted1 = model.predict(inputsNormalised)

        #max_index = np.argmax(predicted1[0])
        max_index=1;
        if (max_index == 0):
            result='T4'
        if (max_index == 1):
            result='NON T4'

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)