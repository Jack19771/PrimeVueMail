<template>
  <div>
    <Toolbar style="position: fixed; top: 0; left: 0; right: 0; z-index: 9999; border-radius: 0; padding: 1rem; background: linear-gradient(to top, #505050 , #000000);">
      <template #start>
        <div class="flex items-center gap-2">
          <router-link to="/" style="display: flex; align-items: center;">
            <i class="pi pi-envelope" style="font-size: 2rem; color: #ffffff;"></i>
            <h3 style="margin-left: 10px; color: #ffffff; font-size: 1.5rem; font-weight: bold;">FastTrack 2</h3>
          </router-link>
        </div>
      </template>

      <template #end>
        <div class="flex items-center gap-2">
          <router-link to="/settings">
            <Button label="Settings" severity="contrast" size="small" />
          </router-link>
          <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" style="width: 32px; height: 32px" />
        </div>
      </template>
    </Toolbar>

    <!-- Banner alertu -->
    <div v-if="alertMessage" class="alert-banner">
      {{ alertMessage }}
    </div>
  </div>
</template>

<script setup>
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
import Avatar from 'primevue/avatar';
import { ref, onMounted } from 'vue';

const alertMessage = ref(null);

let websocket;

onMounted(() => {
  websocket = new WebSocket('ws://localhost:8000/ws');

  websocket.onmessage = (event) => {
    const message = event.data;
    if (message.startsWith('Alert:')) {
      alertMessage.value = message;
      setTimeout(() => {
        alertMessage.value = null;
      }, 100000); // Ukryj alert po 10 sekundach
    }
  };
});
</script>

<style scoped>
.flex {
  display: flex;
  align-items: center;
}

.alert-banner {
  background-color: red;
  color: white;
  text-align: center;
  padding: 1rem;
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  z-index: 1000;
  font-weight: bold;
  font-size: 1,5rem !important; /* Dodanie !important */
  
}
</style>
