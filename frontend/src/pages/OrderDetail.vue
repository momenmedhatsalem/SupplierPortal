<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Back link -->
    <router-link to="/suppliers/orders" class="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 transition-colors group">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="group-hover:-translate-x-0.5 transition-transform"><polyline points="15 18 9 12 15 6"/></svg>
      Back to Orders
    </router-link>

    <!-- Skeleton loading -->
    <template v-if="order.loading">
      <div class="card">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div class="space-y-2">
            <div class="skeleton h-7 w-40" />
            <div class="skeleton h-4 w-56" />
          </div>
          <div class="text-right space-y-2">
            <div class="skeleton h-7 w-28 ml-auto" />
            <div class="skeleton h-4 w-20 ml-auto" />
          </div>
        </div>
      </div>
      <div class="card p-0">
        <div class="p-4 border-b border-gray-100"><div class="skeleton h-5 w-24" /></div>
        <div v-for="i in 3" :key="i" class="p-4 flex items-center gap-4">
          <div class="skeleton w-14 h-14 rounded-lg" />
          <div class="flex-1 space-y-2"><div class="skeleton h-4 w-48" /><div class="skeleton h-3 w-32" /></div>
          <div class="skeleton h-6 w-20 rounded-full" />
        </div>
      </div>
    </template>

    <div v-else-if="order.error" class="card text-center py-12">
      <div class="w-14 h-14 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-3">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-red-500"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      </div>
      <p class="text-sm text-red-600">{{ order.error }}</p>
    </div>

    <template v-else-if="orderData">
      <!-- Order header -->
      <div class="card">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ orderData.shopify_order_number || orderData.name }}</h2>
            <div class="text-sm text-gray-500 mt-1 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              {{ orderData.customer_name }}
              <span class="text-gray-300">&middot;</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              {{ orderData.transaction_date }}
            </div>
          </div>
          <div class="text-right">
            <div class="text-2xl font-bold text-gray-900">{{ Math.round(orderData.supplier_total || 0).toLocaleString() }} MAD</div>
            <div class="text-xs text-gray-500 mt-1">{{ orderData.supplier_item_count }} item(s)</div>
          </div>
        </div>
        <div class="flex gap-2 mt-4">
          <span class="badge" :class="salesStatusBadge">
            Sales: {{ orderData.custom_sales_status }}
          </span>
          <span class="badge badge-gray">
            Logistics: {{ orderData.custom_logistics_status }}
          </span>
        </div>
      </div>

      <!-- Items -->
      <div class="card p-0 overflow-hidden">
        <div class="px-5 py-3.5 border-b border-gray-100 flex items-center justify-between">
          <h3 class="font-semibold text-gray-900">Your Items</h3>
          <span class="text-xs text-gray-500">{{ orderData.items?.length || 0 }} items</span>
        </div>
        <div class="divide-y divide-gray-100">
          <div v-for="item in orderData.items" :key="item.name" class="p-4 sm:p-5 flex flex-wrap items-center gap-4 hover:bg-gray-50/50 transition-colors">
            <!-- Image -->
            <div class="w-16 h-16 bg-gray-100 rounded-xl overflow-hidden flex-shrink-0">
              <img v-if="item.product_image || item.image" :src="item.product_image || item.image" class="w-full h-full object-cover" />
              <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
              </div>
            </div>

            <!-- Info -->
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900">{{ item.item_name }}</div>
              <div class="text-xs text-gray-500 mt-0.5">
                {{ item.sku ? `SKU: ${item.sku}` : item.item_code }}
                <span v-if="item.color" class="ml-1">&middot; {{ item.color }}</span>
                <span v-if="item.size" class="ml-1">&middot; {{ item.size }}</span>
              </div>
              <div class="text-xs text-gray-500 mt-0.5">
                Qty: {{ item.qty }} &times; {{ item.rate }} MAD =
                <span class="font-medium text-gray-700">{{ Math.round(item.amount).toLocaleString() }} MAD</span>
              </div>
            </div>

            <!-- Status + Actions -->
            <div class="flex items-center gap-2 flex-shrink-0">
              <span class="badge" :class="itemBadge(item.status)">
                {{ item.status || 'New Order' }}
              </span>

              <!-- Action buttons -->
              <template v-if="item.status === 'New Order' || !item.status">
                <button @click="updateStatus(item.name, 'Preparing')" :disabled="updating" class="btn-primary text-xs px-3 py-1.5">
                  Confirm
                </button>
                <button @click="confirmCancel(item.name)" :disabled="updating" class="text-xs text-red-600 hover:text-red-700 hover:bg-red-50 px-2 py-1.5 rounded-lg transition-colors">
                  Cancel
                </button>
              </template>
              <template v-else-if="item.status === 'Preparing'">
                <button @click="updateStatus(item.name, 'Shipped')" :disabled="updating" class="btn-primary text-xs px-3 py-1.5">
                  Mark Shipped
                </button>
                <button @click="confirmCancel(item.name)" :disabled="updating" class="text-xs text-red-600 hover:text-red-700 hover:bg-red-50 px-2 py-1.5 rounded-lg transition-colors">
                  Cancel
                </button>
              </template>
              <template v-else-if="item.status === 'Shipped'">
                <span class="text-xs text-green-600 font-medium flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                  Shipped
                </span>
              </template>
              <template v-else-if="item.status === 'Delivered in WH'">
                <span class="text-xs text-green-600 font-medium flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                  Delivered
                </span>
              </template>
              <template v-else-if="item.status === 'Cancelled'">
                <span class="text-xs text-red-500 font-medium">Cancelled</span>
              </template>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Cancel Confirmation Modal -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="showCancelModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showCancelModal = false" />
          <div class="relative bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6 animate-scale-in">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-red-600"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            </div>
            <h3 class="mt-4 text-lg font-semibold text-gray-900 text-center">Cancel Item?</h3>
            <p class="mt-2 text-sm text-gray-500 text-center">
              This action cannot be undone. The item will be marked as cancelled.
            </p>
            <div class="flex gap-3 mt-6">
              <button @click="showCancelModal = false" class="btn-secondary flex-1">Keep Item</button>
              <button @click="executeCancelAction" :disabled="updating" class="btn-danger flex-1">
                {{ updating ? 'Cancelling...' : 'Cancel Item' }}
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- Toast notification -->
    <teleport to="body">
      <transition name="toast">
        <div v-if="toast.show" :class="toast.type === 'success' ? 'toast-success' : 'toast-error'">
          <svg v-if="toast.type === 'success'" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          {{ toast.message }}
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from "vue";
import { useRoute } from "vue-router";
import { useOrderDetail } from "@/composables/useOrders";

