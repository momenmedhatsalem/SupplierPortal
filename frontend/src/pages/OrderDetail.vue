<template>
  <div class="space-y-6">
    <!-- Back link -->
    <router-link to="/suppliers/orders" class="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
      Back to Orders
    </router-link>

    <div v-if="order.loading" class="card text-center py-12 text-gray-400">Loading order...</div>
    <div v-else-if="order.error" class="card text-center py-12 text-red-500">{{ order.error }}</div>
    <template v-else-if="orderData">
      <!-- Order header -->
      <div class="card">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ orderData.shopify_order_number || orderData.name }}</h2>
            <div class="text-sm text-gray-500 mt-1">
              {{ orderData.customer_name }} &middot; {{ orderData.transaction_date }}
            </div>
          </div>
          <div class="text-right">
            <div class="text-xl font-bold text-gray-900">{{ Math.round(orderData.supplier_total || 0).toLocaleString() }} MAD</div>
            <div class="text-xs text-gray-500">{{ orderData.supplier_item_count }} item(s)</div>
          </div>
        </div>
        <div class="flex gap-2 mt-4">
          <span class="text-xs px-2 py-1 rounded-full" :class="salesStatusClass">
            Sales: {{ orderData.custom_sales_status }}
          </span>
          <span class="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-700">
            Logistics: {{ orderData.custom_logistics_status }}
          </span>
        </div>
      </div>

      <!-- Items table -->
      <div class="card p-0 overflow-hidden">
        <div class="px-4 py-3 border-b border-gray-100">
          <h3 class="font-semibold text-gray-900">Your Items</h3>
        </div>
        <div class="divide-y divide-gray-50">
          <div v-for="item in orderData.items" :key="item.name" class="p-4 flex flex-wrap items-center gap-4">
            <!-- Image -->
            <div class="w-14 h-14 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
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
                <span v-if="item.color"> &middot; {{ item.color }}</span>
                <span v-if="item.size"> &middot; {{ item.size }}</span>
              </div>
              <div class="text-xs text-gray-500">Qty: {{ item.qty }} &times; {{ item.rate }} MAD = {{ Math.round(item.amount).toLocaleString() }} MAD</div>
            </div>

            <!-- Status + Actions -->
            <div class="flex items-center gap-2">
              <span class="text-xs px-2 py-1 rounded-full" :class="itemStatusClass(item.status)">
                {{ item.status || 'New Order' }}
              </span>
              <!-- Action buttons based on current status -->
              <template v-if="item.status === 'New Order' || !item.status">
                <button @click="updateStatus(item.name, 'Preparing')" :disabled="updating" class="text-xs btn-primary px-3 py-1">
                  Confirm
                </button>
                <button @click="updateStatus(item.name, 'Cancelled')" :disabled="updating" class="text-xs text-red-600 hover:text-red-700 px-2 py-1">
                  Cancel
                </button>
              </template>
              <template v-else-if="item.status === 'Preparing'">
                <button @click="updateStatus(item.name, 'Shipped')" :disabled="updating" class="text-xs btn-primary px-3 py-1">
                  Mark Shipped
                </button>
                <button @click="updateStatus(item.name, 'Cancelled')" :disabled="updating" class="text-xs text-red-600 hover:text-red-700 px-2 py-1">
                  Cancel
                </button>
              </template>
              <template v-else-if="item.status === 'Shipped'">
                <span class="text-xs text-green-600">Shipped</span>
              </template>
              <template v-else-if="item.status === 'Delivered in WH'">
                <span class="text-xs text-green-600">Delivered</span>
              </template>
              <template v-else-if="item.status === 'Cancelled'">
                <span class="text-xs text-red-500">Cancelled</span>
              </template>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useOrderDetail } from "@/composables/useOrders";

const route = useRoute();
const { order, updateItemStatus, updating } = useOrderDetail(route.params.id);

const orderData = computed(() => order.data);

const salesStatusClass = computed(() => {
  const map = {
    Pending: "bg-yellow-100 text-yellow-700",
    Confirmed: "bg-blue-100 text-blue-700",
    Cancelled: "bg-red-100 text-red-700",
  };
  return map[orderData.value?.custom_sales_status] || "bg-gray-100 text-gray-700";
});

function itemStatusClass(status) {
  const map = {
    "New Order": "bg-yellow-100 text-yellow-700",
    Preparing: "bg-blue-100 text-blue-700",
    Shipped: "bg-green-100 text-green-700",
    "Delivered in WH": "bg-green-100 text-green-700",
    Cancelled: "bg-red-100 text-red-700",
  };
  return map[status] || "bg-yellow-100 text-yellow-700";
}

async function updateStatus(itemName, newStatus) {
  if (newStatus === "Cancelled" && !confirm("Are you sure you want to cancel this item?")) return;
  await updateItemStatus(itemName, newStatus);
}
</script>
