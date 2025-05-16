<template>
  <div class="region-detail-container">
    <img :src="getImage(buildingName)" class="background-image" @click="showTable = true" />

    <div class="floors-table" v-if="showTable">
      <div class="header">
        <h2>教室占用表</h2>
      </div>

      <div class="select-bar">
        <label>
          Week:
          <select v-model="selectedWeek">
            <option value="Today">Today</option>
            <option v-for="w in 5" :key="w" :value="w">{{ w }}</option>
          </select>
        </label>
        <label>
          Weekday:
          <select v-model="selectedWeekday">
            <option value="Today">Today</option>
            <option v-for="(d, i) in weekdays" :key="i" :value="d">{{ d }}</option>
          </select>
        </label>
      </div>

      <table>
        <thead>
          <tr>
            <th>Floor</th>
            <th>Classrooms</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(floor, index) in buildingFloors[buildingName]" :key="index">
            <td class="floor-cell">{{ floor.name }}</td>
            <td class="room-cell">
              <div class="room-buttons">
                <button class="classroom-btn" v-for="room in floor.rooms" :key="room" @click="goToClassroom(room)">
                  {{ room }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="close-container">
        <button class="close-btn" @click="showTable = false">Close</button>
      </div>
    </div>


    <div class="back-arrow" @click="$emit('close')">
      ← Go Back <!-- Unicode left arrow -->
    </div>

    <classroom v-if="selectedClassroom" 
      :courseInfos="classroomInfo[0]" 
      :classroomName="classroomInfo[1]"
      @close="selectedClassroom = null" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import classroom from './classroom.vue'

const props = defineProps({
  buildingName: String,
})

const emit = defineEmits(['close'])
const showTable = ref(true)
const buildingFloors = {
  "二教": [ { name: "1st Floor", rooms: ["101", "102", "105", "106", "107", "109"] },
            { name: "2nd Floor", rooms: ["202", "203", "205", "206", "207", "210", "211"] },
            { name: "3nd Floor", rooms: ["302", "304", "306", "307", "308", "309", "311", "313", "314", "315", "316", "317", "318", "319"] },
            { name: "4nd Floor", rooms: ["401", "402", "403", "404", "405", "406", "407", "408", "410", "411", "412", "413", "414", "415", "416", "420", "421", "422", "423", "424", "425"] },
            { name: "5nd Floor", rooms: ["501", "503", "505", "506", "507", "508", "509", "510", "511", "512", "513", "514", "515", "516", "517", "518", "519", "521", "523", "524", "525", "526", "527", "528", "529", "530"] },
          ],
}
const selectedWeek = ref('Today')
const selectedWeekday = ref('Today')
const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
const selectedClassroom = ref(null)
const classroomInfo = ref([])

const images = import.meta.glob('../assets/*.png', { eager: true })
const getImage = (name) => images[`../assets/${name}.png`]?.default || images['../assets/default.png'].default

const fetchData = async (location, week, weekday) => {
  try {
    const response = await axios.get(`http://localhost:5000/classroom/${location}/${week}/${weekday}`)
    return response.data
  } catch (err) {
    console.error('Failed to fetch data:', err)
    return null
  }
}

async function goToClassroom(roomId) {
  let location = props.buildingName + roomId
  let week = selectedWeek.value
  if (selectedWeek.value === 'Today') {
    week = 1
  }
  let weekday = 1
  if (selectedWeekday.value === 'Today') {
    const today = new Date()
    weekday = -today.getDay() + 7
  } else {
    weekday = weekdays.indexOf(selectedWeekday.value) + 1
  }

  let res = await fetchData(location, week, weekday)
  classroomInfo.value = [res, location]
  selectedClassroom.value = roomId
  console.log(res, selectedClassroom.value)
}

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

.select-bar {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.select-bar select {
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 0.5rem;
}

th {
  text-align: center;
  padding-bottom: 0.5rem;
  font-weight: bold;
  font-size: 1.1rem;
}

.floor-cell {
  width: 20%;
  font-weight: bold;
  text-align: center;
}

.room-cell {
  text-align: left;
}

.room-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.classroom-btn {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 0.8rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.classroom-btn:hover {
  background-color: #2980b9;
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

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th,
td {
  padding: 0.8rem;
  border-bottom: 1px solid #ccc;
}

.classroom-btn {
  margin: 0.3rem;
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.classroom-btn:hover {
  background-color: #2563eb;
}
</style>