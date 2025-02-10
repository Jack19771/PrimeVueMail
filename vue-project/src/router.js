import { createRouter, createWebHistory } from 'vue-router';
import Home from './pages/Home.vue'; // Główna strona
import Settings from './pages/Settings.vue'; // Ustawienia
import Mail from './pages/Mail.vue'; // Skrzynka mailowa
import Chat from './pages/Chat.vue'; // Chat
import Office from './pages/Office.vue'; // Office

const routes = [
  { path: '/settings', component: Settings },
  { path: '/', component: Office },
  
  
 


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
