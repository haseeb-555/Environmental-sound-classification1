import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';

const routes = [
  { path: '/', component: Login },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Protect routes
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem("token");
  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/");
  } else {
    next();
  }
});

export default router;
