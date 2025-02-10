<script setup>
import { ref, onMounted } from 'vue';
import TopBar from '../components/TopBar.vue';  // Zaimportuj komponent TopBar
import SidebarMenu from '../components/SidebarMenu.vue';  // Zaimportuj komponent SidebarMenu
import Inbox from '../components/Inbox.vue';  // Zaimportuj Inbox
import Sent from '../components/Sent.vue';  // Zaimportuj Sent
import Spam from '../components/Spam.vue';  // Zaimportuj Spam
import Drafts from '../components/Drafts.vue';  // Zaimportuj Drafts
import TabView from 'primevue/tabview';  // Zaimportuj TabView
import TabPanel from 'primevue/tabpanel';  // Zaimportuj TabPanel
import Loader from '../components/Loader.vue';  // Zaimportuj komponent Loader
import Toast from 'primevue/toast';
import Account from '../components/Account.vue';  // Zaimportuj komponent Account
import Documentlibrary from '../components/Documentlibrary.vue';  // Zaimportuj komponent Documentlibrary
import AboutUs from '../components/Aboutus.vue';  // Zaimportuj komponent AboutUs
import Chat from '../pages/Chat.vue';  // Zaimportuj komponent Chat
import Members from '../components/Members.vue';  // Zaimportuj komponent Members
import Calendar from '../components/Calendar.vue';  // Zaimportuj komponent Calendar





// Stan ładowania
const isLoading = ref(true);

// Symulacja ładowania (np. API, dane itp.)
onMounted(() => {
    setTimeout(() => {
        isLoading.value = false;  // Po 3 sekundach zmienia się stan na false
    }, 100); // Można dostosować czas
});
</script>

<template>
    <div>
        <SidebarMenu /> <!-- Pasek boczny z menu -->
        <!-- Loader (Pokazuje się dopóki isLoading jest true) -->
        <Loader v-if="isLoading" />

        <!-- Główna zawartość strony, wyświetlana po załadowaniu -->
        <div class="content" v-if="!isLoading">
            <!-- TabView do wyświetlania zakładek -->
            <TabView>
                <TabPanel header="About Us">
                    <AboutUs />
                </TabPanel>
                <TabPanel header="Our Documents">
                    <Documentlibrary />
                </TabPanel>
                <TabPanel header="Calendar">
                    <Calendar />
                </TabPanel>
                <TabPanel header="Messages">
                    <Inbox />
                </TabPanel>
                <TabPanel header="Chat">
                    <Chat />
                </TabPanel>
                <TabPanel header="Members">
                    <Members />
                </TabPanel>
                <TabPanel header="AI Assistant">
                    AI Assistant


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
    margin-top: 80px;
    /* Dodanie marginesu, aby nie było zakryte przez TopBar */
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
