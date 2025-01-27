import { createRouter, createWebHistory } from 'vue-router';
import Inbox from './components/Inbox.vue';
import Sent from './components/Sent.vue';  // Przykładowy komponent dla "Wysłane"
import Spam from './components/Spam.vue';  // Przykładowy komponent dla "Spam"
import Drafts from './components/Drafts.vue';  // Przykładowy komponent dla "Szkice"

const routes = [
  { path: '/inbox', component: Inbox },
  { path: '/sent', component: Sent },
  { path: '/spam', component: Spam },
  { path: '/drafts', component: Drafts },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
