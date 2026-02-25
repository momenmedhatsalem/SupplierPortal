<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar (desktop) -->
    <Sidebar class="hidden lg:flex" />

    <!-- Mobile overlay -->
    <div v-if="mobileMenuOpen" class="fixed inset-0 bg-black/50 z-40 lg:hidden" @click="mobileMenuOpen = false" />

    <!-- Mobile sidebar -->
    <transition name="slide">
      <Sidebar v-if="mobileMenuOpen" class="fixed inset-y-0 left-0 z-50 lg:hidden" @close="mobileMenuOpen = false" />
    </transition>

    <!-- Main content -->
    <div class="flex-1 flex flex-col min-w-0">
      <Header @toggle-menu="mobileMenuOpen = !mobileMenuOpen" />
      <main class="flex-1 p-4 sm:p-6 lg:p-8 overflow-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Sidebar from "./Sidebar.vue";
import Header from "./Header.vue";

const mobileMenuOpen = ref(false);
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.2s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
