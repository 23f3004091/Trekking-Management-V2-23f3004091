import { defineStore } from 'pinia'
import apiClient from '@/axiosApi.js'

export const useTrekkerStore = defineStore('trekker', {
  state: () => ({
    summary: { total_treks: 0, total_bookings: 0 },
    treks: [],
    history: [],
    profile: null,
    isLoading: false,
    error: null,
  }),

  getters: {
    getTrekById: (state) => (id) => {
      return state.treks.find(trek => trek.id === id)
    },
    openTreks: (state) => {
      return state.treks.filter(trek => trek.status === 'OPEN')
    }
  },

  actions: {
    async fetchSummary() {
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.get('/trekker/summary')
        this.summary = {
          total_treks: response.data.total_treks,
          total_bookings: response.data.total_bookings
        }
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch summary'
      } finally {
        this.isLoading = false
      }
    },

    async fetchTreks() {
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.get('/trekker/treks')
        this.treks = response.data.treks
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch treks'
      } finally {
        this.isLoading = false
      }
    },

    async fetchHistory() {
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.get('/trekker/history')
        this.history = response.data.history
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch booking history'
      } finally {
        this.isLoading = false
      }
    },

    async fetchProfile() {
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.get('/trekker/profile')
        this.profile = response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch profile'
      } finally {
        this.isLoading = false
      }
    },

    async updateProfile(data) {
      this.isLoading = true
      this.error = null
      try {
        await apiClient.patch('/trekker/profile', data)
        // Merge updates into local state
        this.profile = { ...this.profile, ...data }
        return { success: true, message: 'Profile updated successfully' }
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update profile'
        return { success: false, message: this.error }
      } finally {
        this.isLoading = false
      }
    },

    async bookTrek(trekId) {
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.post(`/trekker/book-trek/${trekId}`)
        this.history.push(response.data.booking)
        this.summary.total_bookings += 1
        return { success: true, message: response.data.message }
      } catch (error) {
        this.error = error.response?.data?.error || 'Booking failed'
        return { success: false, message: this.error }
      } finally {
        this.isLoading = false
      }
    },

    async updateBookingStatus(bookingId, newStatus) {
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.patch(`/trekker/update-booking-status/${bookingId}`, {
          status: newStatus
        })
        const index = this.history.findIndex(b => b.id === bookingId)
        if (index !== -1) {
          this.history[index].status = response.data.booking.status
        }
        return { success: true, message: response.data.message }
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update status'
        return { success: false, message: this.error }
      } finally {
        this.isLoading = false
      }
    }
  }
})