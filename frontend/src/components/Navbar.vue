<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const userRole = computed(() => authStore.user?.role || null)
const username = computed(() => authStore.user?.username || '')
const firstLetter = computed(() => username.value.charAt(0).toUpperCase())

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar navbar-expand-lg tma-navbar" id="tma-main-navbar">
    <div class="container">
      <!-- Brand -->
      <router-link class="navbar-brand" to="/">
        <span style="font-size: 1.6rem; line-height: 1;">🏔️</span>
        <span class="brand-text">TrekMate</span>
      </router-link>

      <!-- Toggler for mobile -->
      <button
        class="navbar-toggler border-0 shadow-none"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarMain"
        aria-controls="navbarMain"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <i class="bi bi-list" style="font-size: 1.8rem; color: var(--tma-dark);"></i>
      </button>

      <div class="collapse navbar-collapse" id="navbarMain">
        <!-- ===== GUEST LINKS ===== -->
        <ul class="navbar-nav ms-auto align-items-center gap-2" v-if="!isAuthenticated">
          <li class="nav-item">
            <router-link class="nav-link" to="/">
              <i class="bi bi-house-door"></i> Home
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">
              <i class="bi bi-box-arrow-in-right"></i> Login
            </router-link>
          </li>
          <li class="nav-item ms-1">
            <router-link to="/register-trekker" class="btn btn-tma btn-sm px-3 py-2">
              <i class="bi bi-person-plus me-1"></i> Register as Trekker
            </router-link>
          </li>
          <li class="nav-item ms-1">
            <router-link to="/register-staff" class="btn btn-tma btn-sm px-3 py-2">
              <i class="bi bi-person-plus me-1"></i> Apply as Staff
            </router-link>
          </li>
        </ul>

        <!-- ===== ADMIN LINKS ===== -->
        <ul class="navbar-nav ms-auto align-items-center gap-1 flex-wrap" v-else-if="userRole === 'Admin'">
          <li class="nav-item">
            <router-link class="nav-link" to="/admin">
              <i class="bi bi-speedometer2"></i> Dashboard
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/treks">
              <i class="bi bi-compass"></i> Treks
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/staff">
              <i class="bi bi-person-badge"></i> Staff
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/users">
              <i class="bi bi-people"></i> Users
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/bookings">
              <i class="bi bi-journal-check"></i> Bookings
            </router-link>
          </li>
          <li class="nav-item ms-2">
            <div class="navbar-user-badge">
              <div class="user-avatar">{{ firstLetter }}</div>
              <span class="user-name d-none d-xl-inline">{{ username }}</span>
              <span class="role-badge admin d-none d-lg-inline">Admin</span>
            </div>
          </li>
          <li class="nav-item ms-1">
            <button class="btn btn-logout" @click="handleLogout">
              <i class="bi bi-box-arrow-right"></i>
              <span class="d-none d-sm-inline">Logout</span>
            </button>
          </li>
        </ul>

        <!-- ===== STAFF LINKS ===== -->
        <ul class="navbar-nav ms-auto align-items-center gap-1" v-else-if="userRole === 'Trek Staff'">
          <li class="nav-item">
            <router-link class="nav-link" to="/staff">
              <i class="bi bi-speedometer2"></i> Dashboard
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/staff/profile">
              <i class="bi bi-person-badge"></i> Profile
            </router-link>
          </li>
          <li class="nav-item ms-2">
            <div class="navbar-user-badge">
              <div class="user-avatar">{{ firstLetter }}</div>
              <span class="user-name d-none d-xl-inline">{{ username }}</span>
              <span class="role-badge staff d-none d-lg-inline">Staff</span>
            </div>
          </li>
          <li class="nav-item ms-1">
            <button class="btn btn-logout" @click="handleLogout">
              <i class="bi bi-box-arrow-right"></i>
              <span class="d-none d-sm-inline">Logout</span>
            </button>
          </li>
        </ul>

        <!-- ===== TREKKER LINKS ===== -->
        <ul class="navbar-nav ms-auto align-items-center gap-1" v-else-if="userRole === 'Trekker'">
          <li class="nav-item">
            <router-link class="nav-link" to="/trekker">
              <i class="bi bi-speedometer2"></i> Dashboard
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/trekker/explore">
              <i class="bi bi-binoculars"></i> Explore
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/trekker/bookings">
              <i class="bi bi-journal-check"></i> My Bookings
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/trekker/profile">
              <i class="bi bi-person-circle"></i> Profile
            </router-link>
          </li>
          <li class="nav-item ms-2">
            <div class="navbar-user-badge">
              <div class="user-avatar">{{ firstLetter }}</div>
              <span class="user-name d-none d-xl-inline">{{ username }}</span>
              <span class="role-badge trekker d-none d-lg-inline">Trekker</span>
            </div>
          </li>
          <li class="nav-item ms-1">
            <button class="btn btn-logout" @click="handleLogout">
              <i class="bi bi-box-arrow-right"></i>
              <span class="d-none d-sm-inline">Logout</span>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
