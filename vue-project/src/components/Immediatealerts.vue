<template>
  <div class="p-4">
    <Toast ref="toast" position="bottom-right" />

    <Fieldset legend="Immediate Alerts" toggleable>
      <template #legend>
        <span class="text-xl font-bold">Immediate Alerts Control</span>
      </template>
      <p class="text-sm text-gray-600 mb-4">
        Use this panel to activate or deactivate immediate alerts such as Air Raid, NBC Alerts, and Ground Attacks.
        Select an alert from the dropdown and activate it to notify all users.
      </p>

      <div class="flex gap-8 items-center mb-8">
        <Dropdown 
          v-model="selectedAlert" 
          :options="alertOptions" 
          optionLabel="label" 
          placeholder="Select an Alert" 
          class="w-60"
        />

        <Button 
          label="Activate" 
          icon="pi pi-check" 
          class="p-button-danger" 
          @click="activateAlert"
        />

        <Button 
          label="Deactivate" 
          icon="pi pi-times" 
          class="p-button-success" 
          @click="deactivateAlert"
        />
      </div>

      <div v-if="currentAlert" class="p-4 bg-red-500 text-white rounded">
        <strong>Active Alert:</strong> ALERT: {{ currentAlert }}
      </div>
    </Fieldset>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import Fieldset from 'primevue/fieldset';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';
import Toast from 'primevue/toast';

export default {
  components: { Fieldset, Dropdown, Button, Toast },
  setup() {
    const selectedAlert = ref('');
    const currentAlert = ref(null);
    const toast = ref(null);
    let socket = null;

    const alertOptions = [
      { label: 'Air Raid', value: 'Air Raid' },
      { label: 'NBC Alert', value: 'NBC Alert' },
      { label: 'Ground Attack', value: 'Ground Attack' },
      { label: 'Other Threat', value: 'Other Threat' },
    ];

    const showToast = (message, severity) => {
      toast.value.add({ severity, summary: 'Alert Update', detail: message, life: 5000 });
    };

    const activateAlert = () => {
      if (!selectedAlert.value) {
        showToast('Please select an alert type.', 'warn');
        return;
      }

      const alertLabel = selectedAlert.value.label || selectedAlert.value; // Use 'label' if the object is selected

      fetch('http://192.168.178.73:8000/send-alert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ alert: alertLabel }),
      })
        .then(response => response.json())
        .then(data => showToast(`Alert activated: ${data.message}`, 'error'))
        .catch(() => showToast('Error activating alert.', 'error'));
    };

    const deactivateAlert = () => {
      fetch('http://192.168.178.73:8000/send-alert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ alert: null }),
      })
        .then(response => response.json())
        .then(data => showToast(`Alert deactivated: ${data.message}`, 'success'))
        .catch(() => showToast('Error deactivating alert.', 'error'));
    };

    const handleIncomingMessage = (message) => {
      const alertMessage = message.data.includes('Alert deactivated')
        ? null
        : message.data.replace('Alert: ', '').toUpperCase(); // Display in uppercase

      currentAlert.value = alertMessage;
    };

    const setupWebSocket = () => {
      socket = new WebSocket('ws://192.168.178.73:8000/ws');
      socket.onopen = () => console.log('WebSocket connected');
      socket.onmessage = handleIncomingMessage;
      socket.onclose = () => console.log('WebSocket disconnected');
    };

    onMounted(() => {
      setupWebSocket();
    });

    return {
      selectedAlert,
      currentAlert,
      alertOptions,
      activateAlert,
      deactivateAlert,
      toast
    };
  }
};
</script>

<style scoped>
.alert-banner {
  background-color: rgb(62, 64, 142);
  color: white;
  text-align: center;
  padding: 1rem;
  font-weight: bold;
  font-size: 2.2rem;
}

.p-button-danger {
  margin: 10px;
}

.p-select {
  width: 70%;
}
</style>
