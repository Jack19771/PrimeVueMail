<template>
    <div>
      <vue-cal
        :events="events"
        @dayclick="onDayClick"
      />
    </div>
  </template>
  
  <script>
  import VueCal from 'vue-cal';
  import 'vue-cal/dist/vuecal.css';
  
  export default {
    components: { VueCal },
    data() {
      return {
        events: [
          { start: '2025-02-14 13:00', end: '2025-02-14 14:00', title: 'FastTrack2' }
        ]
      };
    },
    methods: {
      onDayClick(day) {
        console.log('Clicked on day: ', day);
      }
    }
  };
  </script>
  