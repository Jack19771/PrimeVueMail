import { createRouter, createWebHistory } from 'vue-router';
import Home from './pages/Home.vue'; // Główna strona
import Settings from './pages/Settings.vue'; // Ustawienia
import Mail from './pages/Mail.vue'; // Skrzynka mailowa


const routes = [
  { path: '/settings', component: Settings },
  { path: '/mail', component: Mail },
  { path: '/', component: Home },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
