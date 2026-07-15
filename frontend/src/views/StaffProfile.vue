<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useStaffStore } from '@/stores/staff'

const authStore = useAuthStore()
const staffStore = useStaffStore()

const isEditing = ref(false)
const isSaving = ref(false)
const saveMessage = ref('')
const saveError = ref('')

const editForm = ref({
  full_name: '',
  phone: '',
  contact_details: '',
  experience_years: '',
  specialization: '',
  bio: ''
})

onMounted(async () => {
  await Promise.all([staffStore.fetchProfile(), staffStore.fetchSummary()])
  if (staffStore.profile) {
    populateForm()
  }
})

function populateForm() {
  const p = staffStore.profile
  editForm.value = {
    full_name: p.full_name || '',
    phone: p.phone || '',
    contact_details: p.contact_details || '',
    experience_years: p.experience_years ?? '',
    specialization: p.specialization || '',
    bio: p.bio || ''
  }
}

function startEdit() {
  populateForm()
  isEditing.value = true
  saveMessage.value = ''
  saveError.value = ''
}

function cancelEdit() {
  isEditing.value = false
}

async function saveProfile() {
  isSaving.value = true
  saveMessage.value = ''
  saveError.value = ''
  const result = await staffStore.updateProfile({ ...editForm.value })
  isSaving.value = false
  if (result.success) {
    saveMessage.value = 'Profile saved successfully!'
    isEditing.value = false
    setTimeout(() => saveMessage.value = '', 3000)
  } else {
    saveError.value = result.message
  }
}

const profile = computed(() => staffStore.profile)
const username = computed(() => authStore.user?.username || profile.value?.username || 'Unknown')
const role = computed(() => authStore.user?.role || 'Trek Staff')
const firstLetter = computed(() => (profile.value?.full_name || username.value).charAt(0).toUpperCase())
const displayName = computed(() => profile.value?.full_name || username.value)

