<template>
  <div class="home">
    <h1>Have fun with AITasker</h1>
    <p>Need to login to chat</p>
    <div>
      <router-link to="/login" class="button">Login</router-link>
      <router-link to="/signup" class="button">Sign Up</router-link>
    </div>
  </div>
</template>
<script>
export default {
  name: 'AppHome'
};
</script>
<style scoped>
.home {
  text-align: center;
  padding: 50px;
  margin-top: 50px;
}

h1 {
  margin-bottom: 20px;
}

p {
  margin-bottom: 20px;
  color: #666;
  font-size: 18px;
}

.button {
  margin: 10px;
  padding: 10px 20px;
  color: white;
  background-color: #FF9900;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
}

.button:hover {
  background-color: #FF9900;
}
</style>