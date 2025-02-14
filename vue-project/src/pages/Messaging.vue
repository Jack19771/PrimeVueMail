<script>
import { ref, onMounted } from 'vue';
import TabView from 'primevue/tabview';  // Zaimportuj TabView
import TabPanel from 'primevue/tabpanel';  // Zaimportuj TabPanel
import Inbox from '../components/Inbox.vue';  // Zaimportuj Inbox
import Sent from '../components/Sent.vue';  // Zaimportuj Sent
import Account from '../components/Account.vue';  // Zaimportuj komponent Account
import Drafts from '../components/Drafts.vue';  // Zaimportuj Drafts
import Messaging from '../pages/Messaging.vue';


</script>



<template>
    <div>
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