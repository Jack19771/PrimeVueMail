<template>
    <div>
      <vue-cal
        @dayclick="onDayClick"
      />
      <button @click="testButton">Kliknij tutaj (test)</button>
    </div>
  </template>
  
  <script>
  import VueCal from 'vue-cal';
  import 'vue-cal/dist/vuecal.css';
  
  export default {
    components: { VueCal },
    methods: {
      onDayClick(day) {
        console.log('Kliknięto dzień: ', day);
      },
      testButton() {
        console.log('Działa testowy button!');
      }
    }
  };
  </script>
  