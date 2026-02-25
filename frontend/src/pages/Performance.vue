<template>
  <div class="space-y-6 animate-fade-in">
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
      <button @click="refresh" class="btn-primary">
        <svg xmlns="http://www.w3.org/2000/svg" class="inline w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
        Apply
      </button>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-3 gap-4">
      <template v-if="performance.loading">
        <div v-for="i in 6" :key="i" class="card">
          <div class="skeleton-text-sm mb-2" />
          <div class="skeleton h-9 w-24" />
        </div>
      </template>
      <template v-else>
        <div
          v-for="(kpi, i) in kpis"
          :key="kpi.label"
          class="card animate-fade-in-up"
          :class="`stagger-${i + 1}`"
        >
          <div class="text-xs text-gray-500 font-medium uppercase tracking-wide">{{ kpi.label }}</div>
          <div class="text-3xl font-bold mt-1.5" :class="kpi.color">
            {{ kpi.value }}
          </div>
        </div>
      </template>
    </div>

    <!-- Rating -->
    <div class="card">
      <h3 class="font-semibold text-gray-900 mb-5">Performance Rating</h3>
      <template v-if="performance.loading">
        <div class="flex items-center gap-6">
          <div class="skeleton-circle w-20 h-20" />
          <div class="flex-1 space-y-3">
            <div v-for="i in 4" :key="i" class="flex items-center gap-3">
              <div class="skeleton h-3 w-28" />
              <div class="flex-1 skeleton h-2 rounded-full" />
              <div class="skeleton h-3 w-10" />
            </div>
          </div>
        </div>
      </template>
      <div v-else-if="perf" class="flex flex-col sm:flex-row items-start sm:items-center gap-6">
        <div class="text-center flex-shrink-0">
          <div class="relative inline-block">
            <svg class="w-24 h-24 -rotate-90" viewBox="0 0 36 36">
              <path class="text-gray-100" stroke="currentColor" stroke-width="3" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              <path
                :class="perf.rating >= 3.5 ? 'text-green-500' : perf.rating >= 2.5 ? 'text-yellow-500' : 'text-red-500'"
                stroke="currentColor" stroke-width="3" stroke-linecap="round" fill="none"
                :stroke-dasharray="`${(perf.rating / 5) * 100}, 100`"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                style="transition: stroke-dasharray 1s ease-out;"
              />
            </svg>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-2xl font-bold text-gray-900">{{ perf.rating }}</span>
            </div>
          </div>
          <div class="flex gap-0.5 mt-2 justify-center">
            <span v-for="i in 5" :key="i" class="text-xl" :class="i <= Math.round(perf.rating) ? 'text-yellow-400' : 'text-gray-200'">
              &#9733;
            </span>
          </div>
          <div class="text-xs text-gray-500 mt-1">out of 5.0</div>
        </div>
        <div class="flex-1 space-y-3 w-full">
          <div v-for="bar in ratingBreakdown" :key="bar.label" class="flex items-center gap-3">
            <span class="text-xs text-gray-500 w-32 flex-shrink-0">{{ bar.label }}</span>
            <div class="flex-1 bg-gray-100 rounded-full h-2.5 overflow-hidden">
              <div
                class="h-2.5 rounded-full transition-all duration-1000 ease-out"
                :class="bar.color"
                :style="{ width: `${bar.value}%` }"
              />
            </div>
            <span class="text-xs font-semibold text-gray-700 w-10 text-right">{{ bar.value }}%</span>
          </div>
        </div>
      </div>
      <div v-if="perf?.recommendation" class="mt-5 p-3.5 rounded-xl text-sm font-medium" :class="recommendationClass">
        {{ perf.recommendation.text }}
      </div>
    </div>

    <!-- Trend chart -->
    <div class="card">
      <h3 class="font-semibold text-gray-900 mb-5">Monthly Trends</h3>
      <template v-if="trends.loading">
        <div class="space-y-3">
          <div v-for="i in 5" :key="i" class="flex items-center gap-4">
            <div class="skeleton h-3 w-16" />
            <div class="flex-1 skeleton h-4 rounded-full" />
            <div class="skeleton h-3 w-20" />
          </div>
        </div>
      </template>
      <div v-else-if="trendData.length === 0" class="text-center py-8">
        <div class="w-14 h-14 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-gray-400"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        </div>
        <p class="text-sm text-gray-500">No trend data available</p>
        <p class="text-xs text-gray-400 mt-1">Data will appear here as orders come in</p>
      </div>
      <div v-else class="space-y-2.5">
        <div v-for="(month, i) in trendData" :key="month.month" class="flex items-center gap-4 animate-fade-in-up" :class="`stagger-${Math.min(i + 1, 6)}`">
          <span class="text-xs text-gray-500 w-16 flex-shrink-0 font-medium">{{ month.month }}</span>
          <div class="flex-1 bg-gray-100 rounded-full h-4 overflow-hidden">
            <div class="h-4 rounded-full bg-gradient-to-r from-brand-400 to-brand-600 transition-all duration-700" :style="{ width: `${getBarWidth(month.order_count)}%` }" />
          </div>
          <span class="text-xs font-semibold text-gray-700 w-20 text-right">{{ month.order_count }} orders</span>
          <span class="text-xs text-gray-500 w-28 text-right hidden sm:inline">{{ Math.round(month.revenue).toLocaleString() }} MAD</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
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
    "bg-green-50 text-green-700 ring-1 ring-inset ring-green-600/10": level === "excellent" || level === "good",
    "bg-yellow-50 text-yellow-700 ring-1 ring-inset ring-yellow-600/10": level === "average",
    "bg-red-50 text-red-700 ring-1 ring-inset ring-red-600/10": level === "below_average" || level === "critical",
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
