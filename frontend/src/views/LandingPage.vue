<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<template>
  <div class="landing-wrapper">
    <!-- Hero Section -->
    <section class="landing-hero" id="landing-hero">
      <div class="container hero-content py-5">
        <div class="row align-items-center min-vh-75 py-5">
          <div class="col-lg-7 animate-slide-up">
            <div class="mb-3">
              <span class="badge rounded-pill px-3 py-2 fw-semibold"
                style="background: var(--tma-primary-light); color: var(--tma-primary); border: 1px solid var(--tma-primary-alpha20); font-size: 0.8rem; letter-spacing: 0.5px;">
                <i class="bi bi-stars me-1"></i> Trekking Management
              </span>
            </div>
            <h1 class="hero-title mb-4">
              Explore the World,<br>
              <span class="accent">One Trek at a Time</span>
            </h1>
            <p class="hero-subtitle mb-5">
              Discover breathtaking trails, book your next adventure, and track your trekking journey with Trekking Management — your ultimate outdoor companion.
            </p>
            <div class="d-flex flex-wrap gap-3 mb-5" v-if="!isAuthenticated">
              <router-link to="/register" class="btn btn-tma btn-lg fw-bold px-4 py-3">
                <i class="bi bi-rocket-takeoff me-2"></i> Start Exploring
              </router-link>
              <router-link to="/login" class="btn btn-tma-outline btn-lg fw-semibold px-4 py-3">
                <i class="bi bi-box-arrow-in-right me-2"></i> Sign In
              </router-link>
            </div>
            <div class="d-flex flex-wrap gap-3 mb-5" v-else>
              <router-link :to="authStore.user?.role === 'Admin' ? '/admin' : (authStore.user?.role === 'Trek Staff' ? '/staff' : '/trekker')"
                class="btn btn-tma btn-lg fw-bold px-4 py-3">
                <i class="bi bi-speedometer2 me-2"></i> Go to Dashboard
              </router-link>
            </div>

            <!-- Stats row -->
            <div class="hero-stats stagger-children">
              <div class="hero-stat-item">
                <span class="stat-num">100+</span>
                <span class="stat-desc">Curated Treks</span>
              </div>
              <div class="hero-stat-item">
                <span class="stat-num">500+</span>
                <span class="stat-desc">Happy Trekkers</span>
              </div>
              <div class="hero-stat-item">
                <span class="stat-num">50+</span>
                <span class="stat-desc">Expert Guides</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section" id="features">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="fw-800" style="color: var(--tma-dark);">Why Choose Trekking Management?</h2>
          <p class="text-muted" style="max-width: 500px; margin: 0.75rem auto 0;">Everything you need for a seamless trekking experience, in one powerful platform.</p>
        </div>
        <div class="row g-4 stagger-children">
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon" style="background: var(--tma-primary-light);">
                <i class="bi bi-binoculars-fill" style="color: var(--tma-primary);"></i>
              </div>
              <h4>Discover Treks</h4>
              <p>Browse our curated collection of amazing trekking routes across breathtaking locations — from easy day hikes to serious expeditions.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon" style="background: var(--tma-info-light);">
                <i class="bi bi-lightning-charge-fill" style="color: var(--tma-sky-dark);"></i>
              </div>
              <h4>Book Instantly</h4>
              <p>Reserve your spot on any upcoming trek in just a few clicks. Our seamless booking system makes it effortless.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon" style="background: var(--tma-warning-light);">
                <i class="bi bi-graph-up-arrow" style="color: var(--tma-gold);"></i>
              </div>
              <h4>Track & Manage</h4>
              <p>Keep a detailed history of all your completed treks, manage bookings, and track your upcoming adventures.</p>
            </div>
          </div>
        </div>

        <!-- Role cards -->
        <div class="row g-4 mt-2 stagger-children">
          <div class="col-md-4">
            <div class="feature-card" style="border-top: 4px solid var(--tma-primary);">
              <div class="feature-icon" style="background: var(--tma-primary-light);">
                <i class="bi bi-person-hiking" style="color: var(--tma-primary); font-size: 1.8rem;"></i>
              </div>
              <h4>Trekkers</h4>
              <p>Browse open treks, book adventures, and manage your personal booking history with ease.</p>
              <router-link to="/register" class="btn btn-sm btn-tma mt-2">Get Started →</router-link>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card" style="border-top: 4px solid var(--tma-sky-dark);">
              <div class="feature-icon" style="background: var(--tma-info-light);">
                <i class="bi bi-person-badge-fill" style="color: var(--tma-sky-dark); font-size: 1.8rem;"></i>
              </div>
              <h4>Trek Staff</h4>
              <p>Manage assigned treks, update availability, and handle participant lists efficiently.</p>
              <router-link to="/login" class="btn btn-sm btn-tma-outline mt-2">Sign In →</router-link>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card" style="border-top: 4px solid var(--tma-accent);">
              <div class="feature-icon" style="background: var(--tma-accent-light);">
                <i class="bi bi-shield-lock-fill" style="color: var(--tma-accent); font-size: 1.8rem;"></i>
              </div>
              <h4>Administrators</h4>
              <p>Full control over treks, staff management, bookings, and platform-wide analytics.</p>
              <router-link to="/login" class="btn btn-sm btn-tma-outline mt-2">Admin Login →</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-4 text-center text-muted small" style="background: var(--tma-secondary-light); border-top: 1px solid var(--tma-border);">
      <div class="container">
        <p class="mb-1"> <strong>Trekking Management</strong> — Trekking Management</p>
        <p class="mb-0" style="font-size: 0.78rem;">Built with for adventure seekers</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.min-vh-75 { min-height: 75vh; }
</style>