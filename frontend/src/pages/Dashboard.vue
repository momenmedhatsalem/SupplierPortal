<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Quick stats -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Skeleton loading state -->
      <template v-if="performance.loading">
        <div v-for="i in 4" :key="i" class="card">
          <div class="flex items-center gap-3">
            <div class="skeleton-circle w-10 h-10" />
            <div class="flex-1">
              <div class="skeleton-text-sm mb-2" />
              <div class="skeleton h-7 w-20" />
            </div>
          </div>
        </div>
      </template>
      <!-- Loaded state -->
      <template v-else>
        <div
          v-for="(stat, i) in quickStats"
          :key="stat.label"
          class="card animate-fade-in-up"
          :class="`stagger-${i + 1}`"
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0" :class="stat.iconBg">
              <div v-html="stat.icon" />
            </div>
            <div class="min-w-0">
              <div class="text-xs text-gray-500 font-medium uppercase tracking-wide">{{ stat.label }}</div>
              <div class="text-xl font-bold mt-0.5 truncate" :class="stat.color">
                {{ stat.value }}
              </div>
            </div>
          </div>
          <div v-if="stat.sub" class="text-xs text-gray-400 mt-2 pl-[52px]">{{ stat.sub }}</div>
        </div>
      </template>
    </div>

    <!-- Rating + Stock Health -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Rating card -->
      <div class="card">
        <h3 class="text-sm font-medium text-gray-500 mb-4">Performance Rating</h3>
        <!-- Skeleton -->
        <template v-if="performance.loading">
          <div class="flex items-center gap-4">
            <div class="skeleton-circle w-16 h-16" />
            <div class="flex-1 space-y-2">
              <div class="skeleton-text" />
              <div class="skeleton-text-sm" />
            </div>
          </div>
        </template>
        <!-- Loaded -->
        <template v-else-if="perf">
          <div class="flex items-center gap-4">
            <div class="relative">
              <svg class="w-20 h-20 -rotate-90" viewBox="0 0 36 36">
                <path class="text-gray-100" stroke="currentColor" stroke-width="3" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path
                  class="text-brand-500"
                  stroke="currentColor"
                  stroke-width="3"
                  stroke-linecap="round"
                  fill="none"
                  :stroke-dasharray="`${(perf.rating / 5) * 100}, 100`"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  style="transition: stroke-dasharray 1s ease-out;"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-2xl font-bold text-gray-900">{{ perf.rating }}</span>
              </div>
            </div>
            <div>
              <div class="flex gap-0.5">
                <span v-for="i in 5" :key="i" class="text-lg" :class="i <= Math.round(perf.rating) ? 'text-yellow-400' : 'text-gray-200'">
                  &#9733;
                </span>
              </div>
              <div
                class="mt-2 text-sm px-3 py-1.5 rounded-lg inline-block"
                :class="{
                  'bg-green-50 text-green-700': perf.recommendation?.level === 'excellent' || perf.recommendation?.level === 'good',
                  'bg-yellow-50 text-yellow-700': perf.recommendation?.level === 'average',
                  'bg-red-50 text-red-700': perf.recommendation?.level === 'below_average' || perf.recommendation?.level === 'critical',
                }"
              >
                {{ perf.recommendation?.text }}
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- Stock Health card -->
      <div class="card">
        <h3 class="text-sm font-medium text-gray-500 mb-4">Stock Health</h3>
        <!-- Skeleton -->
        <template v-if="performance.loading">
          <div class="flex items-center gap-4">
            <div class="skeleton-circle w-16 h-16" />
            <div class="flex-1 space-y-2">
              <div class="skeleton-text" />
              <div class="skeleton-text-sm" />
            </div>
          </div>
        </template>
        <!-- Loaded -->
        <template v-else-if="perf">
          <div class="flex items-center gap-4 mb-4">
            <div class="text-4xl font-bold text-gray-900">{{ perf.stock?.total_items || 0 }}</div>
            <div class="text-sm text-gray-500">total products</div>
            <span
              class="ml-auto badge"
              :class="{
                'badge-green': perf.stock?.health === 'Healthy',
                'badge-yellow': perf.stock?.health === 'Good',
                'badge-red': perf.stock?.health === 'Low',
                'badge-gray': !perf.stock?.health || perf.stock?.health === 'Unknown',
              }"
            >
              {{ perf.stock?.health || 'Unknown' }}
            </span>
          </div>
          <div class="grid grid-cols-3 gap-3">
            <div class="bg-green-50 rounded-xl p-3 text-center">
              <div class="text-lg font-bold text-green-700">{{ (perf.stock?.total_items || 0) - (perf.stock?.low_stock_count || 0) - (perf.stock?.out_of_stock_count || 0) }}</div>
              <div class="text-xs text-green-600 mt-0.5">In Stock</div>
            </div>
            <div class="bg-yellow-50 rounded-xl p-3 text-center">
              <div class="text-lg font-bold text-yellow-700">{{ perf.stock?.low_stock_count || 0 }}</div>
              <div class="text-xs text-yellow-600 mt-0.5">Low Stock</div>
            </div>
            <div class="bg-red-50 rounded-xl p-3 text-center">
              <div class="text-lg font-bold text-red-700">{{ perf.stock?.out_of_stock_count || 0 }}</div>
              <div class="text-xs text-red-600 mt-0.5">Out of Stock</div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Recent orders -->
    <div class="card">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-medium text-gray-500">Recent Orders</h3>
        <router-link to="/suppliers/orders" class="text-sm text-brand-600 hover:text-brand-700 font-medium flex items-center gap-1">
          View all
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        </router-link>
      </div>

      <!-- Skeleton loading -->
      <template v-if="orders.loading">
        <div v-for="i in 4" :key="i" class="flex items-center justify-between py-3">
          <div class="flex items-center gap-3">
            <div class="skeleton-circle w-9 h-9" />
            <div>
              <div class="skeleton h-4 w-24 mb-1.5" />
              <div class="skeleton h-3 w-36" />
            </div>
          </div>
          <div class="text-right">
            <div class="skeleton h-4 w-16 mb-1.5 ml-auto" />
            <div class="skeleton h-5 w-20 ml-auto rounded-full" />
          </div>
        </div>
      </template>

      <!-- Empty state -->
      <div v-else-if="orderList.length === 0" class="text-center py-8">
        <div class="w-14 h-14 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-gray-400"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        </div>
        <p class="text-sm text-gray-500">No orders yet</p>
        <p class="text-xs text-gray-400 mt-1">Orders will appear here once customers start purchasing</p>
      </div>

      <!-- Orders list -->
      <div v-else class="divide-y divide-gray-100">
        <router-link
          v-for="(order, i) in orderList"
          :key="order.name"
          :to="`/suppliers/orders/${order.name}`"
          class="flex items-center justify-between py-3 hover:bg-gray-50 -mx-3 px-3 rounded-lg transition-colors group animate-fade-in-up"
          :class="`stagger-${i + 1}`"
        >
          <div class="flex items-center gap-3 min-w-0">
            <div class="w-9 h-9 bg-brand-50 text-brand-600 rounded-lg flex items-center justify-center flex-shrink-0 text-xs font-bold">
              {{ (order.shopify_order_number || order.name).toString().slice(-3) }}
            </div>
            <div class="min-w-0">
              <div class="text-sm font-medium text-gray-900 group-hover:text-brand-700 transition-colors truncate">
                {{ order.shopify_order_number || order.name }}
              </div>
              <div class="text-xs text-gray-500">{{ order.customer_name }} &middot; {{ order.transaction_date }}</div>
            </div>
          </div>
          <div class="text-right flex-shrink-0 ml-4">
            <div class="text-sm font-semibold text-gray-900">{{ Math.round(order.supplier_total || 0).toLocaleString() }} MAD</div>
            <span
              class="badge mt-1"
              :class="statusBadge(order.custom_sales_status)"
            >
              {{ order.custom_sales_status }}
            </span>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { usePerformance } from "@/composables/usePerformance";
import { useOrders } from "@/composables/useOrders";

const { performance } = usePerformance();
const { orders, fetchOrders } = useOrders();

onMounted(() => fetchOrders());

const perf = computed(() => performance.data);
const orderList = computed(() => orders.data?.data?.slice(0, 5) || []);

const quickStats = computed(() => {
  const p = perf.value;
  return [
    {
      label: "Total Orders",
      value: p?.kpis?.total_orders || 0,
      color: "text-gray-900",
      sub: "Last 90 days",
      iconBg: "bg-blue-50 text-blue-600",
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg>',
    },
    {
      label: "Confirmation",
      value: `${p?.kpis?.confirmation_rate || 0}%`,
      color: "text-green-600",
      iconBg: "bg-green-50 text-green-600",
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    },
    {
      label: "Cancellation",
      value: `${p?.kpis?.cancellation_rate || 0}%`,
      color: "text-red-600",
      iconBg: "bg-red-50 text-red-600",
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    },
    {
      label: "Revenue",
      value: `${Math.round(p?.kpis?.total_revenue || 0).toLocaleString()} MAD`,
      color: "text-brand-600",
      iconBg: "bg-brand-50 text-brand-600",
      icon: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    },
  ];
});

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
