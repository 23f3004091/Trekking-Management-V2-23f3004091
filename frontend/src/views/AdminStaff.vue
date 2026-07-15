<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useAdminStore } from '@/stores/admin'
import apiClient from '@/axiosApi.js'
import SearchBar from '@/components/SearchBar.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const adminStore = useAdminStore()
const showToast = inject('showToast')

const searchQuery = ref('')
const isSubmitting = ref(false)
const showStaffModal = ref(false)

const formData = ref({
  username: '',
  email: '',
  password: '',
  full_name: '',
  phone: '',
  contact_details: '',
  experience_years: '',
  specialization: '',
  bio: ''
})

const resetForm = () => {
  formData.value = {
    username: '',
    email: '',
    password: '',
    full_name: '',
    phone: '',
    contact_details: '',
    experience_years: '',
    specialization: '',
    bio: ''
  }
}

onMounted(() => {
  adminStore.fetchStaff()
})

const filteredStaff = computed(() => {
  const q = searchQuery.value.toLowerCase()
  return (adminStore.staffList || []).filter(s =>
    (s.username?.toLowerCase().includes(q)) ||
    (s.full_name?.toLowerCase().includes(q)) ||
    (s.email?.toLowerCase().includes(q)) ||
    (s.contact_details?.toLowerCase().includes(q)) ||
    (s.user_id?.toString().includes(q)) ||
    (s.status?.toLowerCase().includes(q))
  )
})

const getStatusClass = (s) => {
  if (s === 'Pending') return 'badge-pending'
  if (s === 'Approved') return 'badge-approved'
  if (s === 'Rejected') return 'badge-closed'
  return ''
}

const openAddStaffModal = () => {
  resetForm()
  showStaffModal.value = true
}

