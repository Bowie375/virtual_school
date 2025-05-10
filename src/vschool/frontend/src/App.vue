<template>
  <div class="map-container">
    <img src="./assets/map.png" class="map-image" />
    <div v-for="(region, index) in regions" :key="index" class="map-region" :style="region.style"
      @mouseover="hoveredRegion = index" @mouseleave="hoveredRegion = null" @click="selectRegion(index+1)"
      :class="{ hovered: hoveredRegion === index }"></div>

    <classroom v-if="selectedRegion" :courseInfos="regionInfo[0]" :classroomName="regionInfo[1]" @close="selectedRegion = null" />
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
  { style: { top: '0%', left: '0%' }, building_name: "二教211" },
  { style: { top: '0%', left: '33%' } , building_name: "三教103"},
  { style: { top: '0%', left: '66%' } , building_name: "二教101"},
  { style: { top: '33%', left: '0%' } , building_name: "二教101"},
  { style: { top: '33%', left: '33%' }, building_name: "二教101" },
  { style: { top: '33%', left: '66%' }, building_name: "二教101" },
  { style: { top: '66%', left: '0%' } , building_name: "二教101"},
  { style: { top: '66%', left: '33%' }, building_name: "二教101" },
  { style: { top: '66%', left: '66%' }, building_name: "二教101" },
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
  aspect-ratio: 3 / 2;
  width: 60vw;
  height: auto;
  /* let aspect-ratio control height */
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
