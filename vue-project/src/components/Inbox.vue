<template>
  <Panel header="Received Messages" class="p-mb-1">
    <!-- Przyciski i wyszukiwanie w jednej linii -->
    <div class="p-d-flex p-jc-between p-mb-3">
      <div>
        <Button 
          label="New Mail" 
          icon="pi pi-plus" 
          @click="openNewMailDialog" 
          class="p-mr-2" 
        />
        <Button 
          label="Delete" 
          icon="pi pi-trash" 
          @click="deleteMessages" 
          :disabled="selectedMessages.length === 0" 
          class="p-mr-2" 
        />
        <Button 
          label="Mark as Read" 
          icon="pi pi-check" 
          @click="markAsRead" 
          :disabled="selectedMessages.length === 0" 
        />
      </div>

      <div v-if="loadingMessages" class="p-d-flex p-ai-center p-ml-2">
        <i class="pi pi-spin pi-spinner p-mr-2" style="font-size: 1.4rem; color: #007ad9;"></i>
        <span style="margin-left: 2px; font-size: 0.9rem;">{{ checkingText }}</span>
      </div>
      
      <div v-else class="p-d-flex p-ai-center p-ml-2">
        <span style="font-size: 0.9rem; color: #007ad9;">Last updated: {{ lastUpdated }}</span>
      </div>

      <div>
        <InputText 
          v-model="searchQuery" 
          placeholder="Szukaj wiadomości..." 
          class="p-inputtext p-component" 
        />
      </div>
    </div>

    <div class="message-container">
      <!-- DataTable z wiadomościami -->
      <div class="datatable-container">
        <DataTable 
          v-model:selection="selectedMessages" 
          :value="filteredMessages" 
          selectionMode="checkbox" 
          dataKey="id"
          paginator 
          :rows="rowsPerPage" 
          :totalRecords="totalRecords" 
          :rowsPerPageOptions="[5, 10, 25]" 
          @page="onPageChange"
          @row-click="onRowClick"
        >
          <Column selectionMode="multiple" ></Column>
          <Column field="subject" header="Subject" sortable></Column>
          <Column field="sender" header="Sender" sortable></Column>
          <Column field="date" header="Date" sortable></Column>
          <Column field="status" header="Status" sortable></Column>
        </DataTable>
      </div>

      <!-- Komponent szczegółów wiadomości, otwiera się po prawej stronie -->
      <div v-if="isMessageVisible" class="messagedetails-container">
        <MessageDetails
          :message="selectedMessage"
          :isVisible="isMessageVisible"
          @close="isMessageVisible = false"
        />
      </div>
    </div>
  </Panel>

  <!-- Dialog do tworzenia nowego maila -->
  <Dialog header="New Message" v-model:visible="isDialogVisible" :modal="true" :closable="false" class="p-fluid" style="width: 80vw; height: 80vh;">
    <div>
      <InputText v-model="newMessage.recipient" placeholder="Recipient" class="p-inputtext p-component p-fluid" style="width: 100%;" />
    </div>
    <div class="p-mt-3">
      <InputText v-model="newMessage.subject" placeholder="Subject" class="p-inputtext p-component p-fluid" style="width: 100%;" />

    </div>
    <div class="p-mt-3">
      
      <Editor v-model="newMessage.body" placeholder="Write your message..." style="height: 600px; width: 100%;" />

    </div>

    <div class="p-d-flex p-jc-end p-mt-4">
      <Button label="Cancel" icon="pi pi-times" @click="closeNewMailDialog" class="p-button-text p-mr-2" />
      <Button label="Send" icon="pi pi-check" @click="sendNewMessage" class="p-button-text" />
    </div>
  </Dialog>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Panel from 'primevue/panel';
import axios from 'axios';
import MessageDetails from './MessageDetails.vue'; // Zaimportuj komponent MessageDetails
import Editor from 'primevue/editor';
import { useToast } from 'primevue/usetoast';
import Dialog from 'primevue/dialog';

const toast = useToast();
const messages = ref([]);  // Wiadomości
const selectedMessages = ref([]);  // Wybrane wiadomości
const rowsPerPage = ref(10);  // Domyślna liczba wiadomości na stronie
const totalRecords = ref(0);  // Całkowita liczba wiadomości
const searchQuery = ref('');  // Zapytanie wyszukiwania
const loadingMessages = ref(false);  // Kontroluje spinner
const checkingText = ref("Checking new messages...");  // Tekst podczas sprawdzania
const lastUpdated = ref('');  // Data ostatniego update
const isMessageVisible = ref(false);
const selectedMessage = ref(null);

