<template>
    <div class="about-us">
      <h1>O nas</h1>
      <p>Witamy na naszej stronie! Tutaj znajdziesz informacje o naszej firmie.</p>
      <div class="draggable-container">
        <div v-for="(item, index) in items" :key="item.id" 
             draggable="true" 
             @dragstart="dragStart(index)" 
             @dragover.prevent 
             @drop="drop(index)" 
             class="draggable-item">
          {{ item.text }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "AboutUs",
    data() {
      return {
        items: [
          { id: 1, text: "Element 1" },
          { id: 2, text: "Element 2" },
          { id: 3, text: "Element 3" }
        ],
        draggedItemIndex: null,
      };
    },
    methods: {
      dragStart(index) {
        this.draggedItemIndex = index;
      },
      drop(index) {
        const movedItem = this.items.splice(this.draggedItemIndex, 1)[0];
        this.items.splice(index, 0, movedItem);
        this.draggedItemIndex = null;
      }
    }
  };
  </script>
  
  <style scoped>
  .about-us {
    text-align: center;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .draggable-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px;
  }
  
  .draggable-item {
    width: 200px;
    padding: 10px;
    margin: 5px;
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 5px;
    cursor: grab;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  </style>
  