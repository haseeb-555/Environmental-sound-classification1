<template>
  <div class="upload-container">
    <h1>Upload File</h1>
    <input type="file" @change="handleFileUpload" />
    <button @click="uploadFile">Upload</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedFile: null, // File selected by the user
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0]; // Store the selected file
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert("Please select a file first.");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile); // Append the file to form data

      try {
        const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        alert("File uploaded successfully!");
        console.log(response.data);
      } catch (error) {
        console.error("Error uploading file:", error);
        alert("Failed to upload file.");
      }
    },
  },
};
</script>

<style scoped>
.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
button {
  margin-top: 10px;
  padding: 10px 20px;
  cursor: pointer;
}
</style>
