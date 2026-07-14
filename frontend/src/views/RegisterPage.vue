<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/axiosApi.js'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleRegister = async () => {
  errorMessage.value = ''

  if (!form.value.username || !form.value.email || !form.value.password || !form.value.confirmPassword) {
    errorMessage.value = 'All fields are required.'
    return
  }

  if (form.value.password.length < 6) {
    errorMessage.value = 'Password must be at least 6 characters.'
    return
  }

  if (form.value.password !== form.value.confirmPassword) {
    errorMessage.value = 'Passwords do not match.'
    return
  }

  isLoading.value = true

  try {
    // Register the trekker
    await apiClient.post('/auth/register-trekker', {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password
    })

    // Auto-login after registration
    const loginRes = await authStore.login({
      username: form.value.username,
      password: form.value.password
    })

    if (loginRes.success) {
      router.push('/trekker')
    } else {
      successMessage.value = 'Registration successful! Please log in.'
      setTimeout(() => router.push('/login'), 2000)
    }
  } catch (err) {
    errorMessage.value = err.response?.data?.error || 'Registration failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="auth-page" id="register-page">
    <div class="auth-card animate-slide-up" style="max-width: 480px;">
      <div class="auth-header">
        <span class="brand-icon">🏔️</span>
        <h2>Join TrekMate</h2>
        <p>Create your trekker account today</p>
      </div>

      <div class="auth-body">
        <div v-if="successMessage" class="alert mb-4 py-2 px-3 d-flex align-items-center gap-2"
          style="background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; border-radius: 8px; font-size: 0.87rem;">
          <i class="bi bi-check-circle-fill flex-shrink-0"></i>
          {{ successMessage }}
        </div>

        <transition name="fade">
          <div v-if="errorMessage" class="alert mb-4 py-2 px-3 d-flex align-items-center gap-2"
            style="background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; border-radius: 8px; font-size: 0.87rem;">
            <i class="bi bi-exclamation-circle-fill flex-shrink-0"></i>
            {{ errorMessage }}
          </div>
        </transition>

        <form class="tma-form row g-3" @submit.prevent="handleRegister" id="register-form">
          <div class="col-12">
            <label class="form-label" for="reg-username">
              <i class="bi bi-person me-1"></i>Username
            </label>
            <input
              id="reg-username"
              type="text"
              class="form-control"
              v-model="form.username"
              placeholder="Choose a username"
              autocomplete="username"
              required
            >
          </div>

          <div class="col-12">
            <label class="form-label" for="reg-email">
              <i class="bi bi-envelope me-1"></i>Email Address
            </label>
            <input
              id="reg-email"
              type="email"
              class="form-control"
              v-model="form.email"
              placeholder="Enter your email"
              autocomplete="email"
              required
            >
          </div>

          <div class="col-12">
            <label class="form-label" for="reg-password">
              <i class="bi bi-lock me-1"></i>Password
            </label>
            <div class="input-group">
              <input
                id="reg-password"
                :type="showPassword ? 'text' : 'password'"
                class="form-control"
                v-model="form.password"
                placeholder="Min. 6 characters"
                autocomplete="new-password"
                required
              >
              <button class="btn btn-outline-secondary px-3" type="button" @click="showPassword = !showPassword">
                <i class="bi" :class="showPassword ? 'bi-eye-slash' : 'bi-eye'"></i>
              </button>
            </div>
          </div>

          <div class="col-12">
            <label class="form-label" for="reg-confirm-password">
              <i class="bi bi-lock-fill me-1"></i>Confirm Password
            </label>
            <input
              id="reg-confirm-password"
              :type="showPassword ? 'text' : 'password'"
              class="form-control"
              v-model="form.confirmPassword"
              placeholder="Re-enter your password"
              autocomplete="new-password"
              required
            >
          </div>

          <div class="col-12 mt-1">
            <button
              type="submit"
              class="btn btn-tma w-100 py-2"
              id="register-submit-btn"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              <i v-else class="bi bi-person-plus me-2"></i>
              {{ isLoading ? 'Creating Account...' : 'Create Account' }}
            </button>
          </div>
        </form>
      </div>

      <div class="auth-footer text-muted small">
        Already have an account?
        <router-link to="/login" class="text-primary fw-semibold">Sign in here</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
