<script setup>
import { ref } from 'vue'

const props = defineProps({
  trek: { type: Object, required: true }
})

defineEmits([])

const getDifficultyClass = (d) => {
  if (d === 'Easy') return 'badge-easy'
  if (d === 'Moderate') return 'badge-moderate'
  if (d === 'Hard') return 'badge-hard'
  return ''
}

const getStatusClass = (s) => {
  if (!s) return ''
  const sl = s.toLowerCase()
  if (sl === 'pending') return 'badge-pending'
  if (sl === 'approved') return 'badge-approved'
  if (sl === 'open') return 'badge-open'
  if (sl === 'closed') return 'badge-closed'
  if (sl === 'completed') return 'badge-completed'
  return ''
}

const formatDate = (d) => {
  if (!d) return 'N/A'
  return new Date(d).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>

<template>
  <div class="trek-card">
    <div class="trek-card-header">
      <div class="d-flex justify-content-between align-items-start mb-1">
        <h5 class="mb-0">{{ trek.trek_name }}</h5>
        <span class="badge-status ms-2 flex-shrink-0" :class="getStatusClass(trek.status)">{{ trek.status }}</span>
      </div>
      <div class="trek-location">
        <i class="bi bi-geo-alt-fill"></i>
        {{ trek.location }}
      </div>
    </div>
    <div class="trek-card-body">
      <div class="trek-meta">
        <div class="trek-meta-item">
          <span class="badge-status" :class="getDifficultyClass(trek.difficulty)">{{ trek.difficulty }}</span>
        </div>
        <div class="trek-meta-item" v-if="trek.available_slots !== undefined">
          <i class="bi bi-people-fill"></i>
          {{ trek.available_slots }} slots
        </div>
        <div class="trek-meta-item" v-if="trek.start_date">
          <i class="bi bi-calendar-event"></i>
          {{ formatDate(trek.start_date) }}
        </div>
        <div class="trek-meta-item" v-if="trek.end_date">
          <i class="bi bi-calendar-check"></i>
          {{ formatDate(trek.end_date) }}
        </div>
      </div>
      <!-- Action slot -->
      <slot name="actions"></slot>
    </div>
  </div>
</template>
