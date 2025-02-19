<template>
  <div>
    <h1>Welcome to Your Dashboard 🎵</h1>
    <button @click="logout" class="logout-btn">Logout</button>
    
    <FileUpload />
  </div>
</template>

<script>
import FileUpload from '../components/FileUpload.vue';
import { useRouter } from 'vue-router';

export default {
  components: { FileUpload },
  setup() {
    const router = useRouter();

    const logout = () => {
      localStorage.removeItem("token");  // Clear authentication token
      router.push("/");  // Redirect to login page
    };

    return { logout };
  }
};
</script>

<style>
h1 {
  text-align: center;
  color: black;
}
.logout-btn {
  display: block;
  margin: 20px auto;
  padding: 10px 15px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: 0.3s;
}
.logout-btn:hover {
  background-color: #cc0000;
}
</style>
