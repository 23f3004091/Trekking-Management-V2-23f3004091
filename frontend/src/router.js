import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy-loaded views
const LandingPage    = () => import('@/views/LandingPage.vue')
const LoginPage      = () => import('@/views/LoginPage.vue')
const RegisterPage      = () => import('@/views/RegisterPage.vue')
const RegisterStaffPage = () => import('@/views/RegisterStaffPage.vue')

const AdminDashboard = () => import('@/views/AdminDashboard.vue')
const AdminTreks     = () => import('@/views/AdminTreks.vue')
const AdminStaff     = () => import('@/views/AdminStaff.vue')
const AdminUsers     = () => import('@/views/AdminUsers.vue')
const AdminBookings  = () => import('@/views/AdminBookings.vue')

const StaffDashboard   = () => import('@/views/StaffDashboard.vue')
const StaffTrekDetail  = () => import('@/views/StaffTrekDetail.vue')
const StaffProfileView = () => import('@/views/StaffProfile.vue')

const TrekkerDashboard = () => import('@/views/TrekkerDashboard.vue')
const TrekkerExplore   = () => import('@/views/TrekkerExplore.vue')
const TrekkerBookings  = () => import('@/views/TrekkerBookings.vue')
const TrekkerProfile   = () => import('@/views/TrekkerProfile.vue')

const routes = [
  // ── Public / Guest ────────────────────────────────────────────
  {
    path: '/',
    name: 'Landing',
    component: LandingPage,
    meta: { guest: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { guest: true }
  },
  {
    path: '/register-trekker',
    name: 'Register',
    component: RegisterPage,
    meta: { guest: true }
  },
  {
    path: '/register-staff',
    name: 'RegisterStaff',
    component: RegisterStaffPage,
    meta: { guest: true }
  },

  // ── Admin ──────────────────────────────────────────────────────
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'Admin' }
  },
  {
    path: '/admin/treks',
    name: 'AdminTreks',
    component: AdminTreks,
    meta: { requiresAuth: true, role: 'Admin' }
  },
  {
    path: '/admin/staff',
    name: 'AdminStaff',
    component: AdminStaff,
    meta: { requiresAuth: true, role: 'Admin' }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: AdminUsers,
    meta: { requiresAuth: true, role: 'Admin' }
  },
  {
    path: '/admin/bookings',
    name: 'AdminBookings',
    component: AdminBookings,
    meta: { requiresAuth: true, role: 'Admin' }
  },

  // ── Staff ──────────────────────────────────────────────────────
  {
    path: '/staff',
    name: 'StaffDashboard',
    component: StaffDashboard,
    meta: { requiresAuth: true, role: 'Trek Staff' }
  },
  {
    path: '/staff/trek/:id',
    name: 'StaffTrekDetail',
    component: StaffTrekDetail,
    meta: { requiresAuth: true, role: 'Trek Staff' }
  },
  {
    path: '/staff/profile',
    name: 'StaffProfile',
    component: StaffProfileView,
    meta: { requiresAuth: true, role: 'Trek Staff' }
  },

  // ── Trekker ────────────────────────────────────────────────────
  {
    path: '/trekker',
    name: 'TrekkerDashboard',
    component: TrekkerDashboard,
    meta: { requiresAuth: true, role: 'Trekker' }
  },
  {
    path: '/trekker/explore',
    name: 'TrekkerExplore',
    component: TrekkerExplore,
    meta: { requiresAuth: true, role: 'Trekker' }
  },
  {
    path: '/trekker/bookings',
    name: 'TrekkerBookings',
    component: TrekkerBookings,
    meta: { requiresAuth: true, role: 'Trekker' }
  },
  {
    path: '/trekker/profile',
    name: 'TrekkerProfile',
    component: TrekkerProfile,
    meta: { requiresAuth: true, role: 'Trekker' }
  },

  // ── Catch-all ──────────────────────────────────────────────────
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

// Role → default dashboard path map
const roleDashboardMap = {
  'Admin':      '/admin',
  'Trek Staff': '/staff',
  'Trekker':    '/trekker'
}

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// ── Navigation Guards ──────────────────────────────────────────
router.beforeEach((to, from, next) => {
  const authStore   = useAuthStore()
  const isAuth      = authStore.isAuthenticated
  const userRole    = authStore.user?.role || null   // e.g. 'Admin' | 'Trek Staff' | 'Trekker'

  // 1. Guest-only routes: redirect logged-in users to their dashboard
  if (to.meta.guest && isAuth) {
    return next(roleDashboardMap[userRole] || '/')
  }

  // 2. Protected routes: redirect unauthenticated users to login
  if (to.meta.requiresAuth && !isAuth) {
    return next({ name: 'Login' })
  }

  // 3. Role mismatch: redirect to the user's own dashboard
  if (to.meta.role && userRole !== to.meta.role) {
    return next(roleDashboardMap[userRole] || '/')
  }

  next()
})

export default router
