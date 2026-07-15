<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useAdminStore } from '@/stores/admin'
import SearchBar from '@/components/SearchBar.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const showTrekModal = ref(false)
const showDeleteModal = ref(false)

const adminStore = useAdminStore()
const showToast = inject('showToast')

const searchQuery = ref('')
const activeFilters = ref({ difficulty: 'All', status: 'All' })
const trekToDelete = ref(null)

const isEditing = ref(false)
const currentTrekId = ref(null)
const isSubmitting = ref(false)


const formData = ref({
  trek_name: '',
  location: '',
  difficulty: 'Easy',
  available_slots: 10,
  start_date: '',
  end_date: '',
  staff_name: '',
  description: ''
})

onMounted(() => {
  adminStore.fetchTreks()
  adminStore.fetchStaff()
})

const filteredTreks = computed(() => {
  return (adminStore.trekList || []).filter(trek => {
    const q = searchQuery.value.toLowerCase()
    const matchQuery = (trek.trek_name?.toLowerCase().includes(q)) ||
                       (trek.location?.toLowerCase().includes(q))
    const matchDifficulty = activeFilters.value.difficulty === 'All' || trek.difficulty === activeFilters.value.difficulty
    const matchStatus = activeFilters.value.status === 'All' || trek.status === activeFilters.value.status
    return matchQuery && matchDifficulty && matchStatus
  })
})

const staffList = computed(() => {
  return (adminStore.staffList || []).map(s => {
    return { id: s.id, username: s.username, email: s.email }
  })
})


console.log(staffList.value)
const handleSearch = (q) => { searchQuery.value = q }
const handleFilter = (f) => { activeFilters.value = { ...activeFilters.value, ...f } }

const getDifficultyClass = (d) => {
  if (d === 'Easy') return 'badge-easy'
  if (d === 'Moderate') return 'badge-moderate'
  if (d === 'Hard') return 'badge-hard'
  return ''
}

// Format ISO-8601 UTC string to date-only label for the table
const formatDateOnly = (d) => {
  if (!d) return 'N/A'
  return new Date(d).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}

// Convert ISO-8601 UTC string to local 'YYYY-MM-DDTHH:MM' string
// for use with <input type="datetime-local">, which expects local time.
const toLocalInputValue = (isoUtcStr) => {
  if (!isoUtcStr) return ''
  const d = new Date(isoUtcStr)
  // Shift by timezone offset to get local time as a 'YYYY-MM-DDTHH:MM' string
  const offset = d.getTimezoneOffset() * 60000
  return new Date(d.getTime() - offset).toISOString().slice(0, 16)
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
  return ''
}

const openCreateModal = () => {
  isEditing.value = false
  currentTrekId.value = null
  formData.value = {
    trek_name: '', location: '', difficulty: 'Easy',
    available_slots: 10, start_date: '', end_date: '', staff_name: '', description : ''
  }
  showTrekModal.value = true
}

const openEditModal = (trek) => {
  isEditing.value = true
  currentTrekId.value = trek.id
  formData.value = {
    trek_name: trek.trek_name,
    location: trek.location,
    difficulty: trek.difficulty,
    available_slots: trek.available_slots || 0,
    start_date: toLocalInputValue(trek.start_date),
    end_date: toLocalInputValue(trek.end_date),
    staff_name: trek.staff_name || '',
    description: trek.description || ''
  }
  showTrekModal.value = true
}

