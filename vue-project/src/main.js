import './assets/main.css'

import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import Lara from '@primevue/themes/lara'
import material from '@primevue/themes/material'
import nora from '@primevue/themes/nora'
import 'primeicons/primeicons.css'
import Editor from 'primevue/editor';
import ToastService from 'primevue/toastservice';
import Checkbox from 'primevue/checkbox';
import router from './router'; // Musi być poprawnie zaimportowany router
import App from './App.vue'
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet/dist/leaflet';


const app = createApp(App);
app.use(PrimeVue, {
     theme: {
        preset : Aura,
        
         },
});
app.use(ToastService); // Dodanie ToastService
app.use(router);
export default {
   components: {
     Checkbox
   }
 };

app.mount('#app')


