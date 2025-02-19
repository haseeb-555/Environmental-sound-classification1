<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>{{ isRegistering ? "Register" : "Login" }}</h2>

      <input type="text" v-model="username" placeholder="Username" />
      <input type="password" v-model="password" placeholder="Password" />

      <button @click="isRegistering ? register() : login()">
        {{ isRegistering ? "Register" : "Login" }}
      </button>

      <p @click="toggleAuthMode">
        {{ isRegistering ? "Already have an account? Login" : "New user? Register" }}
      </p>

      <p v-if="message" class="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      isRegistering: false,
      message: "",
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/register", {
          username: this.username,
          password: this.password,
        });
        this.message = response.data.message;
        this.isRegistering = false;
      } catch (error) {
        this.message = error.response?.data?.error || "Registration failed.";
      }
    },
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/login", {
          username: this.username,
          password: this.password,
        });

        // Store token and user ID in localStorage
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("userId", response.data.user_id); // 🔹 Store userId

        this.message = "Login successful!";
        console.log("User ID:", localStorage.getItem("userId")); // Debugging check
        this.$router.push("/dashboard"); // Redirect after login
      } catch (error) {
        this.message = error.response?.data?.error || "Login failed.";
      }
    },
    toggleAuthMode() {
      this.isRegistering = !this.isRegistering;
      this.message = "";
    }
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #121212;
}

.auth-box {
  background: #2a2a3b;
  padding: 20px;
  border-radius: 8px;
  color: white;
  text-align: center;
  width: 300px;
}

input {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
  border: none;
}

button {
  padding: 10px;
  background: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  width: 100%;
  border-radius: 5px;
}

button:hover {
  background: #0056b3;
}

p {
  cursor: pointer;
  margin-top: 10px;
  color: #ccc;
}

.message {
  margin-top: 10px;
  color: #ff6666;
}
</style>
