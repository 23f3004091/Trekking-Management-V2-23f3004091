<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMessage.value = 'Please enter your username and password.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const res = await authStore.login({ username: username.value, password: password.value })
    if (res.success) {
      const role = authStore.user?.role
      if (role === 'Admin') {
        router.push('/admin')
      } else if (role === 'Trek Staff') {
        router.push('/staff')
      } else {
        router.push('/trekker')
      }
    } else {
      errorMessage.value = res.message || 'Login failed. Please check your credentials.'
    }
  } catch (error) {
    errorMessage.value = 'An unexpected error occurred. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="auth-page" id="login-page">
    <div class="auth-card animate-slide-up">
      <div class="auth-header">
        <span class="brand-icon">🏔️</span>
        <h2>Welcome Back</h2>
        <p>Sign in to continue your adventure</p>
      </div>

      <div class="auth-body">
        <transition name="fade">
          <div v-if="errorMessage" class="alert mb-4 py-2 px-3 d-flex align-items-center gap-2"
            style="background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; border-radius: 8px; font-size: 0.87rem;">
            <i class="bi bi-exclamation-circle-fill flex-shrink-0"></i>
            {{ errorMessage }}
          </div>
        </transition>

        <form class="tma-form" @submit.prevent="handleLogin" id="login-form">
          <div class="mb-3">
            <label class="form-label" for="login-username">
              <i class="bi bi-person me-1"></i>Username
            </label>
            <input
              id="login-username"
              type="text"
              class="form-control"
              v-model="username"
              placeholder="Enter your username"
              autocomplete="username"
              required
            >
          </div>

          <div class="mb-4">
            <label class="form-label" for="login-password">
              <i class="bi bi-lock me-1"></i>Password
            </label>
            <div class="input-group">
              <input
                id="login-password"
                :type="showPassword ? 'text' : 'password'"
                class="form-control"
                v-model="password"
                placeholder="Enter your password"
                autocomplete="current-password"
                required
              >
              <button
                class="btn btn-outline-secondary px-3"
                type="button"
                @click="showPassword = !showPassword"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
              >
                <i class="bi" :class="showPassword ? 'bi-eye-slash' : 'bi-eye'"></i>
              </button>
            </div>
          </div>

          <button
            type="submit"
            class="btn btn-tma w-100 py-2"
            id="login-submit-btn"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            <i v-else class="bi bi-box-arrow-in-right me-2"></i>
            {{ isLoading ? 'Signing In...' : 'Sign In' }}
          </button>
        </form>
      </div>

      <div class="auth-footer text-muted small">
        Don't have an account?
        <router-link to="/register" class="text-primary fw-semibold">Register as Trekker</router-link>
        &nbsp;·&nbsp;
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
