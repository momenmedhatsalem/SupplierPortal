<template>
  <div class="space-y-4 animate-fade-in">
    <div v-if="!notifications.length" class="card text-center py-16">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-gray-400"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
      </div>
      <p class="text-sm font-medium text-gray-900">No notifications yet</p>
      <p class="text-xs text-gray-500 mt-1 max-w-xs mx-auto">Alerts about orders, stock levels, and performance updates will appear here</p>
    </div>

    <div
      v-for="(notification, i) in notifications"
      :key="i"
      class="card flex items-start gap-3 animate-fade-in-up"
      :class="`stagger-${Math.min(i + 1, 6)}`"
    >
      <div
        class="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
        :class="{
          'bg-red-50 text-red-600': notification.type === 'urgent',
          'bg-yellow-50 text-yellow-600': notification.type === 'warning',
          'bg-blue-50 text-blue-600': notification.type === 'info',
          'bg-green-50 text-green-600': notification.type === 'success',
        }"
      >
        <svg v-if="notification.type === 'urgent'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <svg v-else-if="notification.type === 'warning'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        <svg v-else-if="notification.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4m0-4h.01"/></svg>
      </div>
      <div class="flex-1 min-w-0">
        <div class="text-sm font-medium text-gray-900">{{ notification.title }}</div>
        <div class="text-sm text-gray-500 mt-0.5">{{ notification.message }}</div>
        <div class="text-xs text-gray-400 mt-1.5">{{ notification.time }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useAuth } from "@/composables/useAuth";

const { supplier } = useAuth();

// Static notifications based on supplier data - in a real app these would come from an API
const notifications = computed(() => {
  const list = [];
  const s = supplier.value;
  if (!s) return list;

  if (s.portal_status === "Pending Approval") {
    list.push({
      type: "info",
      title: "Account Pending Approval",
      message: "Your account is being reviewed by our team. You'll be notified once it's approved.",
      time: "Now",
    });
  }

  return list;
});
</script>
