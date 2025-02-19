<template>
  <div class="container">
    <div class="upload-box">
      <h2>🎵 Upload Your Audio File 🎶</h2>
      <input type="file" @change="handleFileChange" accept="audio/*" />
      <button @click="uploadFile" :disabled="!selectedFile">Upload</button>
    </div>
    
    <div v-if="audioUrl" class="audio-player">
      <h3>🎧 Listen to Uploaded Audio</h3>
      <audio controls>
        <source :src="audioUrl" type="audio/wav" />
        Your browser does not support the audio element.
      </audio>
    </div>

    <div v-if="predictionResult !== null" class="result-card">
      <h3>🔍 Prediction Result</h3>
      <p>{{ predictionResult }}</p>
      
      <div v-if="imageUrl || serverImageUrl">
        <h4>Prediction Image:</h4>
        <img v-if="imageUrl" :src="imageUrl" alt="Mapped Prediction Image" />
        <h4>Spectrogram Image:</h4>
        <img v-if="serverImageUrl" :src="serverImageUrl" alt="Processed Image" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedFile: null,
      predictionResult: null,
      imageUrl: "",
      serverImageUrl: "",
      audioUrl: "",
      imagesMap: {
        "Fire": "fire.jpg",
        "Rain": "rain.jpg",
        "Thunderstorm": "thunderstorm.jpg",
        "WaterDrops": "waterdrops.jpg",
        "Wind": "wind.jpg",
        "Silence": "silence.jpg",
        "TreeFalling": "treefalling.jpg",
        "Helicopter": "helicopter.jpg",
        "VehicleEngine": "vehicleengine.jpg",
        "Axe": "axe.jpg",
        "Chainsaw": "chainsaw.jpg",
        "Generator": "generator.jpg",
        "Handsaw": "handsaw.jpg",
        "Firework": "firework.jpg",
        "Gunshot": "gunshot.jpg",
        "WoodChop": "woodchop.jpg",
        "Whistling": "whistling.jpg",
        "Speaking": "speaking.jpg",
        "Footsteps": "footsteps.jpg",
        "Clapping": "clapping.jpg",
        "Insect": "insect.jpg",
        "Frog": "frog.jpg",
        "BirdChirping": "birdchirping.jpg",
        "WingFlapping": "wingflapping.jpg",
        "Lion": "lion.jpg",
        "WolfHowl": "wolfhowl.jpg",
        "Squirrel": "squirrel.jpg"
      }
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
      if (this.selectedFile) {
        this.audioUrl = URL.createObjectURL(this.selectedFile);
      }
    },

    async uploadFile() {
      if (!this.selectedFile) {
        alert("Please select a file first.");
        return;
      }

      // Get token and user ID from local storage
      const token = localStorage.getItem("token");
      const userId = localStorage.getItem("user_id");

      const formData = new FormData();
      formData.append("file", this.selectedFile);
      formData.append("user_id", userId);  // Include user ID in form data

      try {
        const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            "Authorization": `Bearer ${token}`  // Include access token
          },
        });

        console.log("Response from server:", response.data);

        if (response.data.error) {
          alert(response.data.error);
          return;
        }

        this.predictionResult = response.data.prediction;

        // Map Prediction to Image
        let imageFile = this.imagesMap[this.predictionResult];
        this.imageUrl = imageFile ? `http://127.0.0.1:5000/static/images/${imageFile}` : "";

        // Server-Generated Image
        this.serverImageUrl = `http://127.0.0.1:5000/get_image?image_path=${encodeURIComponent(response.data.image_path)}`;
      } catch (error) {
        console.error("Error uploading file:", error);
        alert("Failed to upload file.");
      }
    }
  }
};
</script>

<style>
.container {
  max-width: 600px;
  margin: auto;
  text-align: center;
  background: #1e1e2f;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  color: white;
  font-family: 'Poppins', sans-serif;
}
.upload-box {
  background: #2a2a3b;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}
button {
  margin-top: 10px;
  padding: 12px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: 0.3s;
}
button:hover {
  background-color: #0056b3;
}
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.result-card {
  background: #2a2a3b;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
}
img {
  margin-top: 10px;
  max-width: 100%;
  border: 2px solid #ddd;
  border-radius: 5px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
audio {
  width: 100%;
  margin-top: 10px;
}
</style>
