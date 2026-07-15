<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTrekkerStore } from '@/stores/trekker'

const authStore = useAuthStore()
const trekkerStore = useTrekkerStore()

const isEditing = ref(false)
const isSaving = ref(false)
const saveMessage = ref('')
const saveError = ref('')

const editForm = ref({
  full_name: '',
  age: '',
  phone: '',
  bio: '',
  emergency_contact: ''
})

onMounted(async () => {
  await Promise.all([trekkerStore.fetchProfile(), trekkerStore.fetchSummary()])
  if (trekkerStore.profile) {
    populateForm()
  }
})

function populateForm() {
  const p = trekkerStore.profile
  editForm.value = {
    full_name: p.full_name || '',
    age: p.age ?? '',
    phone: p.phone || '',
    bio: p.bio || '',
    emergency_contact: p.emergency_contact || ''
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
  const result = await trekkerStore.updateProfile({ ...editForm.value })
  isSaving.value = false
  if (result.success) {
    saveMessage.value = 'Profile saved successfully!'
    isEditing.value = false
    setTimeout(() => saveMessage.value = '', 3000)
  } else {
    saveError.value = result.message
  }
}

const profile = computed(() => trekkerStore.profile)
const username = computed(() => authStore.user?.username || profile.value?.username || 'Unknown')
const role = computed(() => authStore.user?.role || 'Trekker')
const firstLetter = computed(() => (profile.value?.full_name || username.value).charAt(0).toUpperCase())
const displayName = computed(() => profile.value?.full_name || username.value)
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="trekker-profile">
    <div class="page-header">
      <h2><i class="bi bi-person-circle me-2 text-primary"></i>My Profile</h2>
      <p>Your account information and activity overview</p>
    </div>

    <!-- Save success/error alerts -->
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
      <!-- Profile Card (Avatar) -->
      <div class="col-md-4 col-lg-3">
        <div class="tma-card overflow-hidden">
          <div style="height:100px;background:linear-gradient(135deg,var(--primary-dark),var(--primary-light));"></div>
          <div class="card-body text-center px-4 pb-4" style="margin-top:-50px;">
            <div class="d-inline-flex align-items-center justify-content-center rounded-circle text-white fw-bold shadow"
              style="width:96px;height:96px;font-size:2.5rem;border:4px solid white;background:linear-gradient(135deg,var(--primary),var(--primary-light));">
              {{ firstLetter }}
            </div>
            <h3 class="mt-3 mb-1 fw-bold">{{ displayName }}</h3>
            <p class="text-muted small mb-2">@{{ username }}</p>
            <span class="badge rounded-pill px-3 py-2"
              style="background:rgba(45,106,79,0.1);color:var(--primary);font-size:0.8rem;">
              <i class="bi bi-shield-check me-1"></i>{{ role }}
            </span>
            <div v-if="profile?.member_since" class="mt-3 small text-muted">
              <i class="bi bi-calendar3 me-1"></i>Member since {{ profile.member_since }}
            </div>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="tma-card mt-3">
          <div class="card-body p-3">
            <h6 class="fw-semibold mb-3 text-muted text-uppercase" style="font-size:0.75rem;letter-spacing:0.5px;">Activity</h6>
            <div class="d-flex align-items-center justify-content-between py-2 border-bottom">
              <span class="small"><i class="bi bi-journal-check text-primary me-2"></i>Total Bookings</span>
              <span class="fw-bold">{{ trekkerStore.summary?.total_bookings || 0 }}</span>
            </div>
            <div class="d-flex align-items-center justify-content-between py-2">
              <span class="small"><i class="bi bi-map text-primary me-2"></i>Available Treks</span>
              <span class="fw-bold">{{ trekkerStore.summary?.total_treks || 0 }}</span>
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
                  <div class="field-label"><i class="bi bi-calendar2-heart me-1"></i>Age</div>
                  <div class="field-value">{{ profile?.age || '—' }}</div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-heart-pulse me-1"></i>Emergency Contact</div>
                  <div class="field-value">{{ profile?.emergency_contact || '—' }}</div>
                </div>
              </div>
              <div class="col-12">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-chat-square-text me-1"></i>Bio</div>
                  <div class="field-value">{{ profile?.bio || 'No bio added yet.' }}</div>
                </div>
              </div>
              <div class="col-sm-6">
                <div class="profile-field">
                  <div class="field-label"><i class="bi bi-shield-check me-1"></i>Account Status</div>
                  <div class="field-value">
                    <span v-if="profile?.blacklisted" class="badge bg-danger">Blacklisted</span>
                    <span v-else class="text-success fw-semibold"><i class="bi bi-check-circle-fill me-1"></i>Active Member</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- EDIT MODE -->
            <form v-else class="row g-3" @submit.prevent="saveProfile">
              <div class="col-sm-6">
                <label class="form-label" for="edit-fullname"><i class="bi bi-person-badge me-1"></i>Full Name</label>
                <input id="edit-fullname" type="text" class="form-control" v-model="editForm.full_name" placeholder="Your full name">
              </div>
              <div class="col-sm-6">
                <label class="form-label" for="edit-phone"><i class="bi bi-telephone me-1"></i>Phone</label>
                <input id="edit-phone" type="tel" class="form-control" v-model="editForm.phone" placeholder="e.g. +91 98765 43210">
              </div>
              <div class="col-sm-6">
                <label class="form-label" for="edit-age"><i class="bi bi-calendar2-heart me-1"></i>Age</label>
                <input id="edit-age" type="number" min="1" max="120" class="form-control" v-model="editForm.age" placeholder="Your age">
              </div>
              <div class="col-sm-6">
                <label class="form-label" for="edit-emergency"><i class="bi bi-heart-pulse me-1"></i>Emergency Contact</label>
                <input id="edit-emergency" type="text" class="form-control" v-model="editForm.emergency_contact" placeholder="Name & number">
              </div>
              <div class="col-12">
                <label class="form-label" for="edit-bio"><i class="bi bi-chat-square-text me-1"></i>Bio</label>
                <textarea id="edit-bio" class="form-control" rows="3" v-model="editForm.bio" placeholder="Tell us about yourself and your trekking passion…"></textarea>
              </div>
            </form>

            <hr class="my-4">
            <div class="d-flex gap-3 flex-wrap">
              <router-link to="/trekker/explore" class="btn btn-tma">
                <i class="bi bi-binoculars me-2"></i>Explore Treks
              </router-link>
              <router-link to="/trekker/bookings" class="btn btn-tma-outline">
                <i class="bi bi-journal-check me-2"></i>View Bookings
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
