<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { useAdminStore } from '@/stores/admin'
import StatCard from '@/components/StatCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const adminStore = useAdminStore()
const showToast = inject('showToast')

const approvingId = ref(null)

const pendingStaff = computed(() =>
  (adminStore.staffList || []).filter(s => s.status === 'Pending')
)

const handleApprove = async (staffId) => {
  approvingId.value = staffId
  try {
    await adminStore.approveStaff(staffId)
    showToast('Staff member approved successfully!', 'success')
  } catch {
    showToast('Failed to approve staff', 'error')
  } finally {
    approvingId.value = null
  }
}

onMounted(() => {
  adminStore.fetchSummary()
  adminStore.fetchStaff()
})
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="admin-dashboard">
    <!-- Page Header -->
    <div class="page-header d-flex justify-content-between align-items-start">
      <div>
        <h2>
          <i class="bi bi-speedometer2 me-2 text-primary"></i>Admin Dashboard
        </h2>
        <p>Platform-wide overview and quick actions</p>
      </div>
      <div class="text-muted small">
        <i class="bi bi-clock me-1"></i>
        {{ new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}
      </div>
    </div>

    <!-- Loading -->
    <div v-if="adminStore.isLoading">
      <LoadingSpinner message="Loading dashboard..." />
    </div>

    <div v-else>
      <!-- Stat Cards -->
      <div class="row g-4 mb-4 stagger-children">
        <div class="col-sm-6 col-xl-3">
          <StatCard
            title="Total Treks"
            :value="adminStore.summary?.total_treks || 0"
            icon="compass"
            color="green"
          />
        </div>
        <div class="col-sm-6 col-xl-3">
          <StatCard
            title="Total Trekkers"
            :value="adminStore.summary?.total_trekkers || 0"
            icon="people"
            color="blue"
          />
        </div>
        <div class="col-sm-6 col-xl-3">
          <StatCard
            title="Total Staff"
            :value="adminStore.summary?.total_staff || 0"
            icon="person-badge"
            color="gold"
          />
        </div>
        <div class="col-sm-6 col-xl-3">
          <StatCard
            title="Total Bookings"
            :value="adminStore.summary?.total_bookings || 0"
            icon="journal-check"
            color="orange"
          />
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="row g-4">
        <div class="col-lg-8">
          <div class="tma-card h-100">
            <div class="card-header-custom d-flex align-items-center">
              <i class="bi bi-lightning-charge-fill me-2 fs-5"></i>
              <h5 class="mb-0">Quick Actions</h5>
            </div>
            <div class="card-body p-4">
              <div class="row g-3">
                <div class="col-md-6">
                  <router-link to="/admin/treks" class="d-flex align-items-center gap-3 p-3 rounded-3 text-decoration-none"
                    style="background: var(--tma-primary-light); border: 1px solid var(--tma-primary-alpha20); transition: all 0.2s;"
                    onmouseover="this.style.background='#e0e7ff'"
                    onmouseout="this.style.background='var(--tma-primary-light)'">
                    <div class="d-flex align-items-center justify-content-center rounded-2"
                      style="width:44px;height:44px;background:#ffffff; border: 1px solid var(--tma-border);">
                      <i class="bi bi-compass-fill fs-5" style="color:var(--tma-primary);"></i>
                    </div>
                    <div>
                      <div class="fw-semibold" style="color:var(--tma-dark);">Manage Treks</div>
                      <div class="small text-muted">Create, edit & manage treks</div>
                    </div>
                    <i class="bi bi-chevron-right ms-auto text-muted"></i>
                  </router-link>
                </div>
                <div class="col-md-6">
                  <router-link to="/admin/staff" class="d-flex align-items-center gap-3 p-3 rounded-3 text-decoration-none"
                    style="background: var(--tma-info-light); border: 1px solid rgba(2, 132, 199, 0.2); transition: all 0.2s;"
                    onmouseover="this.style.background='#bae6fd'"
                    onmouseout="this.style.background='var(--tma-info-light)'">
                    <div class="d-flex align-items-center justify-content-center rounded-2"
                      style="width:44px;height:44px;background:#ffffff; border: 1px solid var(--tma-border);">
                      <i class="bi bi-person-badge-fill fs-5" style="color:var(--tma-sky-dark);"></i>
                    </div>
                    <div>
                      <div class="fw-semibold" style="color:var(--tma-dark);">Manage Staff</div>
                      <div class="small text-muted">Approve & manage staff</div>
                    </div>
                    <i class="bi bi-chevron-right ms-auto text-muted"></i>
                  </router-link>
                </div>
                <div class="col-md-6">
                  <router-link to="/admin/users" class="d-flex align-items-center gap-3 p-3 rounded-3 text-decoration-none"
                    style="background: var(--tma-warning-light); border: 1px solid rgba(217, 119, 6, 0.2); transition: all 0.2s;"
                    onmouseover="this.style.background='#fde68a'"
                    onmouseout="this.style.background='var(--tma-warning-light)'">
                    <div class="d-flex align-items-center justify-content-center rounded-2"
                      style="width:44px;height:44px;background:#ffffff; border: 1px solid var(--tma-border);">
                      <i class="bi bi-people-fill fs-5" style="color:var(--tma-gold);"></i>
                    </div>
                    <div>
                      <div class="fw-semibold" style="color:var(--tma-dark);">Manage Users</div>
                      <div class="small text-muted">View & moderate trekkers</div>
                    </div>
                    <i class="bi bi-chevron-right ms-auto text-muted"></i>
                  </router-link>
                </div>
                <div class="col-md-6">
                  <router-link to="/admin/bookings" class="d-flex align-items-center gap-3 p-3 rounded-3 text-decoration-none"
                    style="background: var(--tma-accent-light); border: 1px solid rgba(13, 148, 136, 0.2); transition: all 0.2s;"
                    onmouseover="this.style.background='#99f6e4'"
                    onmouseout="this.style.background='var(--tma-accent-light)'">
                    <div class="d-flex align-items-center justify-content-center rounded-2"
                      style="width:44px;height:44px;background:#ffffff; border: 1px solid var(--tma-border);">
                      <i class="bi bi-journal-check-fill fs-5" style="color:var(--tma-accent);"></i>
                    </div>
                    <div>
                      <div class="fw-semibold" style="color:var(--tma-dark);">All Bookings</div>
                      <div class="small text-muted">Monitor reservations</div>
                    </div>
                    <i class="bi bi-chevron-right ms-auto text-muted"></i>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Platform Summary -->
        <div class="col-lg-4">
          <div class="tma-card h-100">
            <div class="card-header-custom">
              <h5 class="mb-0"><i class="bi bi-bar-chart-fill me-2"></i>Platform Summary</h5>
            </div>
            <div class="card-body p-4">
              <div class="d-flex justify-content-between align-items-center py-3" style="border-bottom: 1px solid var(--tma-border);">
                <div class="d-flex align-items-center gap-2">
                  <i class="bi bi-compass text-primary"></i>
                  <span class="small fw-semibold text-secondary">Total Treks</span>
                </div>
                <span class="fw-bold">{{ adminStore.summary?.total_treks || 0 }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center py-3" style="border-bottom: 1px solid var(--tma-border);">
                <div class="d-flex align-items-center gap-2">
                  <i class="bi bi-people" style="color:var(--tma-sky-dark);"></i>
                  <span class="small fw-semibold text-secondary">Trekkers</span>
                </div>
                <span class="fw-bold">{{ adminStore.summary?.total_trekkers || 0 }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center py-3" style="border-bottom: 1px solid var(--tma-border);">
                <div class="d-flex align-items-center gap-2">
                  <i class="bi bi-person-badge" style="color:var(--tma-gold);"></i>
                  <span class="small fw-semibold text-secondary">Staff</span>
                </div>
                <span class="fw-bold">{{ adminStore.summary?.total_staff || 0 }}</span>
              </div>
              <div class="d-flex justify-content-between align-items-center py-3">
                <div class="d-flex align-items-center gap-2">
                  <i class="bi bi-journal-check" style="color:var(--tma-accent);"></i>
                  <span class="small fw-semibold text-secondary">Bookings</span>
                </div>
                <span class="fw-bold">{{ adminStore.summary?.total_bookings || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Pending Staff Approvals -->
      <div class="row g-4 mt-1">
        <div class="col-12">
          <div class="tma-card">
            <div class="card-header-custom d-flex align-items-center justify-content-between">
              <div class="d-flex align-items-center">
                <i class="bi bi-person-check-fill me-2 fs-5" style="color:var(--tma-gold);"></i>
                <h5 class="mb-0">Pending Staff Approvals</h5>
                <span v-if="pendingStaff.length > 0"
                  class="ms-2 badge rounded-pill"
                  style="background:var(--tma-warning-light);color:var(--tma-gold);font-size:0.75rem;padding:0.3em 0.65em;border:1px solid rgba(217,119,6,0.25);">
                  {{ pendingStaff.length }}
                </span>
              </div>
              <router-link to="/admin/staff" class="btn btn-sm btn-outline-secondary" style="font-size:0.8rem;">
                <i class="bi bi-arrow-right me-1"></i>View All Staff
              </router-link>
            </div>

            <div class="card-body p-0">
              <!-- Empty state -->
              <div v-if="!adminStore.isLoading && pendingStaff.length === 0"
                class="d-flex flex-column align-items-center justify-content-center py-5 text-muted">
                <i class="bi bi-patch-check-fill fs-2 mb-2" style="color:#86efac;"></i>
                <p class="mb-0 small fw-semibold">No pending approvals — all caught up!</p>
              </div>

              <!-- Loading -->
              <div v-else-if="adminStore.isLoading" class="py-4">
                <LoadingSpinner message="Loading staff..." />
              </div>

              <!-- Table -->
              <div v-else class="table-responsive">
                <table class="table tma-table mb-0 align-middle">
                  <thead>
                    <tr>
                      <th>Profile ID</th>
                      <th>User ID</th>
                      <th>Contact Details</th>
                      <th>Status</th>
                      <th class="text-end">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="staff in pendingStaff" :key="staff.id">
                      <td class="text-muted fw-medium">#{{ staff.id }}</td>
                      <td class="fw-semibold">User #{{ staff.user_id }}</td>
                      <td>{{ staff.contact_details || '—' }}</td>
                      <td>
                        <span class="badge-status badge-pending">
                          <i class="bi bi-hourglass-split me-1"></i>Pending
                        </span>
                      </td>
                      <td class="text-end">
                        <button
                          class="btn btn-sm btn-outline-success"
                          :id="`approve-staff-${staff.id}`"
                          :disabled="approvingId === staff.id"
                          @click="handleApprove(staff.id)"
                        >
                          <span v-if="approvingId === staff.id"
                            class="spinner-border spinner-border-sm me-1"
                            role="status" aria-hidden="true"></span>
                          <i v-else class="bi bi-check-circle me-1"></i>
                          {{ approvingId === staff.id ? 'Approving…' : 'Approve' }}
                        </button>
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
