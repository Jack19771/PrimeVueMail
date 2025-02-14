<template>
    <div class="chat-container">
      <Card class="chat-card">
        <template #content>
          <div class="response-container">
            <h4>AI Answer</h4>
            <Divider />
            <div v-if="loading" class="loading-indicator">
              <ProgressSpinner />
            </div>
           
            <div class="chat-messages" v-if="response" v-html="response"></div>
        
          </div>
  
          <form @submit.prevent="sendMessage" class="chat-input-container">
            <div class="p-inputgroup chat-input-group">
              <InputText v-model="topic" placeholder="Type your question..." class="chat-input" />
              <Button type="submit" label="Ask" :disabled="loading" icon="pi pi-send" class="send-button" style="padding-left: 10px;"/>
            </div>
          </form>
        </template>
      </Card>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  import Button from 'primevue/button';
  import InputText from 'primevue/inputtext';
  import ProgressSpinner from 'primevue/progressspinner';
  import Divider from 'primevue/divider';
  import Card from 'primevue/card';

  
  export default {
    components: { Card, Button, InputText, ProgressSpinner, Divider },
    setup() {
      const topic = ref('');
      const response = ref(null);
      const loading = ref(false);
  
      const sendMessage = async () => {
        if (!topic.value) return;
        loading.value = true;
        response.value = null;
  
        try {
          const res = await fetch('http://localhost:4000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic: topic.value })
          });
          const data = await res.json();
          response.value = data.response;
        } catch (error) {
          console.error('Error:', error);
        } finally {
          loading.value = false;
        }
      };
  
      return { topic, response, loading, sendMessage };
    }
  };
  </script>
  
  <style>
  .chat-container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 80vh;
    width: 150vh;
    padding: 10px;
    
    
    
  }
  .chat-card {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    max-width: 100%;
    height: 100%;
    background-color: #f9f9f9;
  }
  .response-container {
    flex-grow: 1;
    overflow-y: auto;
    padding: 10px;
    height: 80%;
  }
  .chat-messages {
    max-height: 75vh;
    overflow-y: auto;
    padding: 10px;
    white-space: pre-wrap;
    font-size: medium;
  }
  .loading-indicator {
    display: flex;
    justify-content: center;
    margin-top: 10px;
  }
  .chat-input-container {
    padding: 10px;
    background: white;
  }
  .chat-input-group {
    width: 100%;
  }
  .chat-input {
    flex-grow: 1;
    width: 90%;
  }
  </style>
  