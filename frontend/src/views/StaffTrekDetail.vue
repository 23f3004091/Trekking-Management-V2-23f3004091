<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStaffStore } from '@/stores/staff'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const route = useRoute()
const router = useRouter()
const staffStore = useStaffStore()
const showToast = inject('showToast')

const trekId = parseInt(route.params.id)
const isUpdating = ref(false)

const statusValue = ref('')
const slotsValue = ref(0)

onMounted(async () => {
  if (!staffStore.treks.length) {
    await staffStore.fetchTreks()
  }

  const trek = staffStore.treks.find(t => t.id === trekId)
  if (trek) {
    statusValue.value = trek.status
    slotsValue.value = trek.available_slots || 0
  }

  await staffStore.fetchBookingsForTrek(trekId)
  await staffStore.fetchUsersForTrek(trekId)
})

const currentTrek = computed(() => staffStore.treks.find(t => t.id === trekId))

// Merge bookings with user info (from staffStore.bookingsByTrek and staffStore.usersByTrek)
const mergedBookings = computed(() => {
  const bookings = staffStore.bookingsByTrek[trekId] || []
  const users = staffStore.usersByTrek[trekId] || []
  return bookings.map(b => {
    const user = users.find(u => u.id === b.user_id) || {}
    return { ...b, username: user.username || `User #${b.user_id}`, email: user.email || '—' }
  })
})

const getDifficultyClass = (d) => {
  if (d === 'Easy') return 'badge-easy'
  if (d === 'Moderate') return 'badge-moderate'
  if (d === 'Hard') return 'badge-hard'
  return ''
}

const getStatusClass = (s) => {
  if (!s) return ''
  const sl = s.toLowerCase()
  if (sl === 'pending') return 'badge-pending'
  if (sl === 'approved') return 'badge-approved'
  if (sl === 'open') return 'badge-open'
  if (sl === 'ongoing') return 'badge-ongoing'
  if (sl === 'closed') return 'badge-closed'
  if (sl === 'cancelled') return 'badge-cancelled'
  if (sl === 'completed') return 'badge-completed'
  if (sl === 'booked') return 'badge-booked'
  if (sl === 'cancelled') return 'badge-cancelled'
  return ''
}

const updateTrek = async () => {
  isUpdating.value = true
  try {
    const result = await staffStore.updateTrekStatus(trekId, {
      status: statusValue.value,
      available_slots: slotsValue.value
    })
    if (result.success) {
      showToast('Trek updated successfully', 'success')
    } else {
      showToast(result.message || 'Update failed', 'error')
    }
  } catch (err) {
    showToast('Failed to update trek', 'error')
  } finally {
    isUpdating.value = false
  }
}

const updateBooking = async (bookingId, newStatus) => {
  try {
    const result = await staffStore.updateBookingStatus(bookingId, trekId, newStatus)
    if (result.success) {
      showToast('Booking updated', 'success')
    } else {
      showToast(result.message || 'Update failed', 'error')
    }
  } catch (err) {
    showToast('Failed to update booking', 'error')
  }
}

