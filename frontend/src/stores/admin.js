import { defineStore } from 'pinia'
import apiClient from '@/axiosApi.js'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    summary: {
      total_trekkers: 0,
      total_staff: 0,
      total_treks: 0,
      total_bookings: 0
    },
    staffList: [],
    trekkerList: [],
    trekList: [],
    bookingList: [],
    isLoading: false,
    error: null
  }),

  actions: {
    // ==========================================
    // FETCH ACTIONS (READ)
    // ==========================================
    async fetchSummary() {
      try {
        const response = await apiClient.get('/admin/summary')
        this.summary = response.data
      } catch (error) {
        this.error = 'Failed to fetch summary'
      }
    },

    async fetchStaff() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/admin/staff')
        this.staffList = response.data.users
      } catch (error) {
        this.error = 'Failed to fetch staff'
      } finally {
        this.isLoading = false
      }
    },

    async fetchTreks() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/admin/treks')
        this.trekList = response.data.treks
      } catch (error) {
        this.error = 'Failed to fetch treks'
      } finally {
        this.isLoading = false
      }
    },

    async fetchBookings() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/admin/bookings')
        this.bookingList = response.data.bookings
      } catch (error) {
        this.error = 'Failed to fetch bookings'
      } finally {
        this.isLoading = false
      }
    },

    async fetchTrekkers() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/admin/trekkers')
        this.trekkerList = response.data.trekkers
      } catch (error) {
        this.error = 'Failed to fetch trekkers'
      } finally {
        this.isLoading = false
      }
    },
    
    // Treks
    async createTrek(trekData) {
      const response = await apiClient.post('/admin/create-trek', trekData)
      // Optimistically add the new trek to the list so we don't have to refetch
      this.trekList.push(response.data.trek) 
      return response
    },

    async updateTrek(trekId, trekData) {
      const response = await apiClient.put(`/admin/update-trek/${trekId}`, trekData)
      // Update the specific item in the state
      const index = this.trekList.findIndex(t => t.id === trekId)
      if (index !== -1) {
        this.trekList[index] = { ...this.trekList[index], ...trekData }
      }
      return response
    },

    async deleteTrek(trekId) {
      await apiClient.delete(`/admin/delete-trek/${trekId}`)
      // Remove it from the local list
      this.trekList = this.trekList.filter(t => t.id !== trekId)
    },

    async manageTrekStatus(trekId, action) {
      const response = await apiClient.patch(`/admin/manage-trek/${trekId}`, { action })
      const index = this.trekList.findIndex(t => t.id === trekId)
      if (index !== -1) {
        this.trekList[index].status = response.data.trek.status
      }
    },

    // Bookings
    async manageBooking(bookingId, action) {
      const response = await apiClient.patch(`/admin/manage-booking/${bookingId}`, { action })
      const index = this.bookingList.findIndex(b => b.id === bookingId)
      if (index !== -1) {
        this.bookingList[index].status = response.data.booking.status
      }
    },

    // Users (Staff & Trekkers)
    async approveStaff(staffId) {
      const response = await apiClient.patch('/admin/approve-staff', { staff_id: staffId })
      console.log(response)
      const index = this.staffList.findIndex(s => s.id === staffId)
      if (index !== -1) {
        this.staffList[index].status = response.data.staff_profile.status
      }
    },

    async blacklistStaff(staffId) {
      const response = await apiClient.patch('/admin/blacklist-staff', { staff_id: staffId })
      const index = this.staffList.findIndex(s => s.id === staffId)
      if (index !== -1) {
        this.staffList[index].blacklisted = response.data.staff_profile.blacklisted
      }
    },

    async blacklistTrekker(trekkerId) {
      const response = await apiClient.patch('/admin/blacklist-trekker', { trekker_id: trekkerId })
      const index = this.trekkerList.findIndex(t => t.id === trekkerId)
      if (index !== -1) {
        this.trekkerList[index].blacklisted = response.data.trekker.blacklisted
      }
    }
  }
})