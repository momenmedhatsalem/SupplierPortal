<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Summary cards -->
    <div class="grid grid-cols-2 lg:grid-cols-5 gap-4">
      <template v-if="stockSummary.loading">
        <div v-for="i in 5" :key="i" class="card text-center">
          <div class="skeleton h-8 w-12 mx-auto mb-1" />
          <div class="skeleton h-3 w-16 mx-auto" />
        </div>
      </template>
      <template v-else>
        <div v-for="(card, i) in summaryCards" :key="card.label" class="card text-center animate-fade-in-up" :class="`stagger-${i + 1}`">
          <div class="text-2xl font-bold" :class="card.color">{{ card.value }}</div>
          <div class="text-xs text-gray-500 mt-0.5">{{ card.label }}</div>
        </div>
      </template>
    </div>

    <!-- Stock filter -->
    <div class="card flex flex-wrap items-end gap-3">
      <div class="flex-1 min-w-[200px]">
        <label class="label">Search</label>
        <div class="relative">
          <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input v-model="search" type="text" class="input-field pl-9" placeholder="Product name or code..." @keyup.enter="fetchItems" />
        </div>
      </div>
      <div>
        <label class="label">Filter</label>
        <select v-model="stockFilter" class="input-field" @change="fetchItems">
          <option value="">All</option>
          <option value="in_stock">In Stock</option>
          <option value="low_stock">Low Stock</option>
          <option value="out_of_stock">Out of Stock</option>
        </select>
      </div>
      <button @click="fetchItems" class="btn-primary">Search</button>
    </div>

    <!-- Stock table -->
    <div class="card p-0 overflow-hidden">
      <!-- Skeleton loading -->
      <template v-if="stockLevels.loading">
        <div class="p-4 space-y-4">
          <div v-for="i in 6" :key="i" class="flex items-center gap-4">
            <div class="skeleton w-10 h-10 rounded" />
            <div class="flex-1 space-y-1.5">
              <div class="skeleton h-4 w-40" />
              <div class="skeleton h-3 w-24" />
            </div>
            <div class="skeleton h-4 w-12" />
            <div class="skeleton h-5 w-14 rounded-full" />
          </div>
        </div>
      </template>

      <!-- Empty state -->
      <div v-else-if="!items.length" class="p-12 text-center">
        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-gray-400"><path d="M1 3h15v13H1z"/><path d="M16 8h4l3 3v5h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
        </div>
        <p class="text-sm font-medium text-gray-900">No items found</p>
        <p class="text-xs text-gray-500 mt-1">Try adjusting your filters</p>
      </div>

      <!-- Table -->
      <table v-else class="w-full">
        <thead>
          <tr class="border-b border-gray-100 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
            <th class="px-4 py-3">Product</th>
            <th class="px-4 py-3 text-right">Total</th>
            <th class="px-4 py-3 text-right hidden sm:table-cell">Reserved</th>
            <th class="px-4 py-3 text-right hidden sm:table-cell">Available</th>
            <th class="px-4 py-3">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr v-for="item in items" :key="item.item_code" class="hover:bg-gray-50/80 transition-colors">
            <td class="px-4 py-3.5">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
                  <img v-if="item.image" :src="item.image" class="w-full h-full object-cover" loading="lazy" />
                  <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>
                  </div>
                </div>
                <div class="min-w-0">
                  <div class="text-sm font-medium text-gray-900 truncate max-w-[200px]">{{ item.item_name }}</div>
                  <div class="text-xs text-gray-500">{{ item.item_code }}</div>
                </div>
              </div>
            </td>
            <td class="px-4 py-3.5 text-sm text-right font-semibold">{{ item.total_stock }}</td>
            <td class="px-4 py-3.5 text-sm text-right text-gray-500 hidden sm:table-cell">{{ item.reserved_qty }}</td>
            <td class="px-4 py-3.5 text-sm text-right font-semibold hidden sm:table-cell">{{ item.available_qty }}</td>
            <td class="px-4 py-3.5">
              <span
                class="badge"
                :class="{
                  'badge-green': item.stock_status === 'in_stock',
                  'badge-yellow': item.stock_status === 'low_stock',
                  'badge-red': item.stock_status === 'out_of_stock',
                }"
              >
                {{ item.stock_status === 'in_stock' ? 'In Stock' : item.stock_status === 'low_stock' ? 'Low' : 'Out' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { createResource } from "frappe-ui";

const search = ref("");
const stockFilter = ref("");

const stockSummary = createResource({
  url: "supplier_portal.api.inventory.get_stock_summary",
  auto: true,
});

const stockLevels = createResource({
  url: "supplier_portal.api.inventory.get_stock_levels",
  auto: false,
});

const summary = computed(() => stockSummary.data);
const items = computed(() => stockLevels.data?.data || []);

const summaryCards = computed(() => [
  { label: "Total Products", value: summary.value?.total_items || 0, color: "text-gray-900" },
  { label: "Total Stock", value: (summary.value?.total_stock || 0).toLocaleString(), color: "text-gray-900" },
  { label: "In Stock", value: summary.value?.in_stock || 0, color: "text-green-600" },
  { label: "Low Stock", value: summary.value?.low_stock || 0, color: "text-yellow-600" },
  { label: "Out of Stock", value: summary.value?.out_of_stock || 0, color: "text-red-600" },
]);

function fetchItems() {
  stockLevels.fetch({
    params: {
      search: search.value || undefined,
      stock_filter: stockFilter.value || undefined,
    },
  });
}

onMounted(() => fetchItems());
</script>