const formatDate = (d) => {
  if (!d) return 'N/A'
  return new Date(d).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="staff-trek-detail">
    <!-- Back button -->
    <button class="btn btn-sm btn-outline-secondary mb-3" @click="router.push('/staff')">
      <i class="bi bi-arrow-left me-1"></i> Back to Dashboard
    </button>

    <!-- Not found state -->
    <div v-if="!currentTrek && !staffStore.isLoading" class="empty-state">
      <i class="bi bi-exclamation-triangle"></i>
      <h5>Trek Not Found</h5>
      <p>This trek does not exist or you don't have permission to view it.</p>
      <button class="btn btn-tma mt-3" @click="router.push('/staff')">Go Back</button>
    </div>

    <!-- Loading initial -->
    <div v-else-if="!currentTrek && staffStore.isLoading">
      <LoadingSpinner message="Loading trek details..." />
    </div>

    <!-- Trek Found -->
    <div v-else-if="currentTrek">
      <div class="page-header">
        <h2>
          <i class="bi bi-map me-2 text-primary"></i>{{ currentTrek.trek_name }}
        </h2>
        <p>
          <i class="bi bi-geo-alt-fill me-1 text-primary"></i>{{ currentTrek.location }}
          &nbsp;·&nbsp;
          <span class="badge-status" :class="getStatusClass(currentTrek.status)">{{ currentTrek.status }}</span>
        </p>
      </div>

      <div class="row g-4">
        <!-- Trek Info & Update Form -->
        <div class="col-lg-4">
          <!-- Trek Details Card -->
          <div class="tma-card mb-4">
            <div class="card-header-custom">
              <h5 class="mb-0"><i class="bi bi-info-circle me-2"></i>Trek Info</h5>
            </div>
            <div class="card-body p-4">
              <ul class="list-unstyled mb-0">
                <li class="d-flex align-items-center gap-2 py-2" style="border-bottom: 1px solid #f0f4f2;">
                  <i class="bi bi-compass-fill text-primary"></i>
                  <span class="text-muted small">Trek Name</span>
                  <span class="ms-auto fw-semibold small">{{ currentTrek.trek_name }}</span>
                </li>
                <li class="d-flex align-items-center gap-2 py-2" style="border-bottom: 1px solid #f0f4f2;">
                  <i class="bi bi-geo-alt-fill text-primary"></i>
                  <span class="text-muted small">Location</span>
                  <span class="ms-auto fw-semibold small">{{ currentTrek.location }}</span>
                </li>
                <li class="d-flex align-items-start gap-2 py-2" style="border-bottom: 1px solid #f0f4f2;">
                  <i class="bi bi-card-text text-primary mt-1"></i>
                  <span class="text-muted small">Description</span>
                  <span class="ms-auto fw-semibold small text-end" style="max-width: 60%;">{{ currentTrek.description || 'N/A' }}</span>
                </li>
                <li class="d-flex align-items-center gap-2 py-2" style="border-bottom: 1px solid #f0f4f2;">
                  <i class="bi bi-bar-chart-fill text-warning"></i>
                  <span class="text-muted small">Difficulty</span>
                  <span class="ms-auto">
                    <span class="badge-status" :class="getDifficultyClass(currentTrek.difficulty)">{{ currentTrek.difficulty }}</span>
                  </span>
                </li>
                <li class="d-flex align-items-center gap-2 py-2" style="border-bottom: 1px solid #f0f4f2;">
                  <i class="bi bi-people-fill text-success"></i>
                  <span class="text-muted small">Slots</span>
                  <span class="ms-auto fw-semibold small">{{ currentTrek.available_slots }} available</span>
                </li>
                <li class="d-flex align-items-center gap-2 py-2" style="border-bottom: 1px solid #f0f4f2;">
                  <i class="bi bi-calendar-event text-primary"></i>
                  <span class="text-muted small">Start</span>
                  <span class="ms-auto fw-semibold small">{{ formatDate(currentTrek.start_date) }}</span>
                </li>
                <li class="d-flex align-items-center gap-2 py-2" style="border-bottom: 1px solid #f0f4f2;">
                  <i class="bi bi-calendar-check text-accent"></i>
                  <span class="text-muted small">End</span>
                  <span class="ms-auto fw-semibold small">{{ formatDate(currentTrek.end_date) }}</span>
                </li>
                <li class="d-flex align-items-center gap-2 py-2">
                  <i class="bi bi-circle-fill" style="font-size: 0.5rem; color: var(--primary);"></i>
                  <span class="text-muted small">Status</span>
                  <span class="ms-auto">
                    <span class="badge-status" :class="getStatusClass(currentTrek.status)">{{ currentTrek.status }}</span>
                  </span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Update Trek Status Form (Staff only: Ongoing / Completed) -->
          <div class="tma-card">
            <div class="card-header-custom">
              <h5 class="mb-0"><i class="bi bi-pencil-square me-2"></i>Update Trek Status</h5>
            </div>
            <div class="card-body p-4">
              <!-- Informational note for staff -->
              <div class="alert alert-info py-2 px-3 mb-3" style="font-size:0.85rem; border-radius:8px;">
                <i class="bi bi-info-circle me-1"></i>
                As staff, you can mark this trek as <strong>Ongoing</strong> (started) or <strong>Completed</strong>.
                Trek approval and cancellation are managed by the Admin.
              </div>
              <form @submit.prevent="updateTrek" class="tma-form">
                <div class="mb-3">
                  <label class="form-label">Trek Status</label>
                  <select class="form-select" v-model="statusValue"
                    :disabled="currentTrek.status === 'Completed' || currentTrek.status === 'Cancelled' || currentTrek.status === 'Pending'">
                    <option :value="currentTrek.status" hidden>{{ currentTrek.status }}</option>
                    <!-- Mark as Ongoing: only from Approved or Open -->
                    <option value="Ongoing"
                      v-if="currentTrek.status === 'Approved' || currentTrek.status === 'Open'">
                       Mark as Ongoing (Started)
                    </option>
                    <!-- Mark as Completed: only from Ongoing -->
                    <option value="Completed"
                      v-if="currentTrek.status === 'Ongoing' || currentTrek.status === 'Open'">
                       Mark as Completed
                    </option>
                  </select>
                  <div v-if="currentTrek.status === 'Pending'" class="form-text text-warning mt-1">
                    <i class="bi bi-hourglass-split me-1"></i>Trek is Pending admin approval.
                  </div>
                  <div v-if="currentTrek.status === 'Cancelled'" class="form-text text-danger mt-1">
                    <i class="bi bi-x-circle me-1"></i>This trek has been cancelled by admin.
                  </div>
                </div>
                <div class="mb-4">
                  <label class="form-label">Available Slots</label>
                  <input type="number" class="form-control" v-model="slotsValue" min="0"
                    :disabled="currentTrek.status === 'Completed' || currentTrek.status === 'Cancelled'">
                </div>
                <button type="submit" class="btn btn-tma w-100"
                  :disabled="isUpdating || currentTrek.status === 'Completed' || currentTrek.status === 'Cancelled' || currentTrek.status === 'Pending'">
                  <span v-if="isUpdating" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="bi bi-save me-2"></i>
                  {{ isUpdating ? 'Saving...' : 'Save Changes' }}
                </button>
              </form>
            </div>
          </div>
        </div>

        <!-- Participants Table -->
        <div class="col-lg-8">
          <div class="tma-card">
            <div class="card-header-custom d-flex justify-content-between align-items-center">
              <h5 class="mb-0"><i class="bi bi-people me-2"></i>Registered Participants</h5>
              <span class="badge bg-light text-dark rounded-pill px-3">{{ mergedBookings.length }}</span>
            </div>
            <div class="card-body p-0">
              <div v-if="staffStore.isLoading" class="py-5">
                <LoadingSpinner message="Loading participants..." />
              </div>
              <div v-else-if="mergedBookings.length === 0" class="empty-state">
                <i class="bi bi-people"></i>
                <h5>No participants yet</h5>
                <p>No one has booked this trek yet.</p>
              </div>
              <div v-else class="table-responsive">
                <table class="table tma-table mb-0 align-middle">
                  <thead>
                    <tr>
                      <th>Booking #</th>
                      <th>Participant</th>
                      <th>Trek / Location</th>
                      <th>Booked On</th>
                      <th>Status</th>
                      <th class="text-end">Update</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="booking in mergedBookings" :key="booking.id">
                      <td class="fw-bold text-muted">#{{ booking.id }}</td>
                      <td>
                        <div class="d-flex align-items-center gap-2">
                          <div class="d-flex align-items-center justify-content-center rounded-circle"
                            style="width:30px;height:30px;background:rgba(45,106,79,0.1);font-size:0.8rem;font-weight:700;color:var(--primary);">
                            {{ booking.username.charAt(0).toUpperCase() }}
                          </div>
                          <div>
                            <div class="fw-semibold small">{{ booking.username }}</div>
                            <div class="small text-muted">{{ booking.email }}</div>
                          </div>
                        </div>
                      </td>
                      <td>
                        <div class="fw-semibold small">{{ booking.trek_name || '—' }}</div>
                        <div class="small text-muted">
                          <i class="bi bi-geo-alt-fill text-primary me-1"></i>{{ booking.location || '—' }}
                        </div>
                      </td>
                      <td class="small text-nowrap">
                        <div>
                          <i class="bi bi-calendar2-event text-muted me-1"></i>
                          {{ formatDate(booking.booking_date) }}
                        </div>
                      </td>
                      <td>
                        <span class="badge-status" :class="getStatusClass(booking.status)">{{ booking.status }}</span>
                      </td>
                      <td class="text-end">
                        <select
                          class="form-select form-select-sm d-inline-block w-auto"
                          :value="booking.status"
                          @change="updateBooking(booking.id, $event.target.value)"
                          style="font-size: 0.8rem;"
                          :disabled="booking.status === 'Completed' || booking.status === 'Cancelled'"
                        >
                          <option :value="booking.status" hidden>{{ booking.status }}</option>
                          <option value="Booked" v-if="booking.status !== 'Booked'">Booked</option>
                          <option value="Cancelled" v-if="booking.status !== 'Cancelled'">Cancelled</option>
                          <option value="Completed" v-if="booking.status !== 'Completed'">Completed</option>
                        </select>
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