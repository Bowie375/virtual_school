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
    <!-- Info Box -->
    <div v-if="hoveredRegion !== null" class="info-box">
      <h3>{{ regions[hoveredRegion].buildingName }}</h3>
      <p>{{ regions[hoveredRegion].description }}</p>
    </div>

    <svg viewBox="0 0 30 20" class="map-svg">
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

      <image
        v-for="(region, index) in regions"
        :key="index"
        :href="region.marker.href"
        :x="region.marker.x"
        :y="region.marker.y"
        :width="region.marker.w"
        :height="region.marker.h"
        class="map-marker"
      />

    </svg>
  </div>

  <div class="left-column">
    <a
      v-for="(item, index) in leftColumnItems"
      :key="index"
      :href="item.link"
      class="left-row"
      target="_blank"
      rel="noopener noreferrer"
    >
      {{ item.name }}
    </a>
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
const markerImages = import.meta.glob('./assets/*.gif', { eager: true, as: 'url' })
const regions = [
  {
    marker: {x:19.2, y:13.1, w:2, h:2, href:markerImages['./assets/marker.gif'] },
    path: "M 19.666 14.082 L 19.717 15.848 L 20.484 15.822 L 20.433 14.722 L 21.406 14.722 L 21.354 14.031 Z",
    buildingName: "二教",
    description: "第二教学楼"
  },
  {
    marker: {x:20.1, y:14.1, w:2., h:2., href:markerImages['./assets/marker.gif'] },
    path: "M 20.638 15.72 L 20.587 15.157 L 21.38 15.157 L 21.406 15.643 Z",
    buildingName: "三教",
    description: "第三教学楼"
  },
  {
    marker: {x:19.3, y:10.5, w:2., h:2., href:markerImages['./assets/marker.gif'] },
    path: "M19.6 11.5C20.1 11.1 20.4 11.2 20.8 11.15L20.833 12.299 19.597 12.31 Z",
    buildingName: "理教",
    description: "理科教学楼"
  },
  {
    marker: {x:12.5, y:6.5, w:2.5, h:2.5, href:markerImages['./assets/marker2.gif'] },
    path: "M 12.952 8.897 L 13.96 9.247 L 15.063 9.22 L 15.48 9.368 L 15.857 9.099 L 16.234 9.166 L 18.561 8.695 L 18.292 7.444 L 18.372 7.027 L 18.251 6.274 L 17.781 5.642 L 15.763 5.843 L 15.534 6.341 L 13.113 6.422 L 12.763 7.888 Z",
    buildingName: "未名湖",
    description: "未名湖"
  }
  // {
  //   marker: {x:10, y:10, w:2.5, h:2.5, href:markerImages['./assets/marker.gif'] },
  //   path: "M19.6 14 21.5 13.9 21.6 15.7 19.67 15.75 Z",
  //   buildingName: "二教",
  //   description: "第二教学楼"
  // },
]
const leftColumnItems = [
  {
    name: "校内门户",
    link: "https://portal.pku.edu.cn/"
  },
  {
    name: "北大教学网",
    link: "https://course.pku.edu.cn/"
  },
  {
    name: "北大树洞",
    link: "https://treehole.pku.edu.cn/"
  },
  {
    name: "北大BBS",
    link: "https://bbs.pku.edu.cn/"
  },
  {
    name: "课程测评",
    link: "https://courses.pinzhixiaoyuan.com/"
  },
]

function selectRegion(regionIdx) {
  console.log("Selected region", regionIdx)
  if(regionIdx < 4)
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
  stroke-width: 0;
}

.map-marker {
  pointer-events: none;
}

.info-box {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 1rem;
  max-width: 220px;
  color: #fff;
  font-family: 'Segoe UI', sans-serif;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.info-box h3 {
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
  color: rgba(213, 46, 46, 0.667);
  font-weight: 600;
}

.info-box p {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.4;
  color: rgba(93, 13, 13, 0.8);
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

.left-column {
  position: absolute;
  top: 0;
  left: 0;
  width: 220px;
  height: 100vh;
  background: linear-gradient(to bottom, #b52626, #ffcccc);
  display: flex;
  flex-direction: column;
  padding: 1.5rem 0;
  gap: 1rem;
  z-index: 5;
  box-shadow: 4px 0 16px rgba(0, 0, 0, 0.3);
}

/* Link row style */
.left-row {
  display: block;
  padding: 0.8rem 1.2rem;
  margin-left: 0;
  font-size: 1rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.88);
  text-decoration: none;
  border-radius: 0 1rem 1rem 0;
  background: rgba(255, 255, 255, 0.08);
  transition: 
    font-size 0.3s ease,
    transform 0.3s ease,
    margin-left 0.3s ease,
    background 0.3s ease,
    color 0.3s ease;
}

/* Hover effect: highlight the row */
.left-row:hover {
  font-size: 1.25rem;
  transform: scale(1.05);
  margin-left: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}
</style>