const route = useRoute();
const { order, updateItemStatus, updating } = useOrderDetail(route.params.id);

const orderData = computed(() => order.data);

// Cancel confirmation modal
const showCancelModal = ref(false);
const cancelItemName = ref(null);

// Toast notifications
const toast = reactive({ show: false, message: "", type: "success" });

function showToast(message, type = "success") {
  toast.show = true;
  toast.message = message;
  toast.type = type;
  setTimeout(() => { toast.show = false; }, 3000);
}

const salesStatusBadge = computed(() => {
  const map = {
    Pending: "badge-yellow",
    Confirmed: "badge-blue",
    Cancelled: "badge-red",
  };
  return map[orderData.value?.custom_sales_status] || "badge-gray";
});

function itemBadge(status) {
  const map = {
    "New Order": "badge-yellow",
    Preparing: "badge-blue",
    Shipped: "badge-green",
    "Delivered in WH": "badge-green",
    Cancelled: "badge-red",
  };
  return map[status] || "badge-yellow";
}

function confirmCancel(itemName) {
  cancelItemName.value = itemName;
  showCancelModal.value = true;
}

async function executeCancelAction() {
  try {
    await updateItemStatus(cancelItemName.value, "Cancelled");
    showCancelModal.value = false;
    showToast("Item has been cancelled");
  } catch (e) {
    showToast("Failed to cancel item", "error");
  }
}

async function updateStatus(itemName, newStatus) {
  try {
    await updateItemStatus(itemName, newStatus);
    showToast(`Item updated to ${newStatus}`);
  } catch (e) {
    showToast("Failed to update status", "error");
  }
}
</script>

<style scoped>
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.toast-enter-active { transition: all 0.3s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from { opacity: 0; transform: translateY(12px) scale(0.95); }
.toast-leave-to { opacity: 0; transform: translateY(-8px) scale(0.95); }
</style>
