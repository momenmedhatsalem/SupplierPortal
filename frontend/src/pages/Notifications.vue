<template>
  <div class="space-y-4">
    <div v-if="!notifications.length" class="card text-center py-12">
      <div class="text-gray-400 mb-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="mx-auto"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
      </div>
      <p class="text-gray-500 text-sm">No notifications yet</p>
      <p class="text-gray-400 text-xs mt-1">Alerts about orders, stock, and performance will appear here</p>
    </div>

    <div v-for="(notification, i) in notifications" :key="i" class="card flex items-start gap-3">
      <div
        class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-sm"
        :class="{
          'bg-red-100 text-red-600': notification.type === 'urgent',
          'bg-yellow-100 text-yellow-600': notification.type === 'warning',
          'bg-blue-100 text-blue-600': notification.type === 'info',
          'bg-green-100 text-green-600': notification.type === 'success',
        }"
      >
        {{ notification.type === 'urgent' ? '!' : notification.type === 'warning' ? '?' : 'i' }}
      </div>
      <div>
        <div class="text-sm font-medium text-gray-900">{{ notification.title }}</div>
        <div class="text-sm text-gray-600 mt-0.5">{{ notification.message }}</div>
        <div class="text-xs text-gray-400 mt-1">{{ notification.time }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
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
