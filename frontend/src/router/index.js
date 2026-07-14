// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth'

// import Landing from '@/views/Landing.vue'
// import Login from '@/views/Login.vue'
// import Register from '@/views/Register.vue'
// import AdminDashboard from '@/views/AdminDashboard.vue'
// import StaffDashboard from '@/views/StaffDashboard.vue'
// import TrekkerDashboard from '@/views/TrekkerDashboard.vue'

// const routes = [
//   {
//     path: '/',
//     name: 'Landing',
//     component: Landing
//   },
//   {
//     path: '/login',
//     name: 'Login',
//     component: Login,
//     meta: { guestOnly: true }
//   },
//   {
//     path: '/register',
//     name: 'Register',
//     component: Register,
//     meta: { guestOnly: true }
//   },
//   {
//     path: '/admin',
//     name: 'AdminDashboard',
//     component: AdminDashboard,
//     meta: { requiresAuth: true, role: 'Admin' }
//   },
//   {
//     path: '/staff',
//     name: 'StaffDashboard',
//     component: StaffDashboard,
//     meta: { requiresAuth: true, role: 'Trek Staff' }
//   },
//   {
//     path: '/trekker',
//     name: 'TrekkerDashboard',
//     component: TrekkerDashboard,
//     meta: { requiresAuth: true, role: 'Trekker' }
//   },
//   {
//     // Catch all unknown routes and send to Landing
//     path: '/:pathMatch(.*)*',
//     redirect: '/'
//   }
// ]

// const router = createRouter({
//   history: createWebHistory(),
//   routes,
//   scrollBehavior() {
//     return { top: 0 }
//   }
// })

// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()

//   // If visiting guest only routes (login/register) while authenticated, redirect to role dashboard
//   if (to.meta.guestOnly && authStore.isAuthenticated) {
//     if (authStore.isAdmin) return next('/admin')
//     if (authStore.isTrekStaff) return next('/staff')
//     if (authStore.isTrekker) return next('/trekker')
//     return next('/')
//   }

//   // If route requires authentication
//   if (to.meta.requiresAuth) {
//     if (!authStore.isAuthenticated) {
//       return next('/login')
//     }

//     // Role check if exact role is specified
//     if (to.meta.role === 'Admin' && !authStore.isAdmin) {
//       if (authStore.isTrekStaff) return next('/staff')
//       if (authStore.isTrekker) return next('/trekker')
//       return next('/')
//     }
//     if (to.meta.role === 'Trek Staff' && !authStore.isTrekStaff && !authStore.isAdmin) {
//       if (authStore.isTrekker) return next('/trekker')
//       return next('/')
//     }
//     if (to.meta.role === 'Trekker' && !authStore.isTrekker && !authStore.isAdmin) {
//       if (authStore.isTrekStaff) return next('/staff')
//       return next('/')
//     }
//   }

//   next()
// })

// export default router
