<template>
  <header class="h-16 bg-white border-b border-gray-200 flex items-center px-4 sm:px-6 lg:px-8 gap-4">
    <!-- Mobile menu button -->
    <button @click="$emit('toggleMenu')" class="lg:hidden p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors -ml-2">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>

    <!-- Page title -->
    <h1 class="text-lg font-semibold text-gray-900">
      {{ pageTitle }}
    </h1>

    <div class="flex-1" />

    <!-- Notifications -->
    <router-link
      to="/suppliers/notifications"
      class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors relative"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
    </router-link>

    <!-- User menu -->
    <div class="relative" ref="menuRef">
      <button
        @click="showUserMenu = !showUserMenu"
        class="flex items-center gap-2 p-1.5 rounded-xl hover:bg-gray-100 transition-colors"
      >
        <div class="w-8 h-8 bg-brand-100 text-brand-700 rounded-lg flex items-center justify-center text-sm font-bold">
          {{ userInitial }}
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400 hidden sm:block"><polyline points="6 9 12 15 18 9"/></svg>
      </button>

      <!-- Dropdown -->
      <transition name="dropdown">
        <div v-if="showUserMenu" class="absolute right-0 top-12 w-56 bg-white rounded-xl border border-gray-200 shadow-xl py-1 z-50">
          <div class="px-4 py-3 border-b border-gray-100">
            <div class="text-sm font-medium text-gray-900 truncate">
              {{ supplier?.supplier_name || 'Supplier' }}
            </div>
            <div class="text-xs text-gray-500 truncate">{{ user }}</div>
          </div>
          <div class="py-1">
            <router-link
              to="/suppliers/settings"
              class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
              @click="showUserMenu = false"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-gray-400"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09"/></svg>
              Account Settings
            </router-link>
          </div>
          <div class="border-t border-gray-100 pt-1">
            <button
              @click="handleLogout"
              class="flex items-center gap-2 w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-red-400"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
              Sign Out
            </button>
          </div>
        </div>
      </transition>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuth } from "@/composables/useAuth";

defineEmits(["toggleMenu"]);

const route = useRoute();
const router = useRouter();
const { user, supplier, logout } = useAuth();

const showUserMenu = ref(false);
const menuRef = ref(null);

const pageTitle = computed(() => {
  const titles = {
    Dashboard: "Dashboard",
    Performance: "Performance",
    Orders: "Orders",
    OrderDetail: "Order Detail",
    Products: "Products",
    ProductDetail: "Product Detail",
    Inventory: "Inventory",
    Settings: "Settings",
    Notifications: "Notifications",
  };
  return titles[route.name] || "Portal";
});

const userInitial = computed(() => {
  if (supplier.value?.supplier_name) {
    return supplier.value.supplier_name.charAt(0).toUpperCase();
  }
  return "S";
});

async function handleLogout() {
  await logout();
  router.push("/suppliers/login");
}

// Close menu on outside click
function handleClickOutside(event) {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    showUserMenu.value = false;
  }
}

onMounted(() => document.addEventListener("click", handleClickOutside));
onUnmounted(() => document.removeEventListener("click", handleClickOutside));
</script>

<style scoped>
.dropdown-enter-active {
  transition: all 0.15s ease-out;
}
.dropdown-leave-active {
  transition: all 0.1s ease-in;
}
.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-4px) scale(0.97);
}
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-2px) scale(0.98);
}
</style>
