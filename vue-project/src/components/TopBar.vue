<template>
  <div>
    <Toolbar style="
      position: fixed; 
      top: 0; 
      left: 0; 
      right: 0; 
      z-index: 9999; 
      border-radius: 0; 
      padding: 0rem; 
      background: linear-gradient(45deg, #000, hsl(220, 44%, 18%), hsl(220, 30%, 28%));">
      <template #start>
        <div class="flex items-start gap-2">
          <router-link to="/" style="display: flex; align-items: center;">
            <img src="/NATOOTAN.png" alt="NATO Flag" width="150" />
            <div>
              <h3 id="fasttrack" class="fasttrack-title">FastTrack 2</h3>
              <Breadcrumb :home="home" :model="itemy" class="breadcrumb-custom" />
            </div>
          </router-link>
        </div>
      </template>

      <!-- Pole szukania -->
      <template #center>
        <FloatLabel variant="on" style="width: 300px;">
          <InputText id="on_label" v-model="searchQuery" autocomplete="off" placeholder="Search..." style="width: 150%;" />
          
        </FloatLabel>
      </template>

      <template #end>
        <div class="flex items-center gap-2">
          <router-link to="/settings">
            <Button label="Settings" icon="pi pi-server" class="p-button-contrast" style="margin-right: 20px;" />
          </router-link>
          <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" style="width: 32px; height: 32px;margin-right: 5px;" />
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
import Breadcrumb from 'primevue/breadcrumb';
import FloatLabel from 'primevue/floatlabel';
import InputText from 'primevue/inputtext';
import { ref, onMounted } from 'vue';

const home = ref({ icon: 'pi pi-home' });
const itemy = ref([
  { label: 'NATO' },
  { label: 'SHAPE' },
  { label: 'Command Group' },
  { label: 'COS' },
  { label: 'CSEL' }
]);

const alertMessage = ref(null);
const searchQuery = ref('');
let websocket;

onMounted(() => {
  websocket = new WebSocket('ws://localhost:8000/ws');

  websocket.onmessage = (event) => {
    const message = event.data;
    if (message.startsWith('Alert:')) {
      alertMessage.value = message;
      setTimeout(() => {
        alertMessage.value = null;
      }, 10000);
    }
  };
});
</script>

<style scoped>
.flex {
  display: flex;
  align-items: center;
}

.fasttrack-title {
  margin-left: 10px;
  color: #ffffff;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.breadcrumb-custom {
  color: white;
  background: transparent;
  margin-top: 0 rem;
  font-size: 0.9rem;
  padding: 0px;
  margin-left: 10px;
}

.breadcrumb-custom .p-breadcrumb {
  background: transparent;
  padding: 0 px;
  color: white;
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
}
</style>
