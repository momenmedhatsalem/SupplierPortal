<template>
  <header class="h-16 bg-white border-b border-gray-200 flex items-center px-4 sm:px-6 lg:px-8 gap-4">
    <!-- Mobile menu button -->
    <button @click="$emit('toggleMenu')" class="lg:hidden p-2 text-gray-500 hover:text-gray-700 -ml-2">
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
      class="p-2 text-gray-500 hover:text-gray-700 relative"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
    </router-link>

    <!-- User menu -->
    <div class="relative" ref="menuRef">
      <button
        @click="showUserMenu = !showUserMenu"
        class="flex items-center gap-2 p-1.5 rounded-lg hover:bg-gray-100 transition"
      >
        <div class="w-8 h-8 bg-brand-100 text-brand-700 rounded-full flex items-center justify-center text-sm font-semibold">
          {{ userInitial }}
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400"><polyline points="6 9 12 15 18 9"/></svg>
      </button>

      <!-- Dropdown -->
      <transition name="fade">
        <div v-if="showUserMenu" class="absolute right-0 top-12 w-56 bg-white rounded-xl border border-gray-200 shadow-lg py-1 z-50">
          <div class="px-4 py-3 border-b border-gray-100">
            <div class="text-sm font-medium text-gray-900 truncate">
              {{ supplier?.supplier_name || 'Supplier' }}
            </div>
            <div class="text-xs text-gray-500 truncate">{{ user }}</div>
          </div>
          <router-link
            to="/suppliers/settings"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
            @click="showUserMenu = false"
          >
            Account Settings
          </router-link>
          <button
            @click="handleLogout"
            class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
          >
            Sign Out
          </button>
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
.fade-enter-active, .fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
