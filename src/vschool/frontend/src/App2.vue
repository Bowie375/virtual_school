<template>
    <div class="map-container">
      <svg viewBox="0 0 30 20" class="map-svg">
        <!-- Background image -->
        <image href="./assets/map.png" x="0" y="0" width="30" height="20" />
  
        <!-- Interactive regions -->
        <path
          v-for="(region, index) in regions"
          :key="index"
          :d="region.path"
          class="map-region"
          :class="{ hovered: hoveredRegion === index }"
          @mouseover="hoveredRegion = index"
          @mouseleave="hoveredRegion = null"
          @click="selectRegion(index + 1)"
        />
      </svg>
  
      <classroom
        v-if="selectedRegion"
        :courseInfos="regionInfo[0]"
        :classroomName="regionInfo[1]"
        @close="selectedRegion = null"
      />
    </div>
  </template>
  
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import classroom from "./components/classroom.vue"
  
  const hoveredRegion = ref(null)
  const selectedRegion = ref(null)
  const regionInfo = ref([])
  
  const regions = [
    {
      path: "M19.6 14 21.5 13.9 21.6 15.7 19.67 15.75 Z", // Example square
      building_name: "二教211",
    },
  
    // Add more real region shapes based on your map
  ]
  
  const fetchData = async (location, week, weekday) => {
    try {
      const response = await axios.get(`http://localhost:5000/classroom/${location}/${week}/${weekday}`)
      return response.data
    } catch (err) {
      console.error('Failed to fetch data:', err)
      return null
    }
  }
  
  async function selectRegion(regionIdx) {
    let location = regions[regionIdx-1].building_name
    let res = await fetchData(location, 1, 1)  
    if (res === null) {
      console.error('Failed to fetch data for region', regionIdx)
    } else {
      regionInfo.value = [res, location]
      selectedRegion.value = regionIdx
      console.log(res, selectedRegion.value)
    }
  }
  
  </script>
  
  
  <style scoped>
  .map-container {
    position: relative;
    width: 60vw;
    aspect-ratio: 3 / 2;
    overflow: hidden;
  }
  
  .map-svg {
    width: 100%;
    height: auto;
    display: block;
  }
  
  .map-region {
    fill: transparent;
    stroke: #ffcc00;
    stroke-width: 0;
    cursor: pointer;
    transition: fill 0.3s ease;
  }
  
  .map-region.hovered {
    fill: rgba(255, 255, 0, 0.3);
  }
  </style>
  
  