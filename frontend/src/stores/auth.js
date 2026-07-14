import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'
import apiClient from '@/axiosApi.js'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    user: localStorage.getItem('accessToken') ? jwtDecode(localStorage.getItem('accessToken')) : null
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isAdmin: (state) => state.user?.role === 'Admin' || state.user?.role === 'ADMIN',
    isTrekker: (state) => state.user?.role === 'Trekker' || state.user?.role === 'TREKKER',
    isTrekStaff: (state) => state.user?.role === 'Trek Staff' || state.user?.role === 'TREK_STAFF',
    currentUser: (state) => state.user?.username || '',
    userRole: (state) => state.user?.role || ''
  },

  actions: {
    setAuthTokens(access, refresh) {
      this.accessToken = access
      this.refreshToken = refresh
      this.user = jwtDecode(access)
      
      localStorage.setItem('accessToken', access)
      localStorage.setItem('refreshToken', refresh)
    },
    
    clearAuth() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    },

    async login(credentials) {
      try {
        const response = await apiClient.post('/auth/login', credentials)
        this.setAuthTokens(response.data.access_token, response.data.refresh_token)
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          message: error.response?.data?.error || 'Login failed' 
        }
      }
    },

    logout() {
      this.clearAuth()
    }
  }
})
