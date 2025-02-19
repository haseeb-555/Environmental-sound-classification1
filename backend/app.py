from flask import Flask, request, jsonify, send_file, send_from_directory
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

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# Configure JWT
app.config["JWT_SECRET_KEY"] = "your_secret_key"
jwt = JWTManager(app)

# Configure SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    audio_files = db.relationship('AudioFile', backref='user', lazy=True)

class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    audio_path = db.Column(db.String(255), nullable=False)
    prediction = db.Column(db.String(100), nullable=False)
    mel_spectrogram_image = db.Column(db.String(255), nullable=False)
    prediction_image = db.Column(db.String(255), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Register Route
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)  # Use user.id instead of username
        return jsonify({"token": access_token, "user_id": user.id}), 200  # Include user_id

    return jsonify({"error": "Invalid credentials"}), 401




UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

audios=['Fire', 'Rain', 'Thunderstorm', 'WaterDrops', 'Wind', 'Silence', 'TreeFalling', 'Helicopter', 'VehicleEngine', 'Axe', 'Chainsaw', 'Generator', 'Handsaw', 'Firework', 'Gunshot', 'WoodChop', 'Whistling', 'Speaking', 'Footsteps', 'Clapping', 'Insect', 'Frog', 'BirdChirping', 'WingFlaping', 'Lion', 'WolfHowl', 'Squirrel']

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

# Serve static images
@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory("static/images", filename)

@app.route("/upload", methods=["POST"])
def upload_file():
    token = request.headers.get("Authorization")

    # Get user ID from form data
    user_id = request.form.get("user_id")

    # Get the uploaded file
    file = request.files.get("file")

    # Print received data
    print("Received Data:")
    print(f"Access Token: {token}")
    print(f"User ID: {user_id}")
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
    
    prediction_result = prediction(image_path)
    # Get prediction result
    image_folder = os.path.join("static", "images")
    # Construct the image filename (assuming images are PNG)
    image_filename = f"{prediction_result}.jpg"
    
    # Full path to the image
    image_path1 = os.path.join(image_folder, image_filename)
    new_audio = AudioFile(user_id=user_id,audio_path=file_path,prediction=prediction_result,mel_spectrogram_image=image_path,prediction_image=image_path1)
    db.session.add(new_audio)
    db.session.commit()

    return jsonify({"message": "File processed successfully", "image_path": image_path, "prediction": prediction_result}), 200

@app.route("/get_image", methods=["GET"])
def get_image():
    image_path = request.args.get("image_path")
    if not image_path or not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404
    
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
        X = X / 255.0

        # Load the model
        model = load_model("model_9967_mel.h5")

        # Predict
        predictions = model.predict(X)  # No need for another expand_dims
        predicted_class = np.argmax(predictions)

        print(f"Predicted Class: {predicted_class}")
        return audios[int(predicted_class)]# Ensure integer value is returned

    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        return "Error"


from tensorflow.keras.models import load_model
# Load the sav

    

if __name__ == "__main__":
    app.run(debug=True)