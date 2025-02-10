<template>
    <div>
      <FullCalendar 
        :plugins="calendarPlugins"
        :initialView="'dayGridMonth'"
        :events="calendarEvents"
        :eventClick="handleEventClick"
      />
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import FullCalendar from '@fullcalendar/vue';
  import dayGridPlugin from '@fullcalendar/daygrid';
  import interactionPlugin from '@fullcalendar/interaction';
  
  const calendarPlugins = [dayGridPlugin, interactionPlugin];
  
  const calendarEvents = ref([
    { title: 'Meeting with John', start: '2025-02-10T10:00:00' },
    { title: 'Team Workshop', start: '2025-02-11T12:30:00' },
    { title: 'Conference', start: '2025-02-15T09:00:00' },
  ]);
  
  const handleEventClick = (info) => {
    alert('Event clicked: ' + info.event.title);
  };
  </script>
  
  <style scoped>
  /* Dodaj dodatkowy styl, jeśli chcesz */
  </style>
  