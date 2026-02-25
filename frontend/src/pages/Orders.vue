<template>
  <div class="space-y-4 animate-fade-in">
    <!-- Filters -->
    <div class="card flex flex-wrap items-end gap-3">
      <div class="flex-1 min-w-[200px]">
        <label class="label">Search</label>
        <div class="relative">
          <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input v-model="filters.search" type="text" class="input-field pl-9" placeholder="Order # or customer..." @keyup.enter="fetchOrders" />
        </div>
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
      <button @click="filters.page = 1; fetchOrders()" class="btn-primary">
        <svg xmlns="http://www.w3.org/2000/svg" class="inline w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
        Filter
      </button>
    </div>

    <!-- Orders table -->
    <div class="card p-0 overflow-hidden">
      <!-- Skeleton loading -->
      <template v-if="orders.loading">
        <div class="p-4 space-y-4">
          <div v-for="i in 6" :key="i" class="flex items-center gap-4">
            <div class="skeleton h-4 w-24" />
            <div class="skeleton h-4 w-32 hidden sm:block" />
            <div class="skeleton h-4 w-20" />
            <div class="flex-1" />
            <div class="skeleton h-4 w-20" />
            <div class="skeleton h-5 w-16 rounded-full" />
          </div>
        </div>
      </template>

      <!-- Empty state -->
      <div v-else-if="!orderList.length" class="p-12 text-center">
        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-gray-400"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        </div>
        <p class="text-sm font-medium text-gray-900">No orders found</p>
        <p class="text-xs text-gray-500 mt-1">Try adjusting your filters or check back later</p>
      </div>

      <!-- Table -->
      <table v-else class="w-full">
        <thead>
          <tr class="border-b border-gray-100 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
            <th class="px-4 py-3">Order</th>
            <th class="px-4 py-3 hidden sm:table-cell">Customer</th>
            <th class="px-4 py-3">Date</th>
            <th class="px-4 py-3 text-right">Amount</th>
            <th class="px-4 py-3">Status</th>
            <th class="px-4 py-3 hidden md:table-cell text-center">Items</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr
            v-for="order in orderList"
            :key="order.name"
            class="hover:bg-gray-50/80 cursor-pointer transition-colors group"
            @click="$router.push(`/suppliers/orders/${order.name}`)"
          >
            <td class="px-4 py-3.5">
              <span class="text-sm font-medium text-brand-600 group-hover:text-brand-700">{{ order.shopify_order_number || order.name }}</span>
            </td>
            <td class="px-4 py-3.5 text-sm text-gray-600 hidden sm:table-cell">{{ order.customer_name }}</td>
            <td class="px-4 py-3.5 text-sm text-gray-500">{{ order.transaction_date }}</td>
            <td class="px-4 py-3.5 text-sm font-semibold text-gray-900 text-right">{{ Math.round(order.supplier_total || 0).toLocaleString() }} MAD</td>
            <td class="px-4 py-3.5">
              <span class="badge" :class="statusBadge(order.custom_sales_status)">
                {{ order.custom_sales_status }}
              </span>
            </td>
            <td class="px-4 py-3.5 text-sm text-gray-500 hidden md:table-cell text-center">
              <span class="bg-gray-100 text-gray-600 text-xs font-medium px-2 py-0.5 rounded-md">{{ order.item_count }}</span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div v-if="orderData" class="px-4 py-3 border-t border-gray-100 flex items-center justify-between text-sm bg-gray-50/50">
        <span class="text-gray-500">
          Page {{ filters.page }} &middot; {{ orderData.total }} total orders
        </span>
        <div class="flex gap-2">
          <button :disabled="filters.page <= 1" @click="filters.page--; fetchOrders()" class="btn-secondary text-xs px-3 py-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" class="inline w-3.5 h-3.5 mr-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
            Previous
          </button>
          <button :disabled="!orderData.has_more" @click="filters.page++; fetchOrders()" class="btn-secondary text-xs px-3 py-1.5">
            Next
            <svg xmlns="http://www.w3.org/2000/svg" class="inline w-3.5 h-3.5 ml-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
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

function statusBadge(status) {
  const map = {
    Pending: "badge-yellow",
    Confirmed: "badge-blue",
    Cancelled: "badge-red",
    "On Hold": "badge-gray",
    "Follow Up": "badge-purple",
    "Did not Answer": "badge-orange",
  };
  return map[status] || "badge-gray";
}
</script>
