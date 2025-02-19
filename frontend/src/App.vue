<template>
  <div id="app">
    <router-view></router-view> <!-- This is required for routing to work -->
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Global styles */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8f9fa;
}

#app {
  text-align: center;
  padding: 20px;
}
</style>
