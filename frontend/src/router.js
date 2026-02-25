import { createRouter, createWebHistory } from "vue-router";
import { useAuth } from "@/composables/useAuth";

// Auth pages
import Login from "@/pages/auth/Login.vue";
import Register from "@/pages/auth/Register.vue";
import ForgotPassword from "@/pages/auth/ForgotPassword.vue";

// Portal pages
import Dashboard from "@/pages/Dashboard.vue";
import Performance from "@/pages/Performance.vue";
import Orders from "@/pages/Orders.vue";
import OrderDetail from "@/pages/OrderDetail.vue";
import Products from "@/pages/Products.vue";
import ProductDetail from "@/pages/ProductDetail.vue";
import Inventory from "@/pages/Inventory.vue";
import Settings from "@/pages/Settings.vue";
import Notifications from "@/pages/Notifications.vue";
import Landing from "@/pages/Landing.vue";

// Layout
import AppLayout from "@/components/layout/AppLayout.vue";

const routes = [
  // Public pages
  {
    path: "/suppliers",
    name: "Landing",
    component: Landing,
    meta: { guest: true },
  },
  {
    path: "/suppliers/login",
    name: "Login",
    component: Login,
    meta: { guest: true },
  },
  {
    path: "/suppliers/register",
    name: "Register",
    component: Register,
    meta: { guest: true },
  },
  {
    path: "/suppliers/forgot-password",
    name: "ForgotPassword",
    component: ForgotPassword,
    meta: { guest: true },
  },

  // Protected portal pages (wrapped in AppLayout)
  {
    path: "/suppliers",
    component: AppLayout,
    meta: { requiresAuth: true },
    children: [
      { path: "dashboard", name: "Dashboard", component: Dashboard },
      { path: "performance", name: "Performance", component: Performance },
      { path: "orders", name: "Orders", component: Orders },
      { path: "orders/:id", name: "OrderDetail", component: OrderDetail, props: true },
      { path: "products", name: "Products", component: Products },
      { path: "products/:code", name: "ProductDetail", component: ProductDetail, props: true },
      { path: "inventory", name: "Inventory", component: Inventory },
      { path: "settings", name: "Settings", component: Settings },
      { path: "notifications", name: "Notifications", component: Notifications },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Auth guard
router.beforeEach(async (to, from, next) => {
  const { init, isLoggedIn, isLoading } = useAuth();

  // Initialize auth state
  await init();

  if (to.meta.requiresAuth && !isLoggedIn.value) {
    // Redirect to login with return URL
    next({ name: "Login", query: { redirect: to.fullPath } });
  } else if (to.meta.guest && isLoggedIn.value && to.name !== "Landing") {
    // Logged-in user trying to access login/register — send to dashboard
    next({ name: "Dashboard" });
  } else {
    next();
  }
});

export default router;