const statusColor = computed(() => {
  const s = profile.value?.status
  if (s === 'Approved') return { bg: 'rgba(21,128,61,0.1)', color: '#15803d' }
  if (s === 'Pending') return { bg: 'rgba(180,83,9,0.1)', color: '#b45309' }
  return { bg: 'rgba(185,28,28,0.1)', color: '#b91c1c' }
})
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="staff-profile">
    <div class="page-header">
      <h2><i class="bi bi-person-badge me-2 text-primary"></i>My Profile</h2>
      <p>Your staff account information and assignment overview</p>
    </div>

    <!-- Alerts -->
    <transition name="fade">
      <div v-if="saveMessage" class="alert mb-4 py-2 px-3 d-flex align-items-center gap-2"
        style="background:#f0fdf4;color:#166534;border:1px solid #bbf7d0;border-radius:8px;font-size:0.87rem;">
        <i class="bi bi-check-circle-fill"></i>{{ saveMessage }}
      </div>
    </transition>
    <transition name="fade">
      <div v-if="saveError" class="alert mb-4 py-2 px-3 d-flex align-items-center gap-2"
        style="background:#fef2f2;color:#991b1b;border:1px solid #fecaca;border-radius:8px;font-size:0.87rem;">
        <i class="bi bi-exclamation-circle-fill"></i>{{ saveError }}
      </div>
    </transition>

    <div class="row g-4">
      <!-- Avatar Card -->
      <div class="col-md-4 col-lg-3">
        <div class="tma-card overflow-hidden">
          <div style="height:100px;background:linear-gradient(135deg,#1e3a5f,#3b82f6);"></div>
          <div class="card-body text-center px-4 pb-4" style="margin-top:-50px;">
            <div class="d-inline-flex align-items-center justify-content-center rounded-circle text-white fw-bold shadow"
              style="width:96px;height:96px;font-size:2.5rem;border:4px solid white;background:linear-gradient(135deg,#1e3a5f,#3b82f6);">
              {{ firstLetter }}
            </div>
            <h3 class="mt-3 mb-1 fw-bold">{{ displayName }}</h3>
            <p class="text-muted small mb-2">@{{ username }}</p>
            <span class="badge rounded-pill px-3 py-2 mb-2"
              :style="`background:${statusColor.bg};color:${statusColor.color};font-size:0.8rem;`">
              <i class="bi bi-circle-fill me-1" style="font-size:0.5rem;"></i>{{ profile?.status || 'Pending' }}
            </span>
            <div v-if="profile?.member_since" class="mt-2 small text-muted">
              <i class="bi bi-calendar3 me-1"></i>Since {{ profile.member_since }}
            </div>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="tma-card mt-3">
          <div class="card-body p-3">
            <h6 class="fw-semibold mb-3 text-muted text-uppercase" style="font-size:0.75rem;letter-spacing:0.5px;">Assignment Stats</h6>
            <div class="d-flex align-items-center justify-content-between py-2 border-bottom">
              <span class="small"><i class="bi bi-compass text-primary me-2"></i>Assigned Treks</span>
              <span class="fw-bold">{{ staffStore.summary?.total_treks || 0 }}</span>
            </div>
            <div class="d-flex align-items-center justify-content-between py-2">
              <span class="small"><i class="bi bi-journal-check text-primary me-2"></i>Total Bookings</span>
              <span class="fw-bold">{{ staffStore.summary?.total_bookings || 0 }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Details / Edit Panel -->
      <div class="col-md-8 col-lg-9">
        <div class="tma-card h-100">
          <div class="card-header-custom d-flex justify-content-between align-items-center">
            <h5 class="mb-0"><i class="bi bi-info-circle me-2"></i>{{ isEditing ? 'Edit Profile' : 'Profile Details' }}</h5>
            <div class="d-flex gap-2">
              <button v-if="!isEditing" class="btn btn-tma btn-sm" @click="startEdit">
                <i class="bi bi-pencil me-1"></i>Edit
              </button>
              <template v-else>
                <button class="btn btn-tma btn-sm" :disabled="isSaving" @click="saveProfile">
                  <span v-if="isSaving" class="spinner-border spinner-border-sm me-1"></span>
                  <i v-else class="bi bi-check-lg me-1"></i>{{ isSaving ? 'Saving…' : 'Save' }}
                </button>
                <button class="btn btn-tma-outline btn-sm" @click="cancelEdit">
                  <i class="bi bi-x-lg me-1"></i>Cancel
                </button>
              </template>
            </div>
          </div>

          <div class="card-body p-4">
            <!-- VIEW MODE -->
            <div v-if="!isEditing" class="row g-3">
              <div class="col-sm-6">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-person-badge me-1"></i>Full Name</div>
                  <div class="field-value">{{ profile?.full_name || '—' }}</div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-person me-1"></i>Username</div>
                  <div class="field-value">{{ username }}</div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-envelope me-1"></i>Email</div>
                  <div class="field-value">{{ profile?.email || '—' }}</div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-telephone me-1"></i>Phone</div>
                  <div class="field-value">{{ profile?.phone || '—' }}</div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-card-list me-1"></i>Contact Details</div>
                  <div class="field-value">{{ profile?.contact_details || '—' }}</div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-award me-1"></i>Experience (years)</div>
                  <div class="field-value">{{ profile?.experience_years != null ? profile.experience_years + ' yr' + (profile.experience_years !== 1 ? 's' : '') : '—' }}</div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-lightning me-1"></i>Specialization</div>
                  <div class="field-value">{{ profile?.specialization || '—' }}</div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-shield-check me-1"></i>Account Status</div>
                  <div class="field-value">
                    <span v-if="profile?.blacklisted" class="badge bg-danger">Blacklisted</span>
                    <span v-else class="fw-semibold" :style="`color:${statusColor.color};`">{{ profile?.status || 'Pending' }}</span>
                  </div>
                </div>
              </div>
              <div class="col-12">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-chat-square-text me-1"></i>Bio</div>
                  <div class="field-value">{{ profile?.bio || 'No bio added yet.' }}</div>
                </div>
              </div>
            </div>

            <!-- EDIT MODE -->
            <form v-else class="row g-3" @submit.prevent="saveProfile">
              <div class="col-sm-6">
                <label class="form-label" for="staff-edit-fullname"><i class="bi bi-person-badge me-1"></i>Full Name</label>
                <input id="staff-edit-fullname" type="text" class="form-control" v-model="editForm.full_name" placeholder="Your full name">
              </div>
              <div class="col-sm-6">
                <label class="form-label" for="staff-edit-phone"><i class="bi bi-telephone me-1"></i>Phone</label>
                <input id="staff-edit-phone" type="tel" class="form-control" v-model="editForm.phone" placeholder="e.g. +91 98765 43210">
              </div>
              <div class="col-sm-6">
                <label class="form-label" for="staff-edit-contact"><i class="bi bi-card-list me-1"></i>Contact Details</label>
                <input id="staff-edit-contact" type="text" class="form-control" v-model="editForm.contact_details" placeholder="Address, alternate contact…">
              </div>
              <div class="col-sm-6">
                <label class="form-label" for="staff-edit-exp"><i class="bi bi-award me-1"></i>Experience (years)</label>
                <input id="staff-edit-exp" type="number" min="0" max="60" class="form-control" v-model="editForm.experience_years" placeholder="Years of trekking experience">
              </div>
              <div class="col-sm-12">
                <label class="form-label" for="staff-edit-spec"><i class="bi bi-lightning me-1"></i>Specialization</label>
                <input id="staff-edit-spec" type="text" class="form-control" v-model="editForm.specialization" placeholder="e.g. High Altitude, Rock Climbing, First Aid…">
              </div>
              <div class="col-12">
                <label class="form-label" for="staff-edit-bio"><i class="bi bi-chat-square-text me-1"></i>Bio</label>
                <textarea id="staff-edit-bio" class="form-control" rows="3" v-model="editForm.bio" placeholder="Tell us about your experience and passion for trekking…"></textarea>
              </div>
            </form>

            <hr class="my-4">
            <div class="d-flex gap-3 flex-wrap">
              <router-link to="/staff" class="btn btn-tma">
                <i class="bi bi-speedometer2 me-2"></i>Go to Dashboard
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-field {
  background: #f8faf9;
  border-radius: 10px;
  padding: 12px 14px;
}
.field-label {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #888;
  margin-bottom: 4px;
}
.field-value {
  font-weight: 600;
  color: #1e3a2f;
  font-size: 0.95rem;
}
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
