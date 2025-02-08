from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import noisereduce as nr
from scipy.signal import butter, lfilter
from scipy.io import wavfile
import matplotlib
matplotlib.use("Agg")  # Set the backend to 'Agg' (Non-GUI)
import matplotlib.pyplot as plt


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def apply_noise_reduction(data, rate):
    return nr.reduce_noise(y=data, sr=rate)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

def normalize_audio(data):
    max_val = np.max(np.abs(data))
    return data / max_val if max_val != 0 else data

def extract_mfcc_and_save_image(file_path, image_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfccs, x_axis='time', cmap='viridis')
    plt.colorbar()
    plt.title(f"MFCC - {os.path.basename(file_path)}")
    plt.tight_layout()
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
    plt.close()

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    rate, data = wavfile.read(file_path)
    
    if data.ndim == 2:
        left_channel = apply_noise_reduction(data[:, 0], rate)
        right_channel = apply_noise_reduction(data[:, 1], rate)
        reduced_noise = np.column_stack((left_channel, right_channel))
    else:
        reduced_noise = apply_noise_reduction(data, rate)
    
    cutoff_frequency = 4000  
    filtered_audio = butter_lowpass_filter(reduced_noise, cutoff_frequency, rate)
    normalized_audio = normalize_audio(filtered_audio)
    
    processed_file_path = os.path.join(OUTPUT_FOLDER, file.filename)
    wavfile.write(processed_file_path, rate, np.int16(normalized_audio * 32767))
    
    image_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(file.filename)[0]}.png")
    extract_mfcc_and_save_image(processed_file_path, image_path)
    print(prediction(image_path))


    return jsonify({"message": "File processed successfully", "image_path": image_path}), 200

@app.route("/get_image", methods=["GET"])
def get_image():
    image_path = request.args.get("image_path")
    if not image_path or not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404
    print(prediction(image_path))
    return send_file(image_path, mimetype='image/png')

from keras.preprocessing import image

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def prediction(image_path):
    try:
        # Load image and convert to array
        img = image.load_img(image_path, target_size=(224, 224, 3))
        img_array = image.img_to_array(img)

        # Convert to numpy array and normalize
        X = np.expand_dims(img_array, axis=0)  # Adding batch dimension (1, 224, 224, 3)
        X=X/255
        print(X)
        print(f"Processed image shape: {X.shape}")

        # Load the model
        model = load_model("model_9967_mel.h5")

        # Predict
        predictions = model.predict(X)  # No need for another expand_dims
        print(X)
        predicted_class = np.argmax(predictions)


        print(f"Predicted Class: {predicted_class}")

    except Exception as e:
        print(f"Error loading {image_path}: {e}")


from tensorflow.keras.models import load_model
# Load the sav

    

if __name__ == "__main__":
    app.run(debug=True)




