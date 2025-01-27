<template>
    
    <div v-if="isVisible" class="bg-white p-6 rounded-lg shadow-md max-w-screen-sm mt-6" :style="{ width: '100%' }">


        <!-- Jeśli wiadomość jest dostępna, pokazujemy editor, w przeciwnym przypadku komunikat -->
        <div v-if="message" class="card mb-7">
            <Editor v-model="fullMessage"
                editorStyle="width: 100%; height: 480px; font-family: 'Roboto', sans-serif; font-size: 18px;" />
        </div>
        <div v-else class="text-center py-4 text-gray-600">
            <p class="text-xl">Kliknij, aby otworzyć wiadomość</p>
        </div>

        <!-- Przycisk zamykania -->
        <div class="mt-6 text-right">

            <Button label="Send Message" icon="pi pi-paper-plane" @click="closeMessageDetails" class="p-mr-2" />
        </div>
    </div>

</template>

<script setup>
import { defineProps, defineEmits, ref, watchEffect } from 'vue';
import Editor from 'primevue/editor';
import Button from 'primevue/button';
import ScrollPanel from 'primevue/scrollpanel';

// Props
const props = defineProps({
    message: {
        type: Object,
        required: true
    },
    isVisible: {
        type: Boolean,
        required: true
    }
});

// Emitowanie zdarzenia do zamknięcia komponentu
const emit = defineEmits(['close']);

// Reaktywna zmienna do przechowywania pełnej wiadomości
const fullMessage = ref('');

// Ustawienie pełnej treści wiadomości, aby była dostępna w Editorze
watchEffect(() => {
    if (props.message) {
        fullMessage.value = `
        <strong>Temat:</strong> ${props.message.subject || 'Brak tematu'}<br>
        <strong>Wysłane przez:</strong> ${props.message.sender || 'Nieznany nadawca'}<br>
        <strong>Data:</strong> ${props.message.date || 'Nieznana data'}<br><br>
        <strong>Treść:</strong><br>
        ${props.message.body || 'Brak treści'}
      `;
    } else {
        fullMessage.value = '';
    }
});

// Funkcja do zamknięcia szczegółów wiadomości
const closeMessageDetails = () => {
    emit('close');  // Emituje zdarzenie 'close', aby zamknąć szczegóły
};
</script>


<style></style>