const handleSaveTrek = async () => {
  isSubmitting.value = true
  try {
    if (isEditing.value) {
      if (formData.value.start_date < formData.value.end_date) {
        await adminStore.updateTrek(currentTrekId.value, formData.value)
      showToast(`Trek ${isEditing.value ? 'updated' : 'created'} successfully`, 'success')

      } else {
        showToast('Start date must be before end date', 'error')
      }
    } else {
      if (formData.value.start_date < formData.value.end_date) {
        await adminStore.createTrek(formData.value)
      showToast(`Trek ${isEditing.value ? 'updated' : 'created'} successfully`, 'success')

      } else {
        showToast('Start date must be before end date', 'error')
      }
    }
    showTrekModal.value = false
    await adminStore.fetchTreks()
  } catch (err) {
    showToast(err.response?.data?.error || 'Operation failed', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const confirmDelete = (id) => {
  trekToDelete.value = id
  showDeleteModal.value = true
}

const executeDelete = async () => {
  if (!trekToDelete.value) return
  try {
    await adminStore.deleteTrek(trekToDelete.value)
    showToast('Trek deleted successfully', 'success')
  } catch (err) {
    showToast('Failed to delete trek', 'error')
  }
}

const updateStatus = async (id, action) => {
  try {
    await adminStore.manageTrekStatus(id, action)
    showToast(`Trek ${action}d successfully`, 'success')
  } catch (err) {
    showToast('Failed to update status', 'error')
  }
}

// console.log()
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="admin-treks">
    <div class="page-header d-flex justify-content-between align-items-start flex-wrap gap-3">
      <div>
        <h2><i class="bi bi-compass me-2 text-primary"></i>Manage Treks</h2>
        <p>Create, update, and manage all trekking routes</p>
      </div>
      <button class="btn btn-tma" @click="openCreateModal" id="create-trek-btn">
        <i class="bi bi-plus-lg me-1"></i> Create Trek
      </button>
    </div>

    <SearchBar
      placeholder="Search treks by name or location..."
      :filters="[
        { key: 'difficulty', label: 'Difficulty', options: ['All', 'Easy', 'Moderate', 'Hard'] },
        { key: 'status', label: 'Status', options: ['All', 'Pending', 'Approved', 'Open', 'Ongoing', 'Closed', 'Cancelled', 'Completed'] }
      ]"
      @search="handleSearch"
      @filter="handleFilter"
    />

    <div class="tma-card">
      <div class="card-body p-0">
        <div v-if="adminStore.isLoading" class="py-5 text-center">
          <LoadingSpinner message="Loading treks..." />
        </div>
        <div v-else-if="filteredTreks.length === 0" class="empty-state">
          <i class="bi bi-compass"></i>
          <h5>No treks found</h5>
          <p>Adjust your search filters or create your first trek.</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table tma-table mb-0 align-middle">
            <thead>
              <tr>
                <th>#</th>
                <th>Trek Name</th>
                <th>Location</th>
                <th>Difficulty</th>
                <th>Assigned Staff</th>
                <th>Slots</th>
                <th>Date</th>
                <th>Status</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trek in filteredTreks" :key="trek.id">
                <td class="text-muted fw-medium">{{ trek.id }}</td>
                <td class="fw-semibold">{{ trek.trek_name }}</td>
                <td>
                  <i class="bi bi-geo-alt-fill text-primary me-1"></i>
                  {{ trek.location }}
                </td>
                <td>
                  <span class="badge-status" :class="getDifficultyClass(trek.difficulty)">
                    {{ trek.difficulty }}
                  </span>
                </td>
                <td>
                  <span class="badge-status" :class="getDifficultyClass(trek.difficulty)">
                    {{ trek.staff_name ?? 'Unassigned' }}
                  </span>
                  
                </td>
                <td>
                  <i class="bi bi-people-fill text-muted me-1"></i>
                  {{ trek.available_slots ?? 'N/A' }}
                </td>
                <td class="align-middle text-nowrap">
                  <div class="d-flex flex-column">
                    <div class="small">
                      <i class="bi bi-calendar-event text-primary me-1"></i>
                      {{ formatDateOnly(trek.start_date) }}
                    </div>
                    <div class="small text-muted">
                      <i class="bi bi-arrow-right me-1"></i>
                      {{ formatDateOnly(trek.end_date) }}
                    </div>
                  </div>
                </td>
                <td>
                  <span class="badge-status" :class="getStatusClass(trek.status)">{{ trek.status }}</span>
                </td>
                <td class="text-end">
                  <div class="d-flex justify-content-end gap-1 flex-wrap">
                    <!-- Admin Status Dropdown: Approve or Cancel only -->
                    <div class="dropdown">
                      <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                        :disabled="trek.status === 'Completed' || trek.status === 'Cancelled'">
                        <i class="bi bi-gear-fill me-1"></i>
                        {{ trek.status === 'Completed' ? 'Completed' : trek.status === 'Cancelled' ? 'Cancelled' : 'Status' }}
                      </button>
                      <ul class="dropdown-menu dropdown-menu-end shadow border-0" style="font-size: 0.85rem; min-width: 160px;">
                        <!-- Approve: only when Pending -->
                        <li v-if="trek.status === 'Pending'">
                          <a class="dropdown-item py-2" href="#" @click.prevent="updateStatus(trek.id, 'approve')">
                            <i class="bi bi-check-circle me-2 text-info"></i>Approve
                          </a>
                        </li>
                        <li v-if="trek.status === 'Pending'"><hr class="dropdown-divider my-1"></li>
                        <!-- Cancel: available unless already Completed -->
                        <li v-if="trek.status !== 'Completed' && trek.status !== 'Cancelled'">
                          <a class="dropdown-item py-2 text-danger" href="#" @click.prevent="updateStatus(trek.id, 'cancel')">
                            <i class="bi bi-x-circle me-2"></i>Cancel Trek
                          </a>
                        </li>
                      </ul>
                    </div>
                    <button class="btn btn-sm btn-outline-primary" @click="openEditModal(trek)" title="Edit" :disabled="trek.status == 'Completed'">
                      <i class="bi bi-pencil-fill"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(trek.id)" title="Delete" :disabled="trek.status == 'Completed'">
                      <i class="bi bi-trash-fill"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Create / Edit Modal -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div
          v-if="showTrekModal"
          class="confirm-modal-overlay"
          @click.self="showTrekModal = false"
          role="dialog"
          aria-modal="true"
        >
          <div class="confirm-modal-box" style="max-width: 700px;">
            <div class="confirm-modal-header">
              <h5 class="confirm-modal-title">
                <i class="bi bi-compass me-2"></i>
                {{ isEditing ? 'Edit Trek' : 'Create New Trek' }}
              </h5>
              <button type="button" class="confirm-modal-close" @click="showTrekModal = false" aria-label="Close">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>
            <div class="confirm-modal-body">
              <form class="tma-form row g-3" @submit.prevent="handleSaveTrek" id="trekForm">
                <div class="col-md-6">
                  <label class="form-label">Trek Name *</label>
                  <input type="text" class="form-control" v-model="formData.trek_name" required placeholder="e.g. Himalayan Base Camp">
                </div>
                <div class="col-md-6">
                  <label class="form-label">Location *</label>
                  <input type="text" class="form-control" v-model="formData.location" required placeholder="e.g. Himachal Pradesh">
                </div>
                <div class="col-md-12">
                  <label class="form-label">Description *</label>
                  <textarea class="form-control" v-model="formData.description" required placeholder="Describe the trek..." rows="3"></textarea>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Difficulty *</label>
                  <select class="form-select" v-model="formData.difficulty" required>
                    <option value="Easy">Easy</option>
                    <option value="Moderate">Moderate</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Available Slots *</label>
                  <input type="number" class="form-control" v-model="formData.available_slots" min="1" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Staff Username</label>
                  <select class="form-select" v-model="formData.staff_name" required>
                    <option value="">Unassigned</option>
                    <option v-for="staff in staffList" :key="staff.id" :value="staff.username">
                      {{ staff.username }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Start Date &amp; Time *</label>
                  <input type="date" class="form-control" v-model="formData.start_date" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">End Date &amp; Time *</label>
                  <input type="date" class="form-control" v-model="formData.end_date" required>
                </div>
              </form>
            </div>
            <div class="confirm-modal-footer">
              <button type="button" class="btn btn-secondary btn-sm" @click="showTrekModal = false">Cancel</button>
              <button type="submit" form="trekForm" class="btn btn-tma btn-sm" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-1"></span>
                {{ isSubmitting ? 'Saving...' : (isEditing ? 'Save Changes' : 'Create Trek') }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Delete Confirm Modal -->
    <ConfirmModal
      id="deleteConfirmModal"
      v-model="showDeleteModal"
      title="Delete Trek"
      message="Are you sure you want to permanently delete this trek? This cannot be undone."
      confirmText="Delete Trek"
      confirmClass="btn-danger"
      @confirm="executeDelete"
    />
  </div>
</template>

<style>
/* Trek form modal overlay — must be global since it's teleported to <body> */
.confirm-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1055;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}
.confirm-modal-box {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 480px;
  overflow: hidden;
}
.confirm-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #e9ecef;
}
.confirm-modal-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: #1a1a2e;
}
.confirm-modal-close {
  background: none;
  border: none;
  font-size: 1rem;
  color: #6c757d;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
  transition: color 0.2s;
}
.confirm-modal-close:hover { color: #1a1a2e; }
.confirm-modal-body {
  padding: 1.25rem;
  font-size: 0.95rem;
  color: #4a5568;
}
.confirm-modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-active .confirm-modal-box,
.modal-fade-leave-active .confirm-modal-box {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-from .confirm-modal-box,
.modal-fade-leave-to .confirm-modal-box {
  transform: scale(0.95) translateY(-10px);
  opacity: 0;
}
</style>
