<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/axiosApi.js'

const router = useRouter()

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  contact_details: ''
})

const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!form.value.username || !form.value.email || !form.value.password || !form.value.confirmPassword) {
    errorMessage.value = 'Please fill in all required fields.'
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
    await apiClient.post('/auth/register-staff', {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      contact_details: form.value.contact_details
    })

    successMessage.value = 'Staff account created! Awaiting admin approval. Redirecting to login…'
    setTimeout(() => router.push('/login'), 2500)
  } catch (err) {
    errorMessage.value = err.response?.data?.error || 'Registration failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="auth-page" id="register-staff-page">
    <div class="auth-card animate-slide-up" style="max-width: 500px;">
      <div class="auth-header">
        <span class="brand-icon">🧗</span>
        <h2>Staff Registration</h2>
        <p>Apply to become a TrekMate staff member</p>
      </div>

      <div class="auth-body">
        <!-- Success -->
        <transition name="fade">
          <div v-if="successMessage"
            class="alert mb-4 py-2 px-3 d-flex align-items-center gap-2"
            style="background:#f0fdf4;color:#166534;border:1px solid #bbf7d0;border-radius:8px;font-size:0.87rem;">
            <i class="bi bi-check-circle-fill flex-shrink-0"></i>
            {{ successMessage }}
          </div>
        </transition>

        <!-- Error -->
        <transition name="fade">
          <div v-if="errorMessage"
            class="alert mb-4 py-2 px-3 d-flex align-items-center gap-2"
            style="background:#fef2f2;color:#991b1b;border:1px solid #fecaca;border-radius:8px;font-size:0.87rem;">
            <i class="bi bi-exclamation-circle-fill flex-shrink-0"></i>
            {{ errorMessage }}
          </div>
        </transition>

        <!-- Info banner -->
        <div class="mb-4 py-2 px-3 d-flex align-items-start gap-2"
          style="background:var(--tma-primary-light);color:var(--tma-primary-dark,#1e3a2f);border:1px solid var(--tma-primary-alpha20);border-radius:8px;font-size:0.84rem;">
          <i class="bi bi-info-circle-fill flex-shrink-0 mt-1" style="color:var(--tma-primary);"></i>
          <span>Your account will be reviewed by an admin before you can log in.</span>
        </div>

        <form class="tma-form row g-3" @submit.prevent="handleRegister" id="register-staff-form">
          <!-- Username -->
          <div class="col-12">
            <label class="form-label" for="staff-username">
              <i class="bi bi-person me-1"></i>Username <span class="text-danger">*</span>
            </label>
            <input
              id="staff-username"
              type="text"
              class="form-control"
              v-model="form.username"
              placeholder="Choose a username"
              autocomplete="username"
              required
            >
          </div>

          <!-- Email -->
          <div class="col-12">
            <label class="form-label" for="staff-email">
              <i class="bi bi-envelope me-1"></i>Email Address <span class="text-danger">*</span>
            </label>
            <input
              id="staff-email"
              type="email"
              class="form-control"
              v-model="form.email"
              placeholder="Enter your email"
              autocomplete="email"
              required
            >
          </div>

          <!-- Contact Details -->
          <div class="col-12">
            <label class="form-label" for="staff-contact">
              <i class="bi bi-telephone me-1"></i>Contact Details
            </label>
            <input
              id="staff-contact"
              type="text"
              class="form-control"
              v-model="form.contact_details"
              placeholder="Phone number, address, etc. (optional)"
            >
          </div>

          <!-- Password -->
          <div class="col-md-6">
            <label class="form-label" for="staff-password">
              <i class="bi bi-lock me-1"></i>Password <span class="text-danger">*</span>
            </label>
            <div class="input-group">
              <input
                id="staff-password"
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

          <!-- Confirm Password -->
          <div class="col-md-6">
            <label class="form-label" for="staff-confirm-password">
              <i class="bi bi-lock-fill me-1"></i>Confirm Password <span class="text-danger">*</span>
            </label>
            <input
              id="staff-confirm-password"
              :type="showPassword ? 'text' : 'password'"
              class="form-control"
              v-model="form.confirmPassword"
              placeholder="Re-enter password"
              autocomplete="new-password"
              required
            >
          </div>

          <!-- Submit -->
          <div class="col-12 mt-1">
            <button
              type="submit"
              class="btn btn-tma w-100 py-2"
              id="register-staff-submit-btn"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              <i v-else class="bi bi-person-badge me-2"></i>
              {{ isLoading ? 'Submitting Application…' : 'Submit Staff Application' }}
            </button>
          </div>
        </form>
      </div>

      <div class="auth-footer text-muted small">
        Already have an account?
        <router-link to="/login" class="text-primary fw-semibold">Sign in here</router-link>
        &nbsp;·&nbsp;
        <router-link to="/register" class="text-primary fw-semibold">Register as Trekker</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
