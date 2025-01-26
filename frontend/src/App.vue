<template>
  <div id="app">
    <!-- File Upload Component -->
    <FileUpload />
  </div>
</template>

<script>
import FileUpload from './components/FileUpload.vue';

export default {
  name: 'App',
  components: {
    FileUpload, // Registering the FileUpload component
  },
};
</script>

<style>
/* Add global styles if necessary */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8f9fa; /* Light gray background for better aesthetics */
}

#app {
  text-align: center;
  padding: 20px;
}
</style>
