<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import TieredMenu from 'primevue/tieredmenu';

const menuItems = ref([]);  // Będzie zawierać dane z API
const errorMessage = ref('');  // Zmienna do przechowywania komunikatu o błędzie

// Funkcja do pobierania danych z API
const fetchMenuData = async () => {
  try {
    // Resetujemy komunikat o błędzie przed każdą próbą pobrania danych
    errorMessage.value = '';
    
    const response = await axios.get('https://jsonplaceholder.typicode.com/users');  // Przykład API
    const data = response.data;

    // Zbudowanie menu na podstawie pobranych danych
    menuItems.value = data.map((user) => ({
      label: user.name,
      icon: 'pi pi-user',
      items: [
        {
          label: 'Details',
          command: () => { console.log(`${user.name} Details clicked`); },
        },
        {
          label: 'Settings',
          command: () => { console.log(`${user.name} Settings clicked`); },
        },
      ],  // Zagnieżdżone menu dla każdego użytkownika
    }));
  } catch (error) {
    // Ustawienie komunikatu o błędzie, jeśli nie udało się pobrać danych
    console.error('Błąd podczas pobierania danych:', error);
    errorMessage.value = 'NO PEERS AVAILABLE AT THE MOMENT.';
  }
};

// Wywołanie fetchMenuData przy załadowaniu komponentu i ustawienie interwału na każdą minutę
onMounted(() => {
  fetchMenuData();  // Pierwsze pobranie danych
  setInterval(fetchMenuData, 10000);  // Pobiera dane co minutę
});
</script>

<style scoped>
/* Stylizacja kontenera Sidebar, aby był na stałe po lewej stronie */
.sidebar-container {
  position: fixed;  /* Ustawienie nawigacji w stałej pozycji */
  top: 5;
  left: 0;
  width: 240px;  /* Ustawiamy szerokość paska bocznego */
  height: 100vh;  /* Ustawiamy wysokość na 100% ekranu */
  background-color: transparent;
  z-index: 1000;
  padding-top: 20px;
  padding-left: 20px;
}

h3 {
  margin: 10px 0;
}

.error-message {
  color: red;
  font-size: 1rem;
  margin-top: 10px;
}
</style>

<template>
  <div class="sidebar-container">
    <!-- Wyświetlenie komunikatu o błędzie, jeśli wystąpił -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    
    <!-- Komponent TieredMenu z danymi z API -->
    <TieredMenu :model="menuItems" />
  </div>
</template>
