<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useTrekkerStore } from '@/stores/trekker'
import SearchBar from '@/components/SearchBar.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const showCancelModal = ref(false)

const trekkerStore = useTrekkerStore()
const showToast = inject('showToast')

const activeFilter = ref({ status: 'All' })
const bookingToCancel = ref(null)

onMounted(() => {
  trekkerStore.fetchHistory()
})

const filteredBookings = computed(() => {
  if (activeFilter.value.status === 'All') return trekkerStore.history
  return (trekkerStore.history || []).filter(b => b.status === activeFilter.value.status)
})

const handleFilter = (f) => { activeFilter.value = f }

const getStatusClass = (s) => {
  if (s === 'Booked') return 'badge-booked'
  if (s === 'Cancelled') return 'badge-cancelled'
  if (s === 'Completed') return 'badge-completed'
  return ''
}

const getStatusIcon = (s) => {
  if (s === 'Booked') return 'bi-check-circle-fill'
  if (s === 'Cancelled') return 'bi-x-circle-fill'
  if (s === 'Completed') return 'bi-trophy-fill'
  return ''
}

const formatDate = (d) => {
  if (!d) return 'N/A'
  return new Date(d).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}

const getDifficultyClass = (d) => {
  if (d === 'Easy') return 'badge-easy'
  if (d === 'Moderate') return 'badge-moderate'
  if (d === 'Hard') return 'badge-hard'
  return ''
}

const confirmCancel = (id) => {
  bookingToCancel.value = id
  showCancelModal.value = true
}

const executeCancel = async () => {
  if (!bookingToCancel.value) return
  try {
    const result = await trekkerStore.updateBookingStatus(bookingToCancel.value, 'Cancelled')
    if (result.success) {
      showToast('Booking cancelled successfully', 'success')
    } else {
      showToast(result.message || 'Failed to cancel', 'error')
    }
  } catch (err) {
    showToast('Failed to cancel booking', 'error')
  }
}
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="trekker-bookings">
    <div class="page-header">
      <h2><i class="bi bi-journal-check me-2 text-primary"></i>My Bookings</h2>
      <p>Track all your trekking reservations and history</p>
    </div>

    <SearchBar
      placeholder="Filter by status..."
      :filters="[
        { key: 'status', label: 'Status', options: ['All', 'Booked', 'Cancelled', 'Completed'] }
      ]"
      @filter="handleFilter"
    />

    <div v-if="trekkerStore.isLoading" class="py-5">
      <LoadingSpinner message="Loading your bookings..." />
    </div>
    <div v-else-if="filteredBookings.length === 0" class="empty-state">
      <i class="bi bi-journal-x"></i>
      <h5>No bookings found</h5>
      <p>You haven't made any bookings matching this status.</p>
      <router-link to="/trekker/explore" class="btn btn-tma mt-3">
        <i class="bi bi-binoculars me-2"></i>Explore Treks
      </router-link>
    </div>

    <!-- Booking Cards Grid -->
    <div v-else>
      <p class="text-muted small mb-3">
        <i class="bi bi-journal me-1"></i>
        {{ filteredBookings.length }} booking{{ filteredBookings.length !== 1 ? 's' : '' }}
      </p>

      <!-- Table for larger screens -->
      <div class="tma-card d-none d-md-block">
        <div class="table-responsive">
          <table class="table tma-table mb-0 align-middle">
            <thead>
              <tr>
                <th>Booking #</th>
                <th>Trek ID</th>
                <th>Location</th>
                <th>Date</th>
                <th>Difficulty</th>
                <th>Status</th>
                <th>Booking Date</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="booking in filteredBookings" :key="booking.id">
                <td class="fw-bold">#{{ booking.id }}</td>
                <td>
                  <span class="badge rounded-pill" style="background: rgba(45,106,79,0.1); color: var(--primary); padding: 0.35rem 0.75rem;">
                    Trek #{{ booking.trek_id }}
                  </span>
                </td>
                <td>
                  <i class="bi bi-geo-alt-fill text-primary me-1"></i>
                  {{ booking.location }}
                </td>
                <td class="align-middle text-nowrap">
                  <div class="d-flex">
                    <!-- Added the missing calendar icon class here -->
                    <i class="bi bi-calendar3 text-secondary me-2"></i>
                    <span>{{ booking.start_date ?? 'N/A' }} <span class="text-muted mx-1">to</span> {{ booking.end_date ?? 'N/A' }}</span>
                  </div>
                </td>
                <td>
                  <span class="badge-status" :class="getDifficultyClass(booking.difficulty)">
                    {{ booking.difficulty }}
                  </span>
                </td>
                <td>
                  <i class="bi bi-calendar2-event text-muted me-1"></i>
                  {{ formatDate(booking.booking_date) }}
                </td>
                <td>
                  <span class="badge-status" :class="getStatusClass(booking.status)">
                    <i class="bi me-1" :class="getStatusIcon(booking.status)"></i>
                    {{ booking.status }}
                  </span>
                </td>
                <td class="text-end">
                  <button
                    v-if="booking.status === 'Booked'"
                    class="btn btn-sm btn-outline-danger"
                    @click="confirmCancel(booking.id)"
                    :id="`cancel-booking-${booking.id}`"
                  >
                    <i class="bi bi-x-circle me-1"></i>Cancel
                  </button>
                  <span v-else class="text-muted small fst-italic">—</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Card view for mobile -->
      <div class="d-md-none row g-3">
        <div class="col-12" v-for="booking in filteredBookings" :key="booking.id">
          <div class="tma-card">
            <div class="card-body p-3">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="fw-bold">Booking #{{ booking.id }}</span>
                <span class="badge-status" :class="getStatusClass(booking.status)">{{ booking.status }}</span>
              </div>
              <div class="small text-muted mb-2">
                <i class="bi bi-compass me-1 text-primary"></i>Trek #{{ booking.trek_id }}
              </div>
              <div class="small text-muted mb-3">
                <i class="bi bi-calendar2 me-1"></i>{{ formatDate(booking.booking_date) }}
              </div>
              <button
                v-if="booking.status === 'Booked'"
                class="btn btn-sm btn-outline-danger w-100"
                @click="confirmCancel(booking.id)"
              >
                <i class="bi bi-x-circle me-1"></i>Cancel Booking
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cancel Confirm Modal -->
    <ConfirmModal
      id="cancelConfirmModal"
      v-model="showCancelModal"
      title="Cancel Booking"
      message="Are you sure you want to cancel this booking? This action cannot be undone."
      confirmText="Yes, Cancel Booking"
      confirmClass="btn-danger"
      @confirm="executeCancel"
    />
  </div>
</template>
