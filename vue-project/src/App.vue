<script setup>
import { ref, onMounted } from 'vue';
import TopBar from './components/TopBar.vue';  // Zaimportuj komponent TopBar
import SidebarMenu from './components/SidebarMenu.vue';  // Zaimportuj komponent SidebarMenu
import Inbox from './components/Inbox.vue';  // Zaimportuj Inbox
import Sent from './components/Sent.vue';  // Zaimportuj Sent
import Spam from './components/Spam.vue';  // Zaimportuj Spam
import Drafts from './components/Drafts.vue';  // Zaimportuj Drafts
import TabView from 'primevue/tabview';  // Zaimportuj TabView
import TabPanel from 'primevue/tabpanel';  // Zaimportuj TabPanel
import Loader from './components/Loader.vue';  // Zaimportuj komponent Loader
import Toast from 'primevue/toast';
import Account from './components/Account.vue';  // Zaimportuj komponent Account
// Stan ładowania
const isLoading = ref(true);

// Symulacja ładowania (np. API, dane itp.)
onMounted(() => {
  setTimeout(() => {
    isLoading.value = false;  // Po 3 sekundach zmienia się stan na false
  }, 3000); // Można dostosować czas
});
</script>

<template>
  <div>
    <!-- TopBar na górze strony -->
    <TopBar />
    <Toast />
    <!-- SidebarMenu z nawigacją -->
    <SidebarMenu />

    <!-- Loader (Pokazuje się dopóki isLoading jest true) -->
    <Loader v-if="isLoading" />

    <!-- Główna zawartość strony, wyświetlana po załadowaniu -->
    <div class="content" v-if="!isLoading">
      <!-- TabView do wyświetlania zakładek -->
      <TabView>
        <TabPanel header="Received Messages">
          <Inbox />
        </TabPanel>
        <TabPanel header="Sent Messages">
          <Sent />
        </TabPanel>
        <TabPanel header="Account">
          <Account />
        </TabPanel>
        <TabPanel header="Drafted">
          <Drafts />
        </TabPanel>
      </TabView>
    </div>
  </div>
</template>

<style scoped>
/* Ustawienie marginesu na lewo, aby zrobić miejsce na stały pasek boczny */
.content {
  margin-left: 240px;
  padding: 20px;
  flex-grow: 1;
  margin-top: 80px; /* Dodanie marginesu, aby nie było zakryte przez TopBar */
}

/* Stylizacja nagłówków zakładek */
.p-tabview-nav {
  background-color: #f4f4f4;
}

/* Odstęp od nagłówków zakładek */
.p-tabview-panels {
  margin-top: 20px;
}
</style>
