import { defineStore } from 'pinia'
import apiClient from '@/axiosApi.js'

export const useStaffStore = defineStore('staff', {
  state: () => ({
    summary: { total_treks: 0, total_bookings: 0 },
    treks: [],
    bookingsByTrek: {}, // Cache: { trekId: [bookings...] }
    usersByTrek: {},    // Cache: { trekId: [users...] }
    profile: null,
    isLoading: false,
    error: null
  }),

  actions: {
    async fetchSummary() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/staff/summary');
        this.summary = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to load summary';
      } finally {
        this.isLoading = false;
      }
    },

    async fetchProfile() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/staff/profile');
        this.profile = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to load profile';
      } finally {
        this.isLoading = false;
      }
    },

    async updateProfile(data) {
      this.isLoading = true;
      this.error = null;
      try {
        await apiClient.patch('/staff/profile', data);
        this.profile = { ...this.profile, ...data };
        return { success: true, message: 'Profile updated successfully' };
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update profile';
        return { success: false, message: this.error };
      } finally {
        this.isLoading = false;
      }
    },

    async fetchTreks() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/staff/treks');
        this.treks = response.data.treks;
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to load treks';
      } finally {
        this.isLoading = false;
      }
    },

    async fetchBookingsForTrek(trekId) {
      // Optional: Prevent refetching if we already have the data
      // if (this.bookingsByTrek[trekId]) return; 

      this.isLoading = true;
      try {
        const response = await apiClient.get(`/staff/bookings/${trekId}`);
        // Store in dictionary keyed by trekId
        this.bookingsByTrek[trekId] = response.data.bookings;
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to load bookings';
      } finally {
        this.isLoading = false;
      }
    },

    async fetchUsersForTrek(trekId) {
      this.isLoading = true;
      try {
        const response = await apiClient.get(`/staff/user/${trekId}`);
        this.usersByTrek[trekId] = response.data.users;
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to load users';
      } finally {
        this.isLoading = false;
      }
    },

    async updateTrekStatus(trekId, payload) {
      try {
        const response = await apiClient.patch(`/staff/update-trek/${trekId}`, payload);
        
        // Optimistic UI update: Find the trek in state and update it directly
        // so you don't have to trigger a full refetch of all treks.
        const index = this.treks.findIndex(t => t.id === trekId);
        if (index !== -1) {
          this.treks[index].status = response.data.trek.status;
          if (payload.available_slots !== undefined) {
             // If your API returned available_slots, use that. Otherwise, use payload.
             this.treks[index].available_slots = payload.available_slots;
          }
        }
        return { success: true };
      } catch (error) {
        return { success: false, message: error.response?.data?.error || 'Update failed' };
      }
    },

    async updateBookingStatus(bookingId, trekId, newStatus) {
      try {
        const response = await apiClient.patch(`/staff/update-booking-status/${bookingId}`, {
          status: newStatus
        });
        
        // Optimistic UI update for the specific booking in the cache
        if (this.bookingsByTrek[trekId]) {
          const booking = this.bookingsByTrek[trekId].find(b => b.id === bookingId);
          if (booking) {
            booking.status = response.data.booking.status;
          }
        }
        return { success: true };
      } catch (error) {
        return { success: false, message: error.response?.data?.error || 'Update failed' };
      }
    }
  }
})