<script setup>
import { ref, provide } from 'vue'
import Navbar from './components/Navbar.vue'

// Toast notification system (provide/inject)
const toasts = ref([])
let toastId = 0

const showToast = (message, type = 'success') => {
  const id = ++toastId
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 4000)
}

const removeToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

provide('showToast', showToast)
</script>

<template>
  <div id="tma-app">
    <Navbar />
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>

    <!-- Global Toast Container -->
    <div class="tma-toast-container" v-if="toasts.length">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="tma-toast"
        :class="'toast-' + toast.type"
      >
        <i
          class="bi"
          :class="{
            'bi-check-circle-fill': toast.type === 'success',
            'bi-exclamation-triangle-fill': toast.type === 'error',
            'bi-info-circle-fill': toast.type === 'info',
            'bi-exclamation-circle-fill': toast.type === 'warning'
          }"
        ></i>
        <span>{{ toast.message }}</span>
        <button
          class="btn-close btn-close-sm ms-auto"
          @click="removeToast(toast.id)"
          style="font-size: 0.65rem;"
        ></button>
      </div>
    </div>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
