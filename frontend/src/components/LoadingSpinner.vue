<script setup>
defineProps({
  message: { type: String, default: 'Loading...' }
})
</script>

<template>
  <div class="tma-loading">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <p>{{ message }}</p>
  </div>
</template>
