<template>
    <div class="region-detail-container">
      <img :src="getImage(spotName)" class="background-image" @click="showTable = true" />
  
      <div class="floors-table" v-if="showTable">
        <div class="header">
          <h2>刹那光景</h2>
        </div>
 
  
        <carousel :spotName = props.spotName />
  
        <div class="close-container">
          <button class="close-btn" @click="showTable = false">Close</button>
        </div>
      </div>
  
  
      <div class="back-arrow" @click="$emit('close')">
        ←Back <!-- Unicode left arrow -->
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref, watch } from 'vue'
  import axios from 'axios'
  import carousel from "./carousel.vue"
  
  const props = defineProps({
    spotName: String,
  })
  
  const emit = defineEmits(['close'])
  const showTable = ref(true)
  
  const images = import.meta.glob('../assets/*.png', { eager: true })
  const getImage = (name) => images[`../assets/${name}.png`]?.default || images['../assets/default.png'].default
  
  
  </script>
  
  <style scoped>
  .region-detail-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 1000;
    overflow: hidden;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  .background-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 0;
    filter: brightness(0.7);
  }
  
  .floors-table {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    transform: translate(-50%, -50%);
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 16px;
    padding: 2rem;
    z-index: 2;
    max-width: 80vw;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    text-align: center;
  }
  
  .header h2 {
    margin-bottom: 1rem;
    font-size: 1.75rem;
  }
  
  

  

  
  
  
  .close-container {
    margin-top: 1rem;
  }
  
  .close-btn {
    background-color: #ff5e5e;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .close-btn:hover {
    background-color: #e04e4e;
  }
  
  
  .back-arrow {
    position: absolute;
    top: 20px;
    left: 20px;
    font-size: 2rem;
    color: white;
    cursor: pointer;
    z-index: 3;
    user-select: none;
    transition: transform 0.2s;
  }
  
  .back-arrow:hover {
    transform: scale(1.2);
  }
  </style>