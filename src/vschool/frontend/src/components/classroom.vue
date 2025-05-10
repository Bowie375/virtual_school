<template>
  <div class="overlay">
    <div class="info-box">
      <table class="info-table">
        <caption>{{ classroomName }}</caption>
        <thead>
          <tr>
            <th>Time</th>
            <th>Course Name</th>
            <th>Teacher</th>
            <th>Department</th>
            <th>Class</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(course, index) in schedule" :key="index">
            <td>
              {{ TimeZones[index] }}
              <span class="status-indicator" :class="{ active: course !== null }"></span>
            </td>
            <td>{{ course ? course.course_name : '' }}</td>
            <td>{{ course ? course.teacher : '' }}</td>
            <td>{{ course ? course.department : '' }}</td>
            <td>{{ course ? course.class_id : '' }}</td>
          </tr>
        </tbody>
      </table>
      <button class="close-btn" @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// Define props
const props = defineProps({
  courseInfos: {
    type: Array,
    required: true,
  },
  classroomName: {
    type: String,
    required: true,
  },
})

// Reactive schedule array
const schedule = ref(Array(12).fill(null))

// Time zones
const TimeZones = [
  "8:00-8:50", "9:00-9:50", "10:10-11:00", "11:10-12:00",
  "13:00-13:50", "14:00-14:50", "15:10-16:00", "16:10-17:00",
  "17:10-18:00", "18:40-19:30", "19:40-20:30", "20:40-21:30",
]

// Watch for courseInfos updates
watch(
  () => props.courseInfos,
  (newVal) => {
    if (!Array.isArray(newVal)) return

    schedule.value = Array(12).fill(null)
    newVal.forEach(course => {
      for (let i = course.start_time; i <= course.end_time; i++) {
        schedule.value[i-1] = {
          course_name: course.course_name,
          teacher: course.teacher,
          department: course.department,
          class_id: course.class_id,
        }
      }
    })
  },
  { immediate: true }
)
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  backdrop-filter: blur(12px);
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.info-box {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2rem;
  width: 80vw;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.title {
  margin-bottom: 1rem;
  text-align: center;
  font-size: 2rem;
  color: #42b983;
}


.info-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Segoe UI', sans-serif;
  font-size: 1rem;
  color: #333;
}

.info-table caption {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: bold;
  color: #2c3e50;
}

.info-table th,
.info-table td {
  border: 1px solid #ddd;
  padding: 0.75rem 1rem;
  text-align: center;
}

.info-table thead {
  background-color: #42b883;
  color: white;
}

.status-indicator {
  display: inline-block;
  margin-left: 8px;
  width: 12px;
  height: 12px;
  border-radius: 3px;
  background-color: #ccc;
}

.status-indicator.active {
  background-color: #42b883;
}

.close-btn {
  display: block;
  margin: 0 auto;
  padding: 0.6rem 1.5rem;
  background-color: #ff5555;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.close-btn:hover {
  background-color: #cc0000;
}
</style>