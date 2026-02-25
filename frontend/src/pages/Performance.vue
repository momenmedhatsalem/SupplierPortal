<template>
  <div class="space-y-6">
    <!-- Date filter -->
    <div class="card flex flex-wrap items-end gap-4">
      <div>
        <label class="label">From</label>
        <input v-model="fromDate" type="date" class="input-field" />
      </div>
      <div>
        <label class="label">To</label>
        <input v-model="toDate" type="date" class="input-field" />
      </div>
      <button @click="refresh" class="btn-primary">Apply</button>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="kpi in kpis" :key="kpi.label" class="card">
        <div class="text-sm text-gray-500">{{ kpi.label }}</div>
        <div class="text-3xl font-bold mt-1" :class="kpi.color">
          {{ performance.loading ? '...' : kpi.value }}
        </div>
      </div>
    </div>

    <!-- Rating -->
    <div class="card">
      <h3 class="font-semibold text-gray-900 mb-4">Performance Rating</h3>
      <div v-if="perf" class="flex items-center gap-6">
        <div class="text-center">
          <div class="text-5xl font-bold text-gray-900">{{ perf.rating }}</div>
          <div class="flex gap-0.5 mt-2 justify-center">
            <span v-for="i in 5" :key="i" class="text-2xl" :class="i <= Math.round(perf.rating) ? 'text-yellow-400' : 'text-gray-200'">
              &#9733;
            </span>
          </div>
          <div class="text-sm text-gray-500 mt-1">out of 5.0</div>
        </div>
        <div class="flex-1 space-y-2">
          <div v-for="bar in ratingBreakdown" :key="bar.label" class="flex items-center gap-3">
            <span class="text-xs text-gray-500 w-32">{{ bar.label }}</span>
            <div class="flex-1 bg-gray-100 rounded-full h-2">
              <div class="h-2 rounded-full" :class="bar.color" :style="{ width: `${bar.value}%` }" />
            </div>
            <span class="text-xs font-medium text-gray-700 w-10 text-right">{{ bar.value }}%</span>
          </div>
        </div>
      </div>
      <div v-if="perf?.recommendation" class="mt-4 p-3 rounded-lg" :class="recommendationClass">
        {{ perf.recommendation.text }}
      </div>
    </div>

    <!-- Trend chart placeholder -->
    <div class="card">
      <h3 class="font-semibold text-gray-900 mb-4">Monthly Trends</h3>
      <div v-if="trends.loading" class="text-gray-400 text-sm">Loading trends...</div>
      <div v-else-if="trendData.length === 0" class="text-gray-400 text-sm">No trend data available</div>
      <div v-else class="space-y-2">
        <div v-for="month in trendData" :key="month.month" class="flex items-center gap-4">
          <span class="text-sm text-gray-500 w-20">{{ month.month }}</span>
          <div class="flex-1 bg-gray-100 rounded-full h-3">
            <div class="h-3 rounded-full bg-brand-500" :style="{ width: `${getBarWidth(month.order_count)}%` }" />
          </div>
          <span class="text-sm font-medium text-gray-700 w-20 text-right">{{ month.order_count }} orders</span>
          <span class="text-sm text-gray-500 w-28 text-right">{{ Math.round(month.revenue).toLocaleString() }} MAD</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { usePerformance } from "@/composables/usePerformance";

const fromDate = ref("");
const toDate = ref("");

const { performance, trends } = usePerformance();

const perf = computed(() => performance.data);
const trendData = computed(() => trends.data?.monthly || []);

const kpis = computed(() => {
  const p = perf.value?.kpis;
  return [
    { label: "Total Orders", value: p?.total_orders || 0, color: "text-gray-900" },
    { label: "Confirmation Rate", value: `${p?.confirmation_rate || 0}%`, color: "text-green-600" },
    { label: "Cancellation Rate", value: `${p?.cancellation_rate || 0}%`, color: "text-red-600" },
    { label: "Shipment Rate", value: `${p?.shipment_rate || 0}%`, color: "text-blue-600" },
    { label: "Total Revenue", value: `${Math.round(p?.total_revenue || 0).toLocaleString()} MAD`, color: "text-brand-600" },
    { label: "Avg Order Value", value: `${Math.round(p?.avg_order_value || 0).toLocaleString()} MAD`, color: "text-gray-900" },
  ];
});

const ratingBreakdown = computed(() => {
  const p = perf.value?.kpis;
  return [
    { label: "Confirmation (30%)", value: Math.round(p?.confirmation_rate || 0), color: "bg-green-500" },
    { label: "Low Cancel (30%)", value: Math.round(100 - (p?.cancellation_rate || 0)), color: "bg-blue-500" },
    { label: "Shipment (20%)", value: Math.round(p?.shipment_rate || 0), color: "bg-purple-500" },
    { label: "Stock Health (20%)", value: perf.value?.stock?.health === "Healthy" ? 100 : perf.value?.stock?.health === "Good" ? 70 : 30, color: "bg-amber-500" },
  ];
});

const recommendationClass = computed(() => {
  const level = perf.value?.recommendation?.level;
  return {
    "bg-green-50 text-green-700": level === "excellent" || level === "good",
    "bg-yellow-50 text-yellow-700": level === "average",
    "bg-red-50 text-red-700": level === "below_average" || level === "critical",
  };
});

function getBarWidth(count) {
  const max = Math.max(...trendData.value.map((m) => m.order_count), 1);
  return Math.round((count / max) * 100);
}

function refresh() {
  performance.fetch({ params: { from_date: fromDate.value || undefined, to_date: toDate.value || undefined } });
  trends.fetch({ params: { from_date: fromDate.value || undefined, to_date: toDate.value || undefined } });
}
</script>
