<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useAdminStore } from '@/stores/admin'
import SearchBar from '@/components/SearchBar.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const adminStore = useAdminStore()
const showToast = inject('showToast')

const searchQuery = ref('')
const activeFilter = ref({ status: 'All' })

onMounted(() => {
  adminStore.fetchBookings()
})

const filteredBookings = computed(() => {
  const q = searchQuery.value
  return (adminStore.bookingList || []).filter(b => {
    const matchSearch = !q ||
      b.id?.toString().includes(q) ||
      b.user_id?.toString().includes(q) ||
      b.trek_id?.toString().includes(q)
    const matchStatus = activeFilter.value.status === 'All' || b.status === activeFilter.value.status
    return matchSearch && matchStatus
  })
})

const handleSearch = (q) => { searchQuery.value = q }
const handleFilter = (f) => { activeFilter.value = f }

const getStatusClass = (s) => {
  if (s === 'Booked') return 'badge-booked'
  if (s === 'Cancelled') return 'badge-cancelled'
  if (s === 'Completed') return 'badge-completed'
  return ''
}

const formatDate = (d) => {
  if (!d) return 'N/A'
  return new Date(d).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

const updateBookingStatus = async (id, action) => {
  try {
    await adminStore.manageBooking(id, action)
    showToast(`Booking ${action}d successfully`, 'success')
  } catch (err) {
    showToast(`Failed to ${action} booking`, 'error')
  }
}
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="admin-bookings">
    <div class="page-header">
      <h2><i class="bi bi-journal-check me-2 text-primary"></i>All Bookings</h2>
      <p>Monitor and manage all trek reservations across the platform</p>
    </div>

    <SearchBar
      placeholder="Search by Booking ID, User ID, or Trek ID..."
      :filters="[
        { key: 'status', label: 'Status', options: ['All', 'Booked', 'Cancelled', 'Completed'] }
      ]"
      @search="handleSearch"
      @filter="handleFilter"
    />

    <div class="tma-card">
      <div class="card-body p-0">
        <div v-if="adminStore.isLoading" class="py-5">
          <LoadingSpinner message="Loading bookings..." />
        </div>
        <div v-else-if="filteredBookings.length === 0" class="empty-state">
          <i class="bi bi-journal-x"></i>
          <h5>No bookings found</h5>
          <p>Adjust your search filters to find bookings.</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table tma-table mb-0 align-middle">
            <thead>
              <tr>
                <th>Booking #</th>
                <th>User ID</th>
                <th>Trek ID</th>
                <th>Booking Date</th>
                <th>Status</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="booking in filteredBookings" :key="booking.id">
                <td class="fw-bold">#{{ booking.id }}</td>
                <td class="text-muted">User #{{ booking.user_id }}</td>
                <td class="text-muted">Trek #{{ booking.trek_id }}</td>
                <td>
                  <i class="bi bi-calendar2-event text-muted me-1"></i>
                  {{ formatDate(booking.booking_date) }}
                </td>
                <td>
                  <span class="badge-status" :class="getStatusClass(booking.status)">{{ booking.status }}</span>
                </td>
                <td class="text-end">
                  <div class="dropdown d-inline-block">
                    <button
                      class="btn btn-sm btn-outline-secondary dropdown-toggle"
                      type="button"
                      data-bs-toggle="dropdown"
                      :disabled="booking.status !== 'Booked'"
                    >
                      Manage
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end shadow border-0" style="font-size: 0.85rem;">
                      <li>
                        <a class="dropdown-item py-2 text-danger" href="#"
                          @click.prevent="updateBookingStatus(booking.id, 'cancel')">
                          <i class="bi bi-x-circle me-2"></i>Cancel Booking
                        </a>
                      </li>
                      <li>
                        <a class="dropdown-item py-2 text-success" href="#"
                          @click.prevent="updateBookingStatus(booking.id, 'complete')">
                          <i class="bi bi-check-circle me-2"></i>Mark Completed
                        </a>
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