const handleAddStaff = async () => {
  isSubmitting.value = true
  try {
    await apiClient.post('/auth/register-staff', formData.value)
    showToast('Staff registered successfully', 'success')
    showStaffModal.value = false
    resetForm()
    await adminStore.fetchStaff()
  } catch (err) {
    showToast(err.response?.data?.error || 'Registration failed', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const approveStaff = async (id) => {
  try {
    await adminStore.approveStaff(id)
    showToast('Staff profile approved', 'success')
  } catch (err) {
    showToast('Failed to approve staff', 'error')
  }
}

const toggleBlacklist = async (id) => {
  try {
    await adminStore.blacklistStaff(id)
    showToast('Staff blacklist status updated', 'success')
  } catch (err) {
    showToast('Failed to update blacklist status', 'error')
  }
}
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="admin-staff">
    <div class="page-header d-flex justify-content-between align-items-start flex-wrap gap-3">
      <div>
        <h2><i class="bi bi-person-badge me-2 text-primary"></i>Manage Staff</h2>
        <p>View, approve, and manage trek staff members</p>
      </div>
      <button class="btn btn-tma" @click="openAddStaffModal" id="add-staff-btn">
        <i class="bi bi-person-plus-fill me-1"></i> Add Staff
      </button>
    </div>

    <SearchBar
      placeholder="Search staff by name, email, contact, status or User ID..."
      @search="q => searchQuery = q"
    />

    <div class="tma-card">
      <div class="card-body p-0">
        <div v-if="adminStore.isLoading" class="py-5">
          <LoadingSpinner message="Loading staff..." />
        </div>
        <div v-else-if="filteredStaff.length === 0" class="empty-state">
          <i class="bi bi-person-badge"></i>
          <h5>No staff found</h5>
          <p>Add a new staff member or adjust your search.</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table tma-table mb-0 align-middle">
            <thead>
              <tr>
                <th>Profile ID</th>
                <th>Username</th>
                <th>Full name</th>
                <th>Email</th>
                <th>Contact Details</th>
                <th>Status</th>
                <th>Blacklisted</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="staff in filteredStaff" :key="staff.id">
                <td class="text-muted fw-medium">#{{ staff.id }}</td>
                <td class="fw-semibold">{{ staff.username || `User #${staff.user_id}` }}</td>
                <td class="fw-semibold">{{ staff.full_name }}</td>
                <td class="text-muted">{{ staff.email || '—' }}</td>
                <td>{{ staff.contact_details || '—' }}</td>
                <td>
                  <span class="badge-status" :class="getStatusClass(staff.status)">{{ staff.status }}</span>
                </td>
                <td>
                  <span class="badge-status" :class="staff.blacklisted ? 'badge-closed' : 'badge-open'">
                    <i class="bi me-1" :class="staff.blacklisted ? 'bi-ban' : 'bi-check-circle'"></i>
                    {{ staff.blacklisted ? 'Yes' : 'No' }}
                  </span>
                </td>
                <td class="text-end">
                  <div class="d-flex justify-content-end gap-2">
                    <button
                      v-if="staff.status === 'Pending'"
                      class="btn btn-sm btn-outline-success"
                      @click="approveStaff(staff.id)"
                    >
                      <i class="bi bi-check-circle me-1"></i> Approve
                    </button>
                    <button
                      class="btn btn-sm"
                      :class="staff.blacklisted ? 'btn-outline-secondary' : 'btn-outline-danger'"
                      @click="toggleBlacklist(staff.id)"
                      :disabled="isSubmitting"
                    >
                      <i class="bi bi-ban me-1"></i>
                      {{ staff.blacklisted ? 'Unblacklist' : 'Blacklist' }}
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Add Staff Modal -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div
          v-if="showStaffModal"
          class="confirm-modal-overlay"
          @click.self="showStaffModal = false"
          role="dialog"
          aria-modal="true"
        >
          <div class="confirm-modal-box" style="max-width: 680px;">
            <div class="confirm-modal-header">
              <h5 class="confirm-modal-title">
                <i class="bi bi-person-plus-fill me-2"></i>Register New Staff
              </h5>
              <button type="button" class="confirm-modal-close" @click="showStaffModal = false" aria-label="Close">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>
            <div class="confirm-modal-body">
              <form class="tma-form row g-3" @submit.prevent="handleAddStaff" id="staffForm">
                <!-- Account credentials -->
                <div class="col-12">
                  <p class="section-label mb-1">
                    <i class="bi bi-key-fill me-1 text-primary"></i>
                    Account Credentials
                  </p>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Username *</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="formData.username"
                    required
                    placeholder="e.g. john_doe"
                    id="staff-username"
                  >
                </div>
                <div class="col-md-6">
                  <label class="form-label">Email *</label>
                  <input
                    type="email"
                    class="form-control"
                    v-model="formData.email"
                    required
                    placeholder="e.g. john@example.com"
                    id="staff-email"
                  >
                </div>
                <div class="col-md-6">
                  <label class="form-label">Password *</label>
                  <input
                    type="password"
                    class="form-control"
                    v-model="formData.password"
                    required
                    placeholder="Min. 6 characters"
                    id="staff-password"
                  >
                </div>
                <div class="col-md-6">
                  <label class="form-label">Full Name</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="formData.full_name"
                    placeholder="e.g. John Doe"
                    id="staff-full-name"
                  >
                </div>

                <!-- Profile details -->
                <div class="col-12 mt-1">
                  <p class="section-label mb-1">
                    <i class="bi bi-person-lines-fill me-1 text-primary"></i>
                    Profile Details
                  </p>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Phone</label>
                  <input
                    type="tel"
                    class="form-control"
                    v-model="formData.phone"
                    placeholder="e.g. +91 9876543210"
                    id="staff-phone"
                  >
                </div>
                <div class="col-md-6">
                  <label class="form-label">Contact Details</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="formData.contact_details"
                    placeholder="Additional contact info"
                    id="staff-contact-details"
                  >
                </div>
                <div class="col-md-6">
                  <label class="form-label">Years of Experience</label>
                  <input
                    type="number"
                    class="form-control"
                    v-model="formData.experience_years"
                    min="0"
                    max="50"
                    placeholder="e.g. 5"
                    id="staff-experience"
                  >
                </div>
                <div class="col-md-6">
                  <label class="form-label">Specialization</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="formData.specialization"
                    placeholder="e.g. High Altitude Trekking"
                    id="staff-specialization"
                  >
                </div>
                <div class="col-12">
                  <label class="form-label">Bio</label>
                  <textarea
                    class="form-control"
                    v-model="formData.bio"
                    rows="3"
                    placeholder="Brief description about the staff member..."
                    id="staff-bio"
                  ></textarea>
                </div>
              </form>
            </div>
            <div class="confirm-modal-footer">
              <button type="button" class="btn btn-secondary btn-sm" @click="showStaffModal = false">Cancel</button>
              <button type="submit" form="staffForm" class="btn btn-tma btn-sm" :disabled="isSubmitting" id="submit-staff-btn">
                <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                <i v-else class="bi bi-person-check-fill me-1"></i>
                {{ isSubmitting ? 'Registering...' : 'Register Staff' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

  </div>
</template>

<style scoped>
.section-label {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--tma-muted, #6c757d);
}
</style>

<style>
/* Modal styles - global since teleported to body */
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
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}
.confirm-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #e9ecef;
  flex-shrink: 0;
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
  overflow-y: auto;
}
.confirm-modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
  flex-shrink: 0;
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
