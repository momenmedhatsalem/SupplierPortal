<template>
  <div class="space-y-6">
    <!-- Summary cards -->
    <div class="grid grid-cols-2 lg:grid-cols-5 gap-4">
      <div class="card text-center">
        <div class="text-2xl font-bold text-gray-900">{{ summary?.total_items || 0 }}</div>
        <div class="text-xs text-gray-500">Total Products</div>
      </div>
      <div class="card text-center">
        <div class="text-2xl font-bold text-gray-900">{{ (summary?.total_stock || 0).toLocaleString() }}</div>
        <div class="text-xs text-gray-500">Total Stock</div>
      </div>
      <div class="card text-center">
        <div class="text-2xl font-bold text-green-600">{{ summary?.in_stock || 0 }}</div>
        <div class="text-xs text-gray-500">In Stock</div>
      </div>
      <div class="card text-center">
        <div class="text-2xl font-bold text-yellow-600">{{ summary?.low_stock || 0 }}</div>
        <div class="text-xs text-gray-500">Low Stock</div>
      </div>
      <div class="card text-center">
        <div class="text-2xl font-bold text-red-600">{{ summary?.out_of_stock || 0 }}</div>
        <div class="text-xs text-gray-500">Out of Stock</div>
      </div>
    </div>

    <!-- Stock filter -->
    <div class="card flex flex-wrap items-end gap-3">
      <div class="flex-1 min-w-[200px]">
        <label class="label">Search</label>
        <input v-model="search" type="text" class="input-field" placeholder="Product name or code..." @keyup.enter="fetchItems" />
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
      <div v-if="stockLevels.loading" class="p-8 text-center text-gray-400">Loading...</div>
      <div v-else-if="!items.length" class="p-8 text-center text-gray-400">No items found</div>
      <table v-else class="w-full">
        <thead>
          <tr class="border-b border-gray-100 text-left text-xs font-medium text-gray-500 uppercase">
            <th class="px-4 py-3">Product</th>
            <th class="px-4 py-3 text-right">Total</th>
            <th class="px-4 py-3 text-right hidden sm:table-cell">Reserved</th>
            <th class="px-4 py-3 text-right hidden sm:table-cell">Available</th>
            <th class="px-4 py-3">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr v-for="item in items" :key="item.item_code">
            <td class="px-4 py-3">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-gray-100 rounded overflow-hidden flex-shrink-0">
                  <img v-if="item.image" :src="item.image" class="w-full h-full object-cover" />
                </div>
                <div>
                  <div class="text-sm font-medium text-gray-900 truncate max-w-[200px]">{{ item.item_name }}</div>
                  <div class="text-xs text-gray-500">{{ item.item_code }}</div>
                </div>
              </div>
            </td>
            <td class="px-4 py-3 text-sm text-right font-medium">{{ item.total_stock }}</td>
            <td class="px-4 py-3 text-sm text-right text-gray-500 hidden sm:table-cell">{{ item.reserved_qty }}</td>
            <td class="px-4 py-3 text-sm text-right font-medium hidden sm:table-cell">{{ item.available_qty }}</td>
            <td class="px-4 py-3">
              <span
                class="text-xs px-2 py-0.5 rounded-full"
                :class="{
                  'bg-green-100 text-green-700': item.stock_status === 'in_stock',
                  'bg-yellow-100 text-yellow-700': item.stock_status === 'low_stock',
                  'bg-red-100 text-red-700': item.stock_status === 'out_of_stock',
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