// Stan dla dialogu tworzenia nowego maila
const isDialogVisible = ref(false);
const newMessage = ref({
  subject: '',
  body: '',
  recipient: ''
});

// Filtrowanie wiadomości na podstawie zapytania
const filteredMessages = computed(() => {
  return messages.value.filter(msg => 
    msg.subject.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
    msg.sender.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// Funkcja obsługująca kliknięcie na wiersz w tabeli
const onRowClick = (event) => {
  selectedMessage.value = event.data;  // Ustawienie wybranej wiadomości
  isMessageVisible.value = true;  // Pokazanie szczegółów wiadomości
};

// Funkcja do pobierania danych z API z symulacją opóźnienia
const fetchMessages = async () => {
  try {
    loadingMessages.value = true;
    checkingText.value = "Checking new messages...";

    await new Promise(resolve => setTimeout(resolve, 3000));

    const response = await axios.get('https://jsonplaceholder.typicode.com/posts');
    messages.value = response.data.map(post => ({
      id: post.id,
      subject: post.title,
      body: post.body,
      sender: `User ${post.userId}`,
      date: new Date().toLocaleString(),
      status: Math.random() > 0.5 ? 'read' : 'unread',
    }));
    totalRecords.value = messages.value.length;
    lastUpdated.value = new Date().toLocaleString();
  } catch (error) {
    console.error('Błąd podczas pobierania wiadomości:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      position: 'bottom-right',
      detail: 'Błąd podczas pobierania wiadomości.',
      life: 3000,
    });
  } finally {
    loadingMessages.value = false;
    checkingText.value = "";
  }
};

// Funkcja do obsługi zmiany strony
const onPageChange = (event) => {
  rowsPerPage.value = event.rows;
};

// Funkcja do usuwania wiadomości
const deleteMessages = () => {
  messages.value = messages.value.filter(msg => !selectedMessages.value.includes(msg));
  selectedMessages.value = [];
};

// Funkcja do oznaczania wiadomości jako przeczytane
const markAsRead = () => {
  selectedMessages.value.forEach(msg => msg.status = 'read');
};

// Funkcja otwierająca dialog nowego maila
const openNewMailDialog = () => {
  newMessage.value = { subject: '', body: '', recipient: '' };
  isDialogVisible.value = true;
};

// Funkcja do wysyłania nowego maila
const sendNewMessage = async () => {
  console.log('Sending new message:', newMessage.value);

  // Przygotowanie danych do wysyłki
  const messageData = {
    recipient: newMessage.value.recipient,
    subject: newMessage.value.subject,
    body: newMessage.value.body,
  };

  try {
    // Wysyłanie danych do serwera Python
    const response = await axios.post('http://127.0.0.1:8000/send-mail', messageData);
    if (response.status === 200) {
      toast.add({
        severity: 'success',
        summary: 'Message Sent',
        detail: `Your message to ${newMessage.value.recipient} has been sent.`,
        life: 3000,
      });
      isDialogVisible.value = false;
    } else {
      toast.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Something went wrong while sending the email.',
        life: 3000,
      });
    }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Error sending message. Please try again later.',
      life: 3000,
    });
  }
};

// Funkcja zamykająca dialog
const closeNewMailDialog = () => {
  isDialogVisible.value = false;
};

// Wywołaj fetchMessages przy załadowaniu komponentu
onMounted(() => {
  fetchMessages();
  setInterval(fetchMessages, 5000);  // Wywołuje fetchMessages co 5 sekund
});
</script>

<style scoped>
.message-container {
  display: flex;
  gap: 20px;
}

.datatable-container {
  flex: 1;  /* DataTable zajmuje połowę szerokości */
}

.messagedetails-container {
  flex: 1;  /* MessageDetails zajmuje drugą połowę szerokości */
  max-width: 50%; /* Ustawienie maksymalnej szerokości na 50% */
}

.p-d-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.p-ml-2 {
  margin-left: 10px;
}

.p-mr-2 {
  margin-right: 10px;
}

.p-d-flex > .p-ml-2 {
  margin-left: 10px;
}

.p-tabview-panels {
  background: var(--p-tabview-tab-panel-background);
  color: var(--p-tabview-tab-panel-color);
}

.messagedetails-container {
  flex: 1;
  max-width: 50%;
  display: flex;
  flex-direction: column;
}

.p-editor {
  width: 100%;  /* Zapewnia, że edytor zajmie pełną szerokość dostępnego kontenera */
  height: auto;  /* Dopasowanie wysokości edytora, jeśli to potrzebne */
}

.message-container {
  display: flex;
  gap: 20px;
  width: 100%;
}

.datatable-container {
  flex: 1;
}

.messagedetails-container {
  flex: 1;
  max-width: 50%;
}
</style>
