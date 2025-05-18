<template>
  <div class="overlay">
    <div class="modal">
      <div class="modal-header">
        <h2>🔍 {{ courseName }}</h2>
        <button class="close-btn" @click="$emit('close')">✖</button>
      </div>

      <div v-if="loading" class="loading">Loading...</div>
      <div v-else-if="courses.length === 0" class="no-results">
        No courses found for "{{ courseName }}"
      </div>

      <div class="course-list" v-else>
        <div 
          class="course-card" 
          v-for="(c, index) in courses"
          :key="index"
          @click="toggleExpanded(index)"
          :class="{ expanded: expandedIndex === index }"
        >
          <div class="summary">
            <h3>📘 Class ID: {{ c.course.course_name }} - {{ c.course.class_id }} 班</h3>
            <p><strong>Teacher:</strong> {{ c.course.teacher }}</p>
            <p><strong>Department:</strong> {{ c.course.department }}</p>
          </div>

          <transition name="fade-slide">
            <div class="details" v-if="expandedIndex === index"> 
              <p class="details-header">📅 Schedules:</p>
              <ul v-if="c.schedule.length > 0">
                <li v-for="(s, i) in c.schedule" :key="i">
                  <span class="location">{{ s.location }}</span> — 
                  <span class="time">{{ s.time }}</span>
                </li>
              </ul>
              <div v-else class="no-schedule">
                ❗No schedule information found
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Define props
const props = defineProps({
  courseName: {
    type: String,
    required: true,
  },
})
defineEmits(['close'])

const courses = ref([])
const loading = ref(true)
const expandedIndex = ref(null)

function toggleExpanded(index) {
  expandedIndex.value = expandedIndex.value === index ? null : index
}

onMounted(async () => {
  try {
    const res = await axios.get(`http://localhost:5000/course/search?course_name=${encodeURIComponent(props.courseName)}`)
    courses.value = res.data || []
  } catch (err) {
    console.error('Search failed:', err)
    courses.value = []
  } finally {
    console.log('Search results:', courses.value)
    loading.value = false
  }
})
</script>

<style scoped>
/* Overlay */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* Modal */
.modal {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 2rem;
  width: 80%;
  max-width: 850px;
  max-height: 80vh;
  overflow-y: auto;
  backdrop-filter: blur(14px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  color: #fff;
  font-family: 'Segoe UI', sans-serif;
}

/* Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}
.modal-header h2 {
  font-size: 1.8rem;
}
.close-btn {
  font-size: 1.5rem;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  transition: transform 0.2s;
}
.close-btn:hover {
  transform: scale(1.2);
}

/* States */
.loading,
.no-results {
  text-align: center;
  font-size: 1.2rem;
  color: #eee;
}

/* Course cards */
.course-list {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.course-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem 1.5rem;
  border-radius: 18px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.25);
  border-left: 4px solid #8be9fd;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.3s ease;
}
.course-card:hover {
  background: rgba(255, 255, 255, 0.18);
  transform: scale(1.01);
}
.course-card h3 {
  color: #ffd866;
  font-size: 1.2rem;
  margin: 0 0 0.5rem;
}
.course-card p {
  margin: 0.3rem 0;
}
.details {
  margin-top: 1rem;
  border-top: 1px dashed rgba(255, 255, 255, 0.3);
  padding-top: 0.7rem;
}
.details-header {
  font-weight: 600;
  color: #f1fa8c;
  margin-bottom: 0.5rem;
}
.details ul {
  list-style: none;
  padding-left: 0;
  font-size: 0.95rem;
}
.details li {
  margin: 0.2rem 0;
}
.details .location {
  font-weight: bold;
  color: #8be9fd;
}
.details .time {
  color: #f8f8f2;
}

.no-schedule {
  font-style: italic;
  color: #ff79c6;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border-left: 4px solid #ff79c6;
  box-shadow: 0 2px 5px rgba(255, 121, 198, 0.2);
  margin-top: 0.5rem;
}

/* Animation */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
