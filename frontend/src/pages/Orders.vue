<template>
  <div class="space-y-4">
    <!-- Filters -->
    <div class="card flex flex-wrap items-end gap-3">
      <div class="flex-1 min-w-[200px]">
        <label class="label">Search</label>
        <input v-model="filters.search" type="text" class="input-field" placeholder="Order # or customer..." @keyup.enter="fetchOrders" />
      </div>
      <div>
        <label class="label">Status</label>
        <select v-model="filters.status" class="input-field" @change="filters.page = 1; fetchOrders()">
          <option value="">All Statuses</option>
          <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
      <div>
        <label class="label">From</label>
        <input v-model="filters.from_date" type="date" class="input-field" />
      </div>
      <div>
        <label class="label">To</label>
        <input v-model="filters.to_date" type="date" class="input-field" />
      </div>
      <button @click="filters.page = 1; fetchOrders()" class="btn-primary">Filter</button>
    </div>

    <!-- Orders table -->
    <div class="card p-0 overflow-hidden">
      <div v-if="orders.loading" class="p-8 text-center text-gray-400">Loading orders...</div>
      <div v-else-if="!orderList.length" class="p-8 text-center text-gray-400">No orders found</div>
      <table v-else class="w-full">
        <thead>
          <tr class="border-b border-gray-100 text-left text-xs font-medium text-gray-500 uppercase">
            <th class="px-4 py-3">Order</th>
            <th class="px-4 py-3 hidden sm:table-cell">Customer</th>
            <th class="px-4 py-3">Date</th>
            <th class="px-4 py-3 text-right">Amount</th>
            <th class="px-4 py-3">Status</th>
            <th class="px-4 py-3 hidden md:table-cell">Items</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr
            v-for="order in orderList"
            :key="order.name"
            class="hover:bg-gray-50 cursor-pointer transition"
            @click="$router.push(`/suppliers/orders/${order.name}`)"
          >
            <td class="px-4 py-3 text-sm font-medium text-brand-600">{{ order.shopify_order_number || order.name }}</td>
            <td class="px-4 py-3 text-sm text-gray-600 hidden sm:table-cell">{{ order.customer_name }}</td>
            <td class="px-4 py-3 text-sm text-gray-600">{{ order.transaction_date }}</td>
            <td class="px-4 py-3 text-sm font-medium text-gray-900 text-right">{{ Math.round(order.supplier_total || 0).toLocaleString() }} MAD</td>
            <td class="px-4 py-3">
              <span class="text-xs px-2 py-0.5 rounded-full" :class="statusClass(order.custom_sales_status)">
                {{ order.custom_sales_status }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm text-gray-500 hidden md:table-cell">{{ order.item_count }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div v-if="orderData" class="px-4 py-3 border-t border-gray-100 flex items-center justify-between text-sm">
        <span class="text-gray-500">
          Page {{ filters.page }} &middot; {{ orderData.total }} total orders
        </span>
        <div class="flex gap-2">
          <button :disabled="filters.page <= 1" @click="filters.page--; fetchOrders()" class="btn-secondary text-xs px-3 py-1">
            Previous
          </button>
          <button :disabled="!orderData.has_more" @click="filters.page++; fetchOrders()" class="btn-secondary text-xs px-3 py-1">
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useOrders } from "@/composables/useOrders";

const { orders, filters, fetchOrders } = useOrders();

onMounted(() => fetchOrders());

const orderList = computed(() => orders.data?.data || []);
const orderData = computed(() => orders.data);

const statuses = ["Pending", "Confirmed", "Cancelled", "On Hold", "Follow Up", "Did not Answer"];

function statusClass(status) {
  const map = {
    Pending: "bg-yellow-100 text-yellow-700",
    Confirmed: "bg-blue-100 text-blue-700",
    Cancelled: "bg-red-100 text-red-700",
    "On Hold": "bg-gray-100 text-gray-700",
    "Follow Up": "bg-purple-100 text-purple-700",
    "Did not Answer": "bg-orange-100 text-orange-700",
  };
  return map[status] || "bg-gray-100 text-gray-700";
}
</script>
