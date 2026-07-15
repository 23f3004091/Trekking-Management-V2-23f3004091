<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useTrekkerStore } from '@/stores/trekker'
import SearchBar from '@/components/SearchBar.vue'
import TrekCard from '@/components/TrekCard.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const showBookingModal = ref(false)

const trekkerStore = useTrekkerStore()
const showToast = inject('showToast')

const searchQuery = ref('')
const activeFilters = ref({ difficulty: 'All' })
const trekToBook = ref(null)

onMounted(() => {
  trekkerStore.fetchTreks()
})

const filteredTreks = computed(() => {
  return (trekkerStore.treks || []).filter(trek => {
    const q = searchQuery.value.toLowerCase()
    const matchQuery = (trek.trek_name?.toLowerCase().includes(q)) ||
                       (trek.location?.toLowerCase().includes(q))
    const matchDifficulty = activeFilters.value.difficulty === 'All' || trek.difficulty === activeFilters.value.difficulty
    return matchQuery && matchDifficulty
  })
})

const handleSearch = (q) => { searchQuery.value = q }
const handleFilter = (f) => { activeFilters.value = { ...activeFilters.value, ...f } }

const confirmBooking = (trek) => {
  trekToBook.value = trek
  showBookingModal.value = true
}

const executeBooking = async () => {
  if (!trekToBook.value) return
  try {
    const result = await trekkerStore.bookTrek(trekToBook.value.id)
    if (result.success) {
      showToast('Trek booked successfully! 🎉', 'success')
      await trekkerStore.fetchTreks()
    } else {
      showToast(result.message || 'Booking failed', 'error')
    }
  } catch (err) {
    showToast(err.response?.data?.error || 'Failed to book trek', 'error')
  }
}

const formatDT = (d) => {
  if (!d) return 'N/A'
  return new Date(d).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}
</script>

<template>
  <div class="dashboard-page animate-fade-in-up" id="trekker-explore">
    <div class="page-header">
      <h2><i class="bi bi-binoculars me-2 text-primary"></i>Explore Treks</h2>
      <p>Discover and book your next trekking adventure</p>
    </div>

    <SearchBar
      placeholder="Search treks by name or location..."
      :filters="[
        { key: 'difficulty', label: 'Difficulty', options: ['All', 'Easy', 'Moderate', 'Hard'] }
      ]"
      @search="handleSearch"
      @filter="handleFilter"
    />

    <div v-if="trekkerStore.isLoading" class="py-5">
      <LoadingSpinner message="Loading available treks..." />
    </div>

    <div v-else-if="filteredTreks.length === 0" class="empty-state">
      <i class="bi bi-search"></i>
      <h5>No treks found</h5>
      <p>Try adjusting your search, or check back later for new treks.</p>
    </div>

    <div v-else>
      <!-- Result count -->
      <p class="text-muted small mb-3">
        <i class="bi bi-funnel me-1"></i>
        Showing {{ filteredTreks.length }} trek{{ filteredTreks.length !== 1 ? 's' : '' }}
      </p>

      <div class="row g-4 stagger-children">
        <div class="col-md-6 col-xl-4" v-for="trek in filteredTreks" :key="trek.id">
          <TrekCard :trek="trek">
            <template #actions>
              <button
                v-if="trek.status === 'Open' && trek.available_slots > 0"
                class="btn btn-tma btn-sm w-100 mt-3"
                @click="confirmBooking(trek)"
                :id="`book-trek-${trek.id}`"
                :disabled="filteredTreks.already_booked == true"
              >
                <i class="bi bi-lightning-charge-fill me-2"></i>Book Now
                <span class="ms-1 opacity-75">({{ trek.available_slots }} left)</span>
              </button>
              <button
                v-else-if="trek.status === 'Open' && trek.available_slots <= 0"
                class="btn btn-secondary btn-sm w-100 mt-3" disabled
              >
                <i class="bi bi-x-circle me-2"></i>Sold Out
              </button>
              <button
                v-else
                class="btn btn-outline-secondary btn-sm w-100 mt-3" disabled
              >
                <i class="bi bi-clock-history me-2"></i>{{ trek.status }} — Not Bookable
              </button>
            </template>
          </TrekCard>
        </div>
      </div>
    </div>

    <!-- Booking Confirmation Modal -->
    <ConfirmModal
      id="bookingConfirmModal"
      v-model="showBookingModal"
      :title="`Book: ${trekToBook?.trek_name}`"
      :message="`You're about to book '${trekToBook?.trek_name}' at ${trekToBook?.location}.\n\nStart: ${formatDT(trekToBook?.start_date)}  →  End: ${formatDT(trekToBook?.end_date)}\n\n${trekToBook?.available_slots} slot(s) available. Confirm your booking?`"
      confirmText="Confirm Booking"
      confirmClass="btn-tma"
      @confirm="executeBooking"
    />
  </div>
</template>
