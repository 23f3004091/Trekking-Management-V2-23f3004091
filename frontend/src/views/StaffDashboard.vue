<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStaffStore } from '@/stores/staff'
import StatCard from '@/components/StatCard.vue'
import TrekCard from '@/components/TrekCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const staffStore = useStaffStore()
const router = useRouter()

onMounted(() => {
  staffStore.fetchSummary()
  staffStore.fetchTreks()
})

const navigateToTrek = (id) => {
  router.push(`/staff/trek/${id}`)
}
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="staff-dashboard">
    <div class="page-header">
      <h2><i class="bi bi-speedometer2 me-2 text-primary"></i>Staff Dashboard</h2>
      <p>Manage your assigned trekking routes and participants</p>
    </div>

    <div v-if="staffStore.isLoading && !staffStore.treks.length" class="py-5">
      <LoadingSpinner message="Loading dashboard..." />
    </div>

    <div v-else>
      <!-- Stats -->
      <div class="row g-4 mb-4 stagger-children">
        <div class="col-sm-6 col-xl-4">
          <StatCard
            title="Assigned Treks"
            :value="staffStore.summary?.total_treks || 0"
            icon="compass"
            color="green"
          />
        </div>
        <div class="col-sm-6 col-xl-4">
          <StatCard
            title="Total Bookings"
            :value="staffStore.summary?.total_bookings || 0"
            icon="journal-check"
            color="blue"
          />
        </div>
      </div>

      <!-- Assigned Treks -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="mb-0 fw-700" style="color: var(--tma-dark);">
          <i class="bi bi-map me-2"></i>Your Assigned Treks
        </h4>
        <span class="badge rounded-pill" style="background: var(--tma-primary-light); color: var(--tma-primary); font-size: 0.8rem; padding: 0.4rem 0.8rem;">
          {{ staffStore.treks.length }} trek{{ staffStore.treks.length !== 1 ? 's' : '' }}
        </span>
      </div>

      <div v-if="staffStore.treks.length === 0" class="empty-state">
        <i class="bi bi-compass"></i>
        <h5>No assigned treks</h5>
        <p>You don't have any treks assigned to you yet. Contact your administrator.</p>
      </div>

      <div v-else class="row g-4 stagger-children">
        <div class="col-md-6 col-xl-4" v-for="trek in staffStore.treks" :key="trek.id">
          <TrekCard :trek="trek">
            <template #actions>
              <button class="btn btn-tma w-100 mt-3" @click="navigateToTrek(trek.id)">
                <i class="bi bi-eye-fill me-2"></i>Manage Trek
              </button>
            </template>
          </TrekCard>
        </div>
      </div>
    </div>
  </div>
</template>
