<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTrekkerStore } from '@/stores/trekker'

const authStore = useAuthStore()
const trekkerStore = useTrekkerStore()

const username = computed(() => authStore.user?.username || 'Unknown')
const role = computed(() => authStore.user?.role || 'Trekker')
const firstLetter = computed(() => username.value.charAt(0).toUpperCase())
console.log(trekkerStore.summary)
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="trekker-profile">
    <div class="page-header">
      <h2><i class="bi bi-person-circle me-2 text-primary"></i>My Profile</h2>
      <p>Your account information and activity overview</p>
    </div>

    <div class="row g-4">
      <!-- Profile Card -->
      <div class="col-md-5 col-lg-4">
        <div class="tma-card overflow-hidden">
          <!-- Banner -->
          <div style="height: 100px; background: linear-gradient(135deg, var(--primary-dark), var(--primary-light));"></div>
          <!-- Avatar + Info -->
          <div class="card-body text-center px-4 pb-4" style="margin-top: -50px;">
            <div class="d-inline-flex align-items-center justify-content-center rounded-circle text-white fw-bold shadow"
              style="width: 96px; height: 96px; font-size: 2.5rem; border: 4px solid white; background: linear-gradient(135deg, var(--primary), var(--primary-light));">
              {{ firstLetter }}
            </div>
            <h3 class="mt-3 mb-1 fw-bold">{{ username }}</h3>
            <span class="badge rounded-pill px-3 py-2"
              style="background: rgba(45,106,79,0.1); color: var(--primary); font-size: 0.8rem;">
              <i class="bi bi-shield-check me-1"></i>{{ role }}
            </span>
          </div>
        </div>
      </div>

      <!-- Account Details -->
      <div class="col-md-7 col-lg-8">
        <div class="tma-card h-100">
          <div class="card-header-custom">
            <h5 class="mb-0"><i class="bi bi-info-circle me-2"></i>Account Details</h5>
          </div>
          <div class="card-body p-4">
            <div class="row g-4">
              <div class="col-sm-6">
                <div class="p-3 rounded-3" style="background: #f8faf9;">
                  <div class="small text-muted fw-semibold text-uppercase mb-1" style="letter-spacing: 0.5px;">Username</div>
                  <div class="fw-semibold d-flex align-items-center gap-2">
                    <i class="bi bi-person-fill text-primary"></i>
                    {{ username }}
                  </div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="p-3 rounded-3" style="background: #f8faf9;">
                  <div class="small text-muted fw-semibold text-uppercase mb-1" style="letter-spacing: 0.5px;">Role</div>
                  <div class="fw-semibold d-flex align-items-center gap-2">
                    <i class="bi bi-shield-fill-check text-primary"></i>
                    {{ role }}
                  </div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="p-3 rounded-3" style="background: #f8faf9;">
                  <div class="small text-muted fw-semibold text-uppercase mb-1" style="letter-spacing: 0.5px;">Account Status</div>
                  <div class="fw-semibold d-flex align-items-center gap-2 text-success">
                    <i class="bi bi-check-circle-fill"></i>
                    Active Member
                  </div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="p-3 rounded-3" style="background: #f8faf9;">
                  <div class="small text-muted fw-semibold text-uppercase mb-1" style="letter-spacing: 0.5px;">Total Bookings</div>
                  <div class="fw-semibold d-flex align-items-center gap-2">
                    <i class="bi bi-journal-check text-primary"></i>
                    {{ trekkerStore.summary?.total_bookings || 0 }} bookings
                  </div>
                </div>
              </div>
            </div>

            <hr class="my-4">

            <div class="d-flex gap-3 flex-wrap">
              <router-link to="/trekker/explore" class="btn btn-tma">
                <i class="bi bi-binoculars me-2"></i>Explore Treks
              </router-link>
              <router-link to="/trekker/bookings" class="btn btn-tma-outline">
                <i class="bi bi-journal-check me-2"></i>View Bookings
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
