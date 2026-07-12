<script setup>
import { ref } from 'vue'

defineProps({
  menuItems: {
    type: Array,
    required: true
    // Each item: { label, icon, route }
  },
  title: {
    type: String,
    default: 'Navigation'
  }
})

const isOpen = ref(false)

const toggle = () => {
  isOpen.value = !isOpen.value
}

const closeSidebar = () => {
  isOpen.value = false
}

defineExpose({ toggle, closeSidebar })
</script>

<template>
  <!-- Mobile overlay -->
  <div v-if="isOpen" class="sidebar-overlay d-lg-none" @click="closeSidebar"></div>

  <aside class="tma-sidebar" :class="{ show: isOpen }">
    <div class="sidebar-header">
      <h5>{{ title }}</h5>
    </div>
    <ul class="sidebar-menu">
      <li v-for="item in menuItems" :key="item.route">
        <router-link :to="item.route" @click="closeSidebar">
          <i :class="'bi bi-' + item.icon"></i>
          {{ item.label }}
        </router-link>
      </li>
    </ul>
  </aside>
</template>
