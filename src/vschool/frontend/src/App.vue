<template>
  <div class="search-container">
    <input v-model="searchQuery" placeholder="Search For Course..." class="search-input" />
    <button class="search-btn" @click="searchCourse()">
      <!-- Inline magnifier SVG -->
      <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M21 21l-4.35-4.35M10 18a8 8 0 100-16 8 8 0 000 16z" />
      </svg>
    </button>
  </div>

  <div class="map-container">
    <svg viewBox="0 0 30 20" class="map-svg">
      <!-- Background image -->
      <image href="./assets/map.png" x="0" y="0" width="30" height="20" />

      <!-- Interactive regions -->
      <path v-for="(region, index) in regions" :key="index" :d="region.path" class="map-region"
        :class="{ hovered: hoveredRegion === index }" @mouseover="hoveredRegion = index"
        @mouseleave="hoveredRegion = null" @click="selectRegion(index + 1)" />
    </svg>

  </div>

  <Teleport to="body">
    <Building v-if="selectedRegion" :buildingName="selectedRegion" @close="selectedRegion = null" />
  </Teleport>

  <Teleport to="body">
    <Course v-if="showSearchResults" :courseName="searchQuery" @close="showSearchResults = false" />
  </Teleport>

</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Building from "./components/building.vue"
import Course from "./components/course.vue"

const hoveredRegion = ref(null)
const selectedRegion = ref(null)
const searchQuery = ref(null)
const showSearchResults = ref(false)
const regions = [
  {
    path: "M19.6 14 21.5 13.9 21.6 15.7 19.67 15.75 Z", // Example square
    buildingName: "二教",
  },

]

function selectRegion(regionIdx) {
  console.log("Selected region", regionIdx)
  selectedRegion.value = regions[regionIdx - 1].buildingName
}

function searchCourse() {
  console.log("Searching for", searchQuery.value)
  showSearchResults.value = true
}


</script>


<style scoped>
.map-container {
  position: relative;
  width: 60vw;
  aspect-ratio: 3 / 2;
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

.search-container {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: flex;
  align-items: center;
  background-color: white;
  border-radius: 999px;
  padding: 0.5rem 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.search-input {
  border: none;
  outline: none;
  padding: 0.4rem;
  font-size: 1.1rem;
  border-radius: 999px;
  background: transparent;
}

.search-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
}

.icon {
  width: 30px;
  height: 30px;
  color: #333;
}
</style>