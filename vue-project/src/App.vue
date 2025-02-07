<template>
  <div>
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

<style scoped>
/* Ustawienie marginesu na lewo, aby zrobić miejsce na stały pasek boczny */
.content {
  margin-left: 240px;
  padding: 20px;
  flex-grow: 1;
  margin-top: 80px; 
}


</style>
