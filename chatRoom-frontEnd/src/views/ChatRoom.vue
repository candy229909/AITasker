<template>
    
    <div class="chat-room">
      <ChatRoomHeader></ChatRoomHeader>
      <section class="messages-container">
        <ul class="messages-list">
          <li v-for="message in messages" :key="message.id"
              :class="{ 'my-message': message.uid === currentUser, 'other-message': message.uid !== currentUser }"
              class="message">
             
            <div class="message-wrap">
              <img v-if="message.uid !== currentUser"
              src="https://mdbcdn.b-cdn.net/img/new/avatars/1.webp"
              class="relative inline-block h-12 w-12 !rounded-full object-cover object-center"
              alt="Avatar" />
              <div class="message-wrap-content">
                <p>
                  {{ message.text }}
                </p>
                <small class="time">{{ message.createdAt?.toDate().toLocaleTimeString()}}</small>
              </div>
            </div>
            <div class="conversation-name">
              {{ message.user }}
            </div>
          </li>
        </ul>
      
      </section>
      <form class="message-form" @submit.prevent="sendMessage">
        <input v-model="newMessage" type="text" placeholder="Type your message here..." class="message-input" />
        <button type="submit" class="send-button">
          <svg class="w-6 h-6 rotate-90" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path></svg>
        </button>
      </form>
    </div>

</template>


<script>
import { ref, onMounted } from 'vue';
import { db, auth } from '@/firebase'; // Ensure db is properly exported as Firestore instance
import { collection, query, orderBy, onSnapshot, addDoc, serverTimestamp } from 'firebase/firestore';
import ChatRoomHeader from './ChatRoomHeader.vue';



export default {
  components: {
    ChatRoomHeader,
    // other components
  },
  setup() {
    
    const messages = ref([]);
    const newMessage = ref('');

    // Reference to Firestore collection
    const messagesCollection = collection(db, 'messages');
    const messagesQuery = query(messagesCollection, orderBy('createdAt'));
    
    // Real-time subscription to messages
    onMounted(() => {
      onSnapshot(messagesQuery, (snapshot) => {
        messages.value = snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }));
      });
    });

    // Function to send messages
    const sendMessage = async () => {
      if (newMessage.value.trim()) {
        try {
          await addDoc(messagesCollection, {
            text: newMessage.value,
            uid: auth.currentUser.uid, // Saving UID of the sender
            user: auth.currentUser?.displayName || 'Anonymous',  // Use displayName
            createdAt: serverTimestamp()
          });
          newMessage.value = '';
        } catch (error) {
          console.error('Error adding message: ', error);
        }
      }
    };
    const currentUser = auth.currentUser.uid;

    return { messages, newMessage, currentUser, sendMessage };
  }
};

</script>

<style scoped>

.chat-room {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 51px);
  margin: auto;
  overflow: hidden;
}

.messages-container {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
}

.messages-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.message{
  margin-bottom: 24px;
  position: relative;
  clear: both;
}
.message.my-message {
  float: right;
  text-align: right;
}
.message-wrap {
  display: flex;
  margin-bottom: 10px;
  line-height: 1.4;
}

.message-wrap-content {
  animation: flyIn .6s ease-in-out;
  background-color: #f5f7fb;
  border-radius: 8px 8px 8px 0;
  color: #000000;
  padding: 12px 20px;
  position: relative;
}
.message-wrap-content:before {
  border-bottom: 5px solid transparent;
  border-left: 5px solid #f5f7fb;
  border-right: 5px solid transparent;
  border-top: 5px solid #f5f7fb;
  bottom: -10px;
  content: "";
  left: 0;
  position: absolute;
  right: auto;
}

.time{
  color: hsla(0, 0%, 100%, .5);
  font-size: 12px;
  margin-top: 4px;
  text-align: right;
 }
.conversation-name {
  font-size: 14px;
  font-weight: 500;
}

.my-message .message-wrap-content{
  background-color: #f5f7fb;
  border-radius: 8px 8px 0 8px;
  color: #343a40;
  order: 2;
  text-align: right;
}
.my-message .message-wrap-content:before {
  border-bottom: 5px solid transparent;
  border-left: 5px solid transparent;
  border-right: 5px solid #f5f7fb;
  border-top: 5px solid #f5f7fb;
  left: auto;
  right: 10px;
}
.my-message .time{
  color: #7a7f9a;
  text-align: left;
}


.message-form {
  display: flex;
  padding: 20px;
  /* background: #eceff1; */
  border-top: 1px solid #ccc;
}

.message-input {
  flex-grow: 1;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
}

.send-button {
  padding: 10px 20px;
  background: #FF9900;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 16px;
}

.send-button:hover {
  background: #FF9900;
}



</style>