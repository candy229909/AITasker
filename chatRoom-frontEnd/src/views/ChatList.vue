<template>
      <ChatListHeader />
    <div class="min-h-screen flex flex-col items-center py-4">
      <div class="w-full p-4 bg-white rounded shadow-md">
        <div v-for="user in users" :key="user.id" class="flex items-center py-4 border-b border-gray-200 last:border-b-0" @click="toggleActive(user.id)">
          <img :src="user.avatar" alt="Avatar" class="w-10 h-10 rounded-full mr-4">
          <div>
            <div class="font-bold">{{ user.user }}</div>
            <div>{{ user.text }}</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ChatListHeader from './ChatListHeader.vue';
  import { collection, getDocs, query, limit, orderBy } from "firebase/firestore";
  import { db } from "../firebase";
  export default {
    components: {
    ChatListHeader,
    // other components
    },
    data() {
      return {
        users: [
          { id: 1, user: 'A', text: 'hello, I want to buy your service', avatar: 'https://mdbcdn.b-cdn.net/img/new/avatars/1.webp' },
          // Add more messages as needed
        ]
      };
    },
  //   data() {
  //     return {
  //       users: [],
  //     };
  //   },
  //   async created() {
  //   const querySnapshot = await getDocs(collection(db, "users"));
  //   for (const doc of querySnapshot.docs) {
  //     const userData = { uid: doc.id, ...doc.data() };

  //     // Fetch the latest message for each user
  //     const messagesCollection = collection(db, "messages", userData.uid, "messages");
  //     const latestMessageQuery = query(messagesCollection, orderBy("createdAt", "desc"), limit(1));
  //     const messageSnapshot = await getDocs(latestMessageQuery);

  //     if (!messageSnapshot.empty) {
  //       const latestMessage = messageSnapshot.docs[0].data();
  //       userData.latestMessage = {
  //         text: latestMessage.text,
  //         createdAt: latestMessage.createdAt
  //       };
  //     }

  //     this.users.push(userData);
  //   }
  // },
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
  