<script setup>
import { onMounted, computed, ref, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTrekkerStore } from '@/stores/trekker'
import StatCard from '@/components/StatCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import apiClient from '@/axiosApi.js'

const authStore = useAuthStore()
const trekkerStore = useTrekkerStore()

const username = computed(() => authStore.user?.username || 'Trekker')
const firstLetter = computed(() => username.value.charAt(0).toUpperCase())

const recentBookings = computed(() => {
  return (trekkerStore.history || []).slice(0, 5)
})

// ── CSV Export state ─────────────────────────────────────────────────────────
const exportStatus = ref('idle')   // idle | processing | done | error
const exportTaskId = ref(null)
const exportError  = ref(null)
let   pollInterval = null

async function triggerExport() {
  exportStatus.value = 'processing'
  exportError.value  = null
  exportTaskId.value = null

  try {
    const res = await apiClient.post('/trekker/export-history')
    // 202 Accepted – job is queued
    exportTaskId.value = res.data.task_id
    startPolling()
  } catch (err) {
    exportStatus.value = 'error'
    exportError.value  = err.response?.data?.error || 'Failed to start export'
  }
}

function startPolling() {
  pollInterval = setInterval(async () => {
    try {
      const res = await apiClient.get(`/trekker/export-status/${exportTaskId.value}`)
      if (res.data.status === 'SUCCESS') {
        clearInterval(pollInterval)
        pollInterval = null
        exportStatus.value = 'done'
      } else if (res.data.status === 'FAILURE') {
        clearInterval(pollInterval)
        pollInterval = null
        exportStatus.value = 'error'
        exportError.value  = res.data.error || 'Export failed'
      }
      // else still PENDING / STARTED — keep polling
    } catch {
      clearInterval(pollInterval)
      pollInterval = null
      exportStatus.value = 'error'
      exportError.value  = 'Could not check export status'
    }
  }, 3000)
}

function downloadCsv() {
  // Use direct browser navigation so the browser handles the download natively.
  // JWT is passed as a query param because XHR/fetch on send_file responses
  // is blocked by CORS (no CORS headers on Flask's file responses).
  const token = authStore.accessToken
  const url   = `http://localhost:8000/api/trekker/download-csv/${exportTaskId.value}?jwt=${token}`
  const link  = document.createElement('a')
  link.href   = url
  link.setAttribute('download', 'booking_history.csv')
  document.body.appendChild(link)
  link.click()
  link.remove()
}

onMounted(() => {
  trekkerStore.fetchSummary()
  trekkerStore.fetchHistory()
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})

const formatDateTime = (d) => {
  if (!d) return 'N/A'
  return new Date(d).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}
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
          <h2 class="mb-1">Welcome back, {{ username }}!</h2>
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
              <div class="mb-4" style="font-size: 3.5rem; filter: drop-shadow(0 4px 8px var(--tma-primary-alpha20));">️</div>
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

                <!-- Export Booking History -->
                <div
                  id="export-booking-card"
                  class="d-flex align-items-center gap-3 p-3 rounded-3"
                  style="background: var(--tma-success-light, #f0fdf4); border: 1px solid rgba(22,163,74,0.2);"
                >
                  <div class="d-flex align-items-center justify-content-center rounded-2"
                    style="width: 40px; height: 40px; background: #ffffff; border: 1px solid var(--tma-border); flex-shrink: 0;">
                    <i class="bi bi-file-earmark-spreadsheet-fill" style="color: #16a34a;"></i>
                  </div>
                  <div class="flex-grow-1">
                    <div class="fw-semibold" style="color: var(--tma-dark);">Export Booking History</div>
                    <div class="small text-muted">Download your trek history as CSV</div>
                  </div>

                  <!-- idle: show Export button -->
                  <button
                    v-if="exportStatus === 'idle'"
                    id="btn-export-history"
                    class="btn btn-sm btn-tma ms-auto"
                    style="white-space: nowrap;"
                    @click="triggerExport"
                  >
                    <i class="bi bi-download me-1"></i>Export
                  </button>

                  <!-- processing: spinner -->
                  <span
                    v-else-if="exportStatus === 'processing'"
                    class="ms-auto d-flex align-items-center gap-2 small text-muted"
                  >
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    Processing…
                  </span>

                  <!-- done: Download button -->
                  <button
                    v-else-if="exportStatus === 'done'"
                    id="btn-download-csv"
                    class="btn btn-sm btn-success ms-auto"
                    style="white-space: nowrap;"
                    @click="downloadCsv"
                  >
                    <i class="bi bi-file-earmark-arrow-down me-1"></i>Download
                  </button>

                  <!-- error: retry -->
                  <button
                    v-else-if="exportStatus === 'error'"
                    id="btn-export-retry"
                    class="btn btn-sm btn-outline-danger ms-auto"
                    style="white-space: nowrap;"
                    @click="triggerExport"
                    :title="exportError"
                  >
                    <i class="bi bi-arrow-clockwise me-1"></i>Retry
                  </button>
                </div>
                <!-- error message -->
                <div v-if="exportStatus === 'error' && exportError" class="small text-danger px-1">
                  <i class="bi bi-exclamation-circle me-1"></i>{{ exportError }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Bookings -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="tma-card">
            <div class="card-header-custom d-flex align-items-center justify-content-between">
              <h5 class="mb-0">
                <i class="bi bi-clock-history me-2 text-primary"></i>Recent Bookings
              </h5>
              <router-link to="/trekker/bookings" class="btn btn-sm btn-outline-secondary" style="font-size:0.8rem;">
                <i class="bi bi-arrow-right me-1"></i>View All
              </router-link>
            </div>
            <div class="card-body p-0">
              <div v-if="trekkerStore.isLoading" class="py-4">
                <LoadingSpinner message="Loading bookings..." />
              </div>
              <div v-else-if="recentBookings.length === 0" class="d-flex flex-column align-items-center justify-content-center py-5 text-muted">
                <i class="bi bi-journal-x fs-2 mb-2 opacity-50"></i>
                <p class="mb-0 small fw-semibold">No bookings yet — explore and book a trek!</p>
              </div>
              <div v-else class="table-responsive">
                <table class="table tma-table mb-0 align-middle">
                  <thead>
                    <tr>
                      <th>Booking #</th>
                      <th>Trek</th>
                      <th>Location</th>
                      <th>Trek Start (Date &amp; Time)</th>
                      <th>Booked On</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="booking in recentBookings" :key="booking.id">
                      <td class="fw-bold text-muted">#{{ booking.id }}</td>
                      <td class="fw-semibold small">{{ booking.trek_name || `Trek #${booking.trek_id}` }}</td>
                      <td>
                        <i class="bi bi-geo-alt-fill text-primary me-1"></i>
                        <span class="small">{{ booking.location || '—' }}</span>
                      </td>
                      <td class="small text-nowrap">
                        <i class="bi bi-calendar-event text-primary me-1"></i>
                        {{ formatDateTime(booking.start_date) }}
                      </td>
                      <td class="small text-nowrap">
                        <i class="bi bi-clock text-muted me-1"></i>
                        {{ formatDateTime(booking.booking_date) }}
                      </td>
                      <td>
                        <span class="badge-status" :class="{
                          'badge-booked': booking.status === 'Booked',
                          'badge-cancelled': booking.status === 'Cancelled',
                          'badge-completed': booking.status === 'Completed'
                        }">
                          {{ booking.status }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
