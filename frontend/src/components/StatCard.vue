<script setup>
defineProps({
  title: { type: String, required: true },
  value: { type: [Number, String], default: 0 },
  icon: { type: String, default: 'bar-chart' },
  color: { type: String, default: 'green' }
})
</script>

<template>
  <div class="stat-card" :class="`stat-${color}`">
    <div class="stat-icon">
      <i class="bi" :class="`bi-${icon}`"></i>
    </div>
    <div class="stat-value">{{ value }}</div>
    <div class="stat-label">{{ title }}</div>
  </div>
</template>
