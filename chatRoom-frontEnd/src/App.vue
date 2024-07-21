<!-- 
<script setup>
import ChatSub from './views/ChatSub.vue';
</script> -->
<template>
  <header>
    <nav v-if="!user" >
      <!-- <router-link to="/chat">Chat</router-link> -->
      <!-- Display login and logout links based on authentication status -->
      <router-link to="/login">Login</router-link>
      <router-link to="/signup">Sign Up</router-link>
      
    </nav>
  <nav v-if="user">
    <button v-if="user" @click="logout">Logout</button>
    
  </nav>
  </header>
  <main>
    <router-view />
  </main>
</template>

<script>
import { ref, onMounted } from 'vue';
import { auth } from './firebase';
import {useRouter} from "vue-router";

export default {
name: 'App',

setup() {
  const user = ref(null);
  const router = useRouter(); // Initialize the router
  // Check user login state
  onMounted(() => {
    auth.onAuthStateChanged(u => {
      user.value = u;
    });
  });
 
  // Logout method
  const logout = async () => {
    try {
      await auth.signOut();
      await router.push('/');
    } catch (error) {
      console.error('Logout Failed:', error);
      alert('Logout failed. Please try again.');
    }
  };

  return { user, logout };
}
};
</script>
<style>
body{
padding: 0;
margin: 0;
}
#app {
font-family: Avenir, Helvetica, Arial, sans-serif;
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
color: #2c3e50;
}

.logo{
font-size: calc(1.25625rem + .075vw);
margin: 0;
}

header {
background-color: #ffffff;
padding: 10px 20px;
border-bottom: 1px solid #f0eff5 !important;
display: flex;
justify-content: space-between;
align-items: center;
}

nav a, nav button {
margin: 10px;
text-decoration: none;
color: #333;
}

</style>
