<script setup>
import { onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTrekkerStore } from '@/stores/trekker'
import StatCard from '@/components/StatCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const authStore = useAuthStore()
const trekkerStore = useTrekkerStore()

const username = computed(() => authStore.user?.username || 'Trekker')
const firstLetter = computed(() => username.value.charAt(0).toUpperCase())

onMounted(() => {
  trekkerStore.fetchSummary()
})
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="trekker-dashboard">
    <!-- Welcome Header -->
    <div class="page-header">
      <div class="d-flex align-items-center gap-3">
        <div class="d-flex align-items-center justify-content-center rounded-circle fw-bold text-white"
          style="width: 52px; height: 52px; background: linear-gradient(135deg, var(--tma-primary), var(--tma-primary-hover)); font-size: 1.4rem; flex-shrink: 0;">
          {{ firstLetter }}
        </div>
        <div>
          <h2 class="mb-1">Welcome back, {{ username }}! 👋</h2>
          <p class="mb-0">Ready for your next adventure?</p>
        </div>
      </div>
    </div>

    <div v-if="trekkerStore.isLoading">
      <LoadingSpinner message="Loading your dashboard..." />
    </div>

    <div v-else>
      <!-- Stats -->
      <div class="row g-4 mb-4 stagger-children">
        <div class="col-sm-6">
          <StatCard
            title="Available Treks"
            :value="trekkerStore.summary?.total_treks || 0"
            icon="compass"
            color="green"
          />
        </div>
        <div class="col-sm-6">
          <StatCard
            title="My Bookings"
            :value="trekkerStore.summary.total_bookings || 0"
            icon="journal-check"
            color="blue"
          />
        </div>
      </div>

      <!-- CTA Cards -->
      <div class="row g-4 stagger-children">
        <!-- Explore CTA -->
        <div class="col-lg-6">
          <div class="tma-card h-100" style="background: linear-gradient(135deg, var(--tma-primary-light) 0%, #e0e7ff 100%); border: 1px solid var(--tma-primary-alpha20);">
            <div class="card-body p-4 p-xl-5 text-center">
              <div class="mb-4" style="font-size: 3.5rem; filter: drop-shadow(0 4px 8px var(--tma-primary-alpha20));">🏔️</div>
              <h4 class="fw-bold mb-2" style="color: var(--tma-dark);">Find Your Next Trail</h4>
              <p class="text-muted mb-4 mx-auto" style="max-width: 300px;">
                Browse our hand-picked trekking routes — from easy day hikes to challenging expeditions.
              </p>
              <router-link to="/trekker/explore" class="btn btn-tma btn-lg px-4 shadow-sm">
                <i class="bi bi-binoculars me-2"></i>Explore Treks
              </router-link>
            </div>
          </div>
        </div>

        <!-- Quick Links -->
        <div class="col-lg-6">
          <div class="tma-card h-100">
            <div class="card-header-custom">
              <h5 class="mb-0"><i class="bi bi-grid-3x3-gap me-2"></i>Quick Navigation</h5>
            </div>
            <div class="card-body p-4">
              <div class="d-grid gap-3">
                <router-link to="/trekker/explore"
                  class="d-flex align-items-center gap-3 p-3 rounded-3 text-decoration-none"
                  style="background: var(--tma-primary-light); border: 1px solid var(--tma-primary-alpha20);">
                  <div class="d-flex align-items-center justify-content-center rounded-2"
                    style="width: 40px; height: 40px; background: #ffffff; border: 1px solid var(--tma-border);">
                    <i class="bi bi-binoculars-fill" style="color: var(--tma-primary);"></i>
                  </div>
                  <div>
                    <div class="fw-semibold" style="color: var(--tma-dark);">Explore Treks</div>
                    <div class="small text-muted">Discover new adventures</div>
                  </div>
                  <i class="bi bi-chevron-right ms-auto text-muted"></i>
                </router-link>

                <router-link to="/trekker/bookings"
                  class="d-flex align-items-center gap-3 p-3 rounded-3 text-decoration-none"
                  style="background: var(--tma-info-light); border: 1px solid rgba(2,132,199,0.2);">
                  <div class="d-flex align-items-center justify-content-center rounded-2"
                    style="width: 40px; height: 40px; background: #ffffff; border: 1px solid var(--tma-border);">
                    <i class="bi bi-journal-check-fill" style="color: var(--tma-sky-dark);"></i>
                  </div>
                  <div>
                    <div class="fw-semibold" style="color: var(--tma-dark);">My Bookings</div>
                    <div class="small text-muted">Track your reservations</div>
                  </div>
                  <i class="bi bi-chevron-right ms-auto text-muted"></i>
                </router-link>

                <router-link to="/trekker/profile"
                  class="d-flex align-items-center gap-3 p-3 rounded-3 text-decoration-none"
                  style="background: var(--tma-warning-light); border: 1px solid rgba(217,119,6,0.2);">
                  <div class="d-flex align-items-center justify-content-center rounded-2"
                    style="width: 40px; height: 40px; background: #ffffff; border: 1px solid var(--tma-border);">
                    <i class="bi bi-person-circle" style="color: var(--tma-gold);"></i>
                  </div>
                  <div>
                    <div class="fw-semibold" style="color: var(--tma-dark);">My Profile</div>
                    <div class="small text-muted">View your account info</div>
                  </div>
                  <i class="bi bi-chevron-right ms-auto text-muted"></i>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
