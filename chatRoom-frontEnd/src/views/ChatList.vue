<template>
      <ChatListHeader />
    <div class="bg-gray-100 min-h-screen flex flex-col items-center">
      <div class="w-full max-w-md p-4 bg-white rounded shadow-md">
        <div v-for="message in messages" :key="message.id" class="flex items-center py-4 border-b border-gray-200 last:border-b-0" @click="toggleActive(message.user)">
          <img :src="message.avatar" alt="Avatar" class="w-10 h-10 rounded-full mr-4">
          <div>
            <div class="font-bold">{{ message.user }}</div>
            <div>{{ message.text }}</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ChatListHeader from './ChatListHeader.vue';
  export default {
    components: {
    ChatListHeader,
    // other components
    },
    data() {
      return {
        messages: [
          { id: 1, user: 'A', text: 'hello, I want to buy your service', avatar: 'https://mdbcdn.b-cdn.net/img/new/avatars/1.webp' },
          // Add more messages as needed
        ]
      };
    },
    methods:{
        toggleActive(user){
        console.log(user);
        this.$router.push(`/chat/user=${user}`);
      },

    }
  };
  </script>
  
  <style>
  /* Add any custom styles here */
  </style>
  