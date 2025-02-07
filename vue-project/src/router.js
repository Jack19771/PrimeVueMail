import { createRouter, createWebHistory } from 'vue-router';
import Home from './pages/Home.vue'; // Główna strona
import Settings from './pages/Settings.vue'; // Ustawienia
import Mail from './pages/Mail.vue'; // Skrzynka mailowa
import Chat from './pages/Chat.vue'; // Chat


const routes = [
  { path: '/settings', component: Settings },
  { path: '/mail', component: Mail },
  { path: '/', component: Home },
  { path: '/chat', component: Chat }
 


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
