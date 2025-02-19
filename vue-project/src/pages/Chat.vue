<template>
    <div class="dupa">
      <Card>
        <template #title>Real-Time Chat</template>
        <template #content>
          <ul class="message-list" ref="messageList">
            <li v-for="(msg, index) in messages" :key="index" :class="['message-item', msg.isSent ? 'right-message' : 'left-message']">
              <!-- Wyświetlanie autora i daty -->
              <div class="message-header">
                <span class="message-author">{{ msg.author }}</span>
                <span class="message-time">{{ msg.timestamp }}</span>
              </div>
              <!-- IMPORTANT -->
              <div v-if="msg.isImportant" class="important-label">IMPORTANT</div>
              <div class="message-text">{{ msg.text }}</div>
            </li>
            <li v-if="messages.length === 0">No messages yet.</li>
          </ul>
        </template>
      </Card>
  
      <div class="input-section">
        <Checkbox v-model="isImportant" label="Mark as Important" class="important-checkbox" />
        <InputText v-model="newMessage" placeholder="Type your message..." class="input-field" @keyup.enter="sendMessage" />
        <Button icon="pi pi-send" class="p-button-rounded p-button-success" @click="sendMessage" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, nextTick } from 'vue';
  import Card from 'primevue/card';
  import Button from 'primevue/button';
  import InputText from 'primevue/inputtext';
  import Checkbox from 'primevue/checkbox';

  // Get logged user
import keycloak from '@/keycloak'; // Importujemy Keycloak

const username = ref('Anonimowy'); // Domyślnie anonimowy użytkownik

onMounted(() => {
  if (keycloak.authenticated) {
    username.value = keycloak.tokenParsed?.preferred_username || keycloak.tokenParsed?.name || 'Anonimowy';
    console.log("Zalogowany użytkownik:", username.value); // Sprawdzamy w konsoli
  } else {
    console.log("Użytkownik niezalogowany");
  }
});

  
  // WebSocket
  const socket = new WebSocket('ws://192.168.178.73:8000/ws');  // Upewnij się, że adres i port są poprawne
  
  // Message data
  const messages = ref([]);
  const newMessage = ref('');
  const messageList = ref(null);
  const isImportant = ref(false);  // Flag to mark message as important
  
  // Scroll to the latest message
  const scrollToBottom = () => {
    if (messageList.value) {
      messageList.value.scrollTop = messageList.value.scrollHeight;
    }
  };
  
  // Format the current date and time
  const getCurrentTimestamp = () => {
    const now = new Date();
    return `${now.toLocaleDateString()}, ${now.toLocaleTimeString()}`;
  };
  
  // Send message function
  const sendMessage = () => {
  if (newMessage.value.trim()) {
    const message = {
      id: Date.now(), // Każda wiadomość dostaje unikalny identyfikator
      text: newMessage.value,
      author: username.value,  // Pobieramy zalogowanego użytkownika z Keycloak
      timestamp: getCurrentTimestamp(),
      isSent: true,
      isImportant: isImportant.value,
    };

    socket.send(JSON.stringify(message));  // Wysyłamy pełny JSON przez WebSocket
    newMessage.value = '';
    isImportant.value = false;
    nextTick(scrollToBottom);
  }
};


  
  // Listen for incoming messages from WebSocket server
  socket.onmessage = (event) => {
  try {
    const receivedMessage = JSON.parse(event.data); // Parsujemy JSON

    // Sprawdzamy, czy już mamy wiadomość o tym samym ID
    if (!messages.value.some(msg => msg.id === receivedMessage.id)) {
      messages.value.push({
        id: receivedMessage.id,
        text: receivedMessage.text,
        author: receivedMessage.author || 'Anonimowy', // Pobieramy autora lub "Anonimowy"
        timestamp: receivedMessage.timestamp || getCurrentTimestamp(),
        isSent: receivedMessage.author === username.value, // Jeśli to nasza wiadomość, ustawiamy isSent
        isImportant: receivedMessage.isImportant || false,
      });
      nextTick(scrollToBottom);
    }
  } catch (error) {
    console.error('Błąd parsowania wiadomości:', error);
  }
};

  
  // WebSocket error handling
  socket.onerror = (error) => {
    console.error('WebSocket Error:', error);
  };
  
  // WebSocket close handling
  socket.onclose = () => {
    console.log('WebSocket connection closed');
  };
  
  onMounted(() => {
    scrollToBottom();
  });
  </script>
  
  <style scoped>
  .dupa {
    
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: calc(100vh - 150px);
  }
  
  .message-list {
    list-style: none;
    padding: 0;
    margin: 0;
    max-height: 60vh;
    overflow-y: auto;
  }
  
  .message-item {
    background: #f1f1f1;
    margin-bottom: 5px;
    padding: 10px;
    border-radius: 8px;
    max-width: 75%;
    word-wrap: break-word;
    width: fit-content;
  }
  
  .right-message {
    align-self: flex-end;
    background: linear-gradient(to top, #004aad, #0073ff);  /* Niebieski gradient */
    color: white;
    border-radius: 12px 12px 0 12px;
    text-align: left;
    margin-left: auto;
    max-width: 75%;
    width: fit-content;
  }
  
  .left-message {
    align-self: flex-start;
    background: linear-gradient(to top, #2c9d3b, #36d777);  /* Zielony gradient */
    color: white;
    border-radius: 12px 12px 12px 0;
    text-align: left;
    margin-right: auto;
    max-width: 75%;
    width: fit-content;
  }
  
  .message-header {
    font-size: 0.85em;
    color: white;
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
  }
  
  .message-author {
    font-weight: bold;
  }
  
  .message-time {
    font-style: italic;
    color: #ddd;
  }
  
  .important-label {
    background-color: red;
    color: white;
    padding: 2px 5px;
    font-size: 0.85em;
    border-radius: 5px;
    margin-bottom: 5px;
  }
  
  .message-text {
    word-wrap: break-word;
    width: fit-content;
  }
  
  .input-section {
    display: flex;
    align-items: center;
    position: sticky;
    bottom: 0;
    background: white;
    padding: 10px;
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    width: 100%;
  }
  
  .input-field {
    flex-grow: 1;
    margin-right: 10px;
  }
  
  .important-checkbox {
    margin-right: 10px;
    flex-grow: 0;
  }
  </style>
  