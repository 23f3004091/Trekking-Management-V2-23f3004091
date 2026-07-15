<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useAdminStore } from '@/stores/admin'
import SearchBar from '@/components/SearchBar.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const showBlacklistModal = ref(false)

const adminStore = useAdminStore()
const showToast = inject('showToast')

const searchQuery = ref('')
const userToBlacklist = ref(null)

onMounted(() => {
  adminStore.fetchTrekkers()
})

const filteredTrekkers = computed(() => {
  const q = searchQuery.value.toLowerCase()
  return (adminStore.trekkerList || []).filter(t =>
    t.id?.toString().includes(q) ||
    t.user_id?.toString().includes(q) ||
    t.username?.toLowerCase().includes(q) ||
    t.email?.toLowerCase().includes(q) ||
    t.full_name?.toLowerCase().includes(q) ||
    t.age?.toString().includes(q)
  )
})

const executeBlacklist = async (id) => {
  try {
    await adminStore.blacklistTrekker(id)
    showToast('User blacklist status updated', 'success')
  } catch (err) {
    showToast('Failed to blacklist user', 'error')
  }
}
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="admin-users">
    <div class="page-header">
      <h2><i class="bi bi-people me-2 text-primary"></i>Manage Users (Trekkers)</h2>
      <p>View all registered trekkers and manage their account status</p>
    </div>

    <SearchBar
      placeholder="Search by username, name, email, ID, or age..."
      @search="q => searchQuery = q"
    />

    <div class="tma-card">
      <div class="card-body p-0">
        <div v-if="adminStore.isLoading" class="py-5">
          <LoadingSpinner message="Loading trekkers..." />
        </div>
        <div v-else-if="filteredTrekkers.length === 0" class="empty-state">
          <i class="bi bi-person-slash"></i>
          <h5>No trekkers found</h5>
          <p>Wait for new users to register on the platform.</p>
        </div>
        <div v-else class="table-responsive">
          <table class="table tma-table mb-0 align-middle">
            <thead>
              <tr>
                <th>#</th>
                <th>Trekker</th>
                <th>Contact</th>
                <th>Age</th>
                <th>Emergency Contact</th>
                <th>Status</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trekker in filteredTrekkers" :key="trekker.id">
                <td class="text-muted fw-medium small">#{{ trekker.id }}</td>
                <td>
                  <div class="d-flex align-items-center gap-2">
                    <div class="d-flex align-items-center justify-content-center rounded-circle fw-bold"
                      style="width:34px;height:34px;background:var(--tma-primary-light);color:var(--tma-primary);font-size:0.85rem;flex-shrink:0;">
                      {{ (trekker.full_name || trekker.username || '?').charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <div class="fw-semibold small">{{ trekker.full_name || '—' }}</div>
                      <div class="text-muted" style="font-size:0.78rem;">
                        <i class="bi bi-person me-1"></i>{{ trekker.username }}
                        <span class="mx-1">·</span>
                        <i class="bi bi-envelope me-1"></i>{{ trekker.email || '—' }}
                      </div>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="small">
                    <i class="bi bi-telephone-fill text-primary me-1"></i>
                    {{ trekker.phone || '—' }}
                  </div>
                </td>
                <td class="text-center fw-semibold small">{{ trekker.age || '—' }}</td>
                <td>
                  <span class="small text-muted">{{ trekker.emergency_contact || '—' }}</span>
                </td>
                <td>
                  <span class="badge-status" :class="trekker.blacklisted ? 'badge-closed' : 'badge-open'">
                    <i class="bi me-1" :class="trekker.blacklisted ? 'bi-ban' : 'bi-check-circle'"></i>
                    {{ trekker.blacklisted ? 'Blacklisted' : 'Active' }}
                  </span>
                </td>
                <td class="text-end">
                  <button
                    class="btn btn-sm"
                    :class="trekker.blacklisted ? 'btn-outline-secondary' : 'btn-outline-danger'"
                    @click="executeBlacklist(trekker.id)"
                  >
                    <i class="bi bi-ban me-1"></i>
                    {{ trekker.blacklisted ? 'Unblacklist' : 'Blacklist' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <ConfirmModal
      id="blacklistConfirmModal"
      v-model="showBlacklistModal"
      title="Blacklist Trekker"
      message="Are you sure you want to blacklist this user? They will be restricted from the platform."
      confirmText="Blacklist User"
      confirmClass="btn-danger"
      @confirm="executeBlacklist"
    />
  </div>
</template>
