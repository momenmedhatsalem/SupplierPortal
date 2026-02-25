<template>
  <div class="space-y-6">
    <!-- Quick stats -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="stat in quickStats" :key="stat.label" class="card">
        <div class="text-sm text-gray-500">{{ stat.label }}</div>
        <div class="text-2xl font-bold mt-1" :class="stat.color">
          {{ stat.loading ? '...' : stat.value }}
        </div>
        <div v-if="stat.sub" class="text-xs text-gray-400 mt-1">{{ stat.sub }}</div>
      </div>
    </div>

    <!-- Rating + Recommendation -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div class="card">
        <h3 class="text-sm font-medium text-gray-500 mb-3">Performance Rating</h3>
        <div v-if="performance.loading" class="text-gray-400">Loading...</div>
        <div v-else-if="perf">
          <div class="flex items-center gap-3">
            <span class="text-4xl font-bold text-gray-900">{{ perf.rating }}</span>
            <div class="flex gap-0.5">
              <span v-for="i in 5" :key="i" class="text-xl" :class="i <= Math.round(perf.rating) ? 'text-yellow-400' : 'text-gray-200'">
                &#9733;
              </span>
            </div>
          </div>
          <div
            class="mt-3 text-sm px-3 py-2 rounded-lg"
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

      <div class="card">
        <h3 class="text-sm font-medium text-gray-500 mb-3">Stock Health</h3>
        <div v-if="performance.loading" class="text-gray-400">Loading...</div>
        <div v-else-if="perf">
          <div class="flex items-baseline gap-2">
            <span class="text-4xl font-bold text-gray-900">{{ perf.stock?.total_items || 0 }}</span>
            <span class="text-sm text-gray-500">products</span>
          </div>
          <div class="mt-3 grid grid-cols-3 gap-3">
            <div class="text-center">
              <div class="text-lg font-semibold text-green-600">{{ perf.stock?.total_items - (perf.stock?.low_stock_count || 0) - (perf.stock?.out_of_stock_count || 0) }}</div>
              <div class="text-xs text-gray-500">In Stock</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-semibold text-yellow-600">{{ perf.stock?.low_stock_count || 0 }}</div>
              <div class="text-xs text-gray-500">Low Stock</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-semibold text-red-600">{{ perf.stock?.out_of_stock_count || 0 }}</div>
              <div class="text-xs text-gray-500">Out of Stock</div>
            </div>
          </div>
          <div class="mt-3">
            <span
              class="text-xs px-2 py-1 rounded-full font-medium"
              :class="{
                'bg-green-100 text-green-700': perf.stock?.health === 'Healthy',
                'bg-yellow-100 text-yellow-700': perf.stock?.health === 'Good',
                'bg-red-100 text-red-700': perf.stock?.health === 'Low',
              }"
            >
              {{ perf.stock?.health || 'Unknown' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent orders -->
    <div class="card">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-medium text-gray-500">Recent Orders</h3>
        <router-link to="/suppliers/orders" class="text-sm text-brand-600 hover:text-brand-700">
          View all
        </router-link>
      </div>
      <div v-if="orders.loading" class="text-gray-400 text-sm">Loading orders...</div>
      <div v-else-if="orderList.length === 0" class="text-gray-400 text-sm">No orders yet</div>
      <div v-else class="divide-y divide-gray-100">
        <router-link
          v-for="order in orderList"
          :key="order.name"
          :to="`/suppliers/orders/${order.name}`"
          class="flex items-center justify-between py-3 hover:bg-gray-50 -mx-2 px-2 rounded-lg transition"
        >
          <div>
            <div class="text-sm font-medium text-gray-900">{{ order.shopify_order_number || order.name }}</div>
            <div class="text-xs text-gray-500">{{ order.customer_name }} &middot; {{ order.transaction_date }}</div>
          </div>
          <div class="text-right">
            <div class="text-sm font-medium text-gray-900">{{ order.supplier_total }} MAD</div>
            <span
              class="text-xs px-2 py-0.5 rounded-full"
              :class="statusClass(order.custom_sales_status)"
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
    { label: "Total Orders", value: p?.kpis?.total_orders || 0, color: "text-gray-900", loading: performance.loading, sub: "Last 90 days" },
    { label: "Confirmation Rate", value: `${p?.kpis?.confirmation_rate || 0}%`, color: "text-green-600", loading: performance.loading },
    { label: "Cancellation Rate", value: `${p?.kpis?.cancellation_rate || 0}%`, color: "text-red-600", loading: performance.loading },
    { label: "Revenue", value: `${Math.round(p?.kpis?.total_revenue || 0).toLocaleString()} MAD`, color: "text-brand-600", loading: performance.loading },
  ];
});

function statusClass(status) {
  const map = {
    Pending: "bg-yellow-100 text-yellow-700",
    Confirmed: "bg-blue-100 text-blue-700",
    Cancelled: "bg-red-100 text-red-700",
    "On Hold": "bg-gray-100 text-gray-700",
  };
  return map[status] || "bg-gray-100 text-gray-700";
}
</script>
