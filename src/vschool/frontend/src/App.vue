<template>
  <div class="map-container">
    <img src="./assets/map.png" class="map-image" />
    <div
      v-for="(region, index) in regions"
      :key="index"
      class="map-region"
      :style="region.style"
      @mouseover="hoveredRegion = index"
      @mouseleave="hoveredRegion = null"
      :class="{ hovered: hoveredRegion === index }"
    ></div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const hoveredRegion = ref(null)
const regions = [
  // Example: divide image into 3x3 grid with 33% width and height
  { style: { top: '0%', left: '0%' } },
  { style: { top: '0%', left: '33%' } },
  { style: { top: '0%', left: '66%' } },
  { style: { top: '33%', left: '0%' } },
  { style: { top: '33%', left: '33%' } },
  { style: { top: '33%', left: '66%' } },
  { style: { top: '66%', left: '0%' } },
  { style: { top: '66%', left: '33%' } },
  { style: { top: '66%', left: '66%' } },
]
</script>

<style scoped>
.map-container {
  position: relative;
  aspect-ratio: 3 / 2;
  width: 60vw;
  height: auto; /* let aspect-ratio control height */
  overflow: hidden;
}
.map-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.map-region {
  position: absolute;
  width: 33.3%;
  height: 33.3%;
  transition: all 0.3s ease;
}
.map-region.hovered {
  box-shadow: 0 0 15px 5px rgba(255, 255, 0, 0.7);
  background-color: rgba(255, 255, 255, 0.0);
}
</style>

