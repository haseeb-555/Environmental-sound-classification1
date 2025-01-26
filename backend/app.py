from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import librosa
import numpy as np

app = Flask(__name__)
CORS(app)  



UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    extract_features_from_audio(file_path,target_length=22050)
    mfccs = load_and_preprocess_audio(file_path)
    print("mfccs : ", mfccs)
    mfccs = mfccs.reshape(1, -1, 1) 
    print("mfccs : ", mfccs)



    return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200


# Normalize audio amplitude (Peak Normalization or RMS Normalization)
def normalize_amplitude(audio, target_amplitude=1.0):
    # Compute RMS value of the audio
    rms = np.sqrt(np.mean(audio**2))
    # Scale the audio to the target amplitude
    return audio * (target_amplitude / rms) if rms != 0 else audio

# Normalize audio length (Padding or trimming)
def normalize_length(audio, target_length=22050):  # Default length is 1 second at 22.05 kHz
    if len(audio) > target_length:
        # Trim the audio if it's too long
        return audio[:target_length]
    elif len(audio) < target_length:
        # Pad the audio with zeros if it's too short
        return np.pad(audio, (0, target_length - len(audio)), mode='constant')
    return audio


def extract_features_from_audio(file_path, target_length=22050):
    """
    Extracts audio features for testing.
    """
    try:
        # Load the audio file
        x, sample_rate = librosa.load(file_path, sr=None)

        # Normalize amplitude and length
        x = normalize_amplitude(x)
        x = normalize_length(x, target_length=target_length)

        # Extract features
        duration = librosa.get_duration(y=x, sr=sample_rate)
        pitch, _ = librosa.core.piptrack(y=x, sr=sample_rate)
        mean_pitch = np.mean(pitch[pitch > 0])
        tempo, _ = librosa.beat.beat_track(y=x, sr=sample_rate)
        spectral_centroid = librosa.feature.spectral_centroid(y=x, sr=sample_rate)
        frequency_range = np.mean(spectral_centroid)

        # Return features as a list
        print("duration :",duration,"mean_pitch :", mean_pitch,"tempo : ", tempo,"frequency_range : ", frequency_range)
        return [duration, mean_pitch, tempo, frequency_range]

    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

import librosa
import numpy as np

def load_and_preprocess_audio(file_name, sample_rate=None):
    # Load the audio file
    x, sr = librosa.load(file_name, sr=sample_rate, res_type='kaiser_fast')

    # Normalize the audio
    x = librosa.util.normalize(x)

    # Extract MFCC features
    mfccs = librosa.feature.mfcc(y=x, sr=sr, n_mfcc=40)

    # Compute the mean of MFCCs over time to get a fixed-size feature vector
    mfccs = np.mean(mfccs.T, axis=0)

    # Normalize the MFCC features
    mfccs = (mfccs - np.mean(mfccs)) / np.std(mfccs)

    # Return the processed MFCCs
    return mfccs


if __name__ == "__main__":
    app.run(debug=True)
