<script setup>
import { ref } from 'vue';
import axios from 'axios';
import  Toast  from 'primevue/toast';
import  Button  from 'primevue/button';
import InputText from 'primevue/inputtext';
import  { useToast }from 'primevue/usetoast';
import Messages  from 'primevue/message';

// Stany formularza
const rank = ref('');
const lastName = ref('');
const firstName = ref('');
const militaryUnit = ref('');
const generatePGP = ref(false);

// Stany do wyświetlania komunikatów
const toast = useToast();
const messages = ref([]);

// Funkcja do generowania kluczy PGP
const handleGenerateKeys = async () => {
  // Walidacja formularza
  if (!rank.value || !lastName.value || !firstName.value || !militaryUnit.value) {
    messages.value.push({
      severity: 'error',
      summary: 'Błąd',
      detail: 'Wszystkie pola muszą być wypełnione.',
    });
    return;
  }

  // Przekazujemy dane do API, aby wygenerować parę kluczy PGP
  try {
    const response = await axios.post('http://127.0.0.1:8000/generate-pgp-keys', {
      rank: rank.value,
      lastName: lastName.value,
      firstName: firstName.value,
      militaryUnit: militaryUnit.value,
    });

    const keys = response.data; // Zakładając, że API zwraca wygenerowane klucze

    toast.add({
      severity: 'success',
      summary: 'Sukces',
      detail: 'Para kluczy PGP została wygenerowana!',
    });

    console.log(keys); // Możesz tutaj użyć kluczy w zależności od formatu, np. wyświetlić je lub zapisać

  } catch (error) {
    console.error('Błąd podczas generowania kluczy PGP:', error);
    toast.add({
      severity: 'error',
      summary: 'Błąd',
      detail: 'Nie udało się wygenerować kluczy PGP.',
    });
  }
};
</script>

<template>
  <div class="user-form">
    <!-- Komponent Toast do wyświetlania powiadomień -->
    <Toast position="top-right" />

    <!-- Wiadomości o błędach -->
    <Messages :value="messages" />

    <h2>Twój formularz użytkownika</h2>
    <p>Wprowadź swoje dane i wygeneruj parę kluczy PGP.</p>

    <div class="form-container">
      <!-- Stopień -->
      <div class="form-field">
        <label for="rank">
          <i class="pi pi-tag"></i> Stopień
        </label>
        <InputText id="rank" v-model="rank" placeholder="Wpisz stopień" />
      </div>

      <!-- Nazwisko -->
      <div class="form-field">
        <label for="lastName">
          <i class="pi pi-user"></i> Nazwisko
        </label>
        <InputText id="lastName" v-model="lastName" placeholder="Wpisz nazwisko" />
      </div>

      <!-- Imię -->
      <div class="form-field">
        <label for="firstName">
          <i class="pi pi-user-plus"></i> Imię
        </label>
        <InputText id="firstName" v-model="firstName" placeholder="Wpisz imię" />
      </div>

      <!-- Jednostka wojskowa -->
      <div class="form-field">
        <label for="militaryUnit">
          <i class="pi pi-building"></i> Jednostka wojskowa
        </label>
        <InputText id="militaryUnit" v-model="militaryUnit" placeholder="Wpisz jednostkę wojskową" />
      </div>

      <!-- Przycisk generowania kluczy PGP -->
      <Button label="Generuj parę kluczy PGP" icon="pi pi-key" @click="handleGenerateKeys" />
    </div>
  </div>
</template>

<style scoped>
/* Stylizacja formularza */
.user-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.form-container {
  display: flex;
  flex-direction: column;
}

.form-field {
  margin-bottom: 20px;
}

.form-field label {
  font-weight: bold;
}

.form-field i {
  margin-right: 8px;
}

button {
  margin-top: 20px;
}
</style>
