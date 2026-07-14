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

const formData = ref({
  username: '',
  email: '',
  password: '',
  contact_details: ''
})

onMounted(() => {
  adminStore.fetchStaff()
})

const filteredStaff = computed(() => {
  const q = searchQuery.value.toLowerCase()
  return (adminStore.staffList || []).filter(s =>
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



const handleAddStaff = async () => {
  isSubmitting.value = true
  try {
    await apiClient.post('/auth/register-staff', formData.value)
    showToast('Staff registered successfully', 'success')
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
    </div>

    <SearchBar
      placeholder="Search staff by contact, status, or User ID..."
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
                <th>User ID</th>
                <th>Contact Details</th>
                <th>Status</th>
                <th>Blacklisted</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="staff in filteredStaff" :key="staff.id">
                <td class="text-muted fw-medium">#{{ staff.id }}</td>
                <td class="fw-semibold">User #{{ staff.user_id }}</td>
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


  </div>
</template>
