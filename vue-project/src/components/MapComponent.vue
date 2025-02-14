<template>
    <div id="map" style="height: 80vh;"></div>
  </template>
  
  <script>
  import { onMounted } from 'vue';
  import L from 'leaflet';
  import 'leaflet/dist/leaflet.css';
  
  export default {
    name: 'MapComponent',
    setup() {
      onMounted(() => {
        // Inicjalizacja mapy
        const map = L.map('map').setView([52.505, 18.09], 13);
  
        // Dodanie warstwy kafelków z OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: '© OpenStreetMap'
        }).addTo(map);
      });
    }
  };
  </script>
  
  <style scoped>
  /* Upewnij się, że kontener mapy ma ustaloną wysokość */
  #map {
  height: 500px;
  width: 100%;
}
  </style>
  