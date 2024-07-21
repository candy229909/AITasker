import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomeView.vue'
import Login from '../views/Login.vue';
import SignUp from '../views/SignUp.vue';
import ChatList from '../views/ChatList.vue';
import ChatRoom from '../views/ChatRoom.vue';
import {onAuthStateChanged} from '@/firebase';

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     {path: '/',name: 'home',component: HomeView},
//     { path: '/login', name: 'Login', component: Login },
//     { path: '/signup', name: 'SignUp', component: SignUp },
//     { path: '/chat', name: 'ChatRoom', component: ChatRoom, meta: { requiresAuth: true } }
//     // { path: '/chat', name: 'ChatRoom', component: ChatRoom, meta: { requiresAuth: true } }
//   ]
// })
const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'SignUp', component: SignUp },
  { path: '/chat', name: 'ChatList', component: ChatList, meta: { requiresAuth: true } },
  { path: '/chat/:chatid', name: 'ChatRoom', component: ChatRoom, meta: { requiresAuth: true }}
  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  onAuthStateChanged( (user) => {
      if (requiresAuth && !user) {
          next('/login'); // Redirect to login if not authenticated and trying to access a restricted route
      } else if ((to.path === '/login' || to.path === '/signup') && user) {
          next('/chat'); // Redirect to chat if already logged in and trying to access login or signup
      } else {
          next(); // Proceed normally if the authentication state meets the route requirements
      }
  });
});




export default router
