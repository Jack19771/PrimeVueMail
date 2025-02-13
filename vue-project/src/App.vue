<template>
  <div id="app">
    <!-- TopBar na górze strony -->
    <TopBar />
    <Toast />

   

    <!-- Miejsce na dynamicznie ładowany widok -->
    <router-view />
    
    <!-- Loader, jeśli strona ładuje się -->
    <Loader v-if="isLoading" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import TopBar from './components/TopBar.vue';
import SidebarMenu from './components/SidebarMenu.vue';
import Loader from './components/Loader.vue';
import Toast from 'primevue/toast';
import topbar from './components/TopBar.vue';

const isLoading = ref(true);

// Symulacja ładowania
onMounted(() => {
  setTimeout(() => {
    isLoading.value = false;
  }, 1000); // Możesz zmienić czas ładowania
});
</script>

<style >
/* Ustawienie marginesu na lewo, aby zrobić miejsce na stały pasek boczny */
.content {
  margin-left: 350px;
  padding: 20px;
  flex-grow: 1;
  margin-top: 80px; 
}

.p-breadcrumb-item-label {
    transition: inherit;
    color: white;
}


.p-fieldset {
    background: var(--p-fieldset-background);
    /* border: 1px solid var(--p-fieldset-border-color); */
    border-radius: var(--p-fieldset-border-radius);
    color: var(--p-fieldset-color);
    padding: var(--p-fieldset-padding);
    margin: 0;
}

</style>
