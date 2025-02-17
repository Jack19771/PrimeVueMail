import './assets/main.css';

import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import 'primeicons/primeicons.css';
import ToastService from 'primevue/toastservice';
import router from './router';
import App from './App.vue';
import keycloak from './keycloak'; // Import Keycloak

const app = createApp(App);

app.use(PrimeVue, {
    theme: {
        preset: Aura,
    },
});
app.use(ToastService);
app.use(router);

// Zapobieganie wielokrotnej inicjalizacji (szczególnie podczas HMR)
if (!window.__KEYCLOAK_INIT) {
    window.__KEYCLOAK_INIT = true;
    keycloak.init({ 
        onLoad: 'login-required', 
        checkLoginIframe: false // Wyłączenie sprawdzania iframe (jeśli potrzebne)
    }).then((authenticated) => {
        if (!authenticated) {
            window.location.reload();
        } else {
            app.config.globalProperties.$keycloak = keycloak;
            app.mount('#app');
        }
    }).catch(() => {
        console.error('Błąd inicjalizacji Keycloak');
    });
} else {
    // Jeśli już inicjalizowano, po prostu przypisz Keycloak i zamontuj aplikację
    app.config.globalProperties.$keycloak = keycloak;
    app.mount('#app');
}

export default {
    components: {
        // Twoje komponenty (np. Checkbox)
    },
};
