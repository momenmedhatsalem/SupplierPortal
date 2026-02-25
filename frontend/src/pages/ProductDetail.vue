<template>
  <div class="space-y-6">
    <router-link to="/suppliers/products" class="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
      Back to Products
    </router-link>

    <div v-if="product.loading" class="card text-center py-12 text-gray-400">Loading product...</div>
    <template v-else-if="data">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Image -->
        <div class="card lg:col-span-1">
          <div class="aspect-square bg-gray-100 rounded-lg overflow-hidden">
            <img v-if="data.image" :src="data.image" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
            </div>
          </div>
        </div>

        <!-- Details -->
        <div class="card lg:col-span-2 space-y-4">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ data.item_name }}</h2>
            <div class="text-sm text-gray-500 mt-1">{{ data.item_code }}</div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <div class="text-xs text-gray-500 uppercase">Item Group</div>
              <div class="text-sm font-medium">{{ data.item_group || '-' }}</div>
            </div>
            <div>
              <div class="text-xs text-gray-500 uppercase">Price</div>
              <div class="text-sm font-medium">{{ data.standard_rate ? `${data.standard_rate} MAD` : '-' }}</div>
            </div>
            <div>
              <div class="text-xs text-gray-500 uppercase">UOM</div>
              <div class="text-sm font-medium">{{ data.stock_uom || 'Nos' }}</div>
            </div>
            <div>
              <div class="text-xs text-gray-500 uppercase">Total Stock</div>
              <div class="text-sm font-medium">{{ data.total_stock }}</div>
            </div>
          </div>

          <div v-if="data.description">
            <div class="text-xs text-gray-500 uppercase mb-1">Description</div>
            <div class="text-sm text-gray-700 prose prose-sm max-w-none" v-html="data.description" />
          </div>
        </div>
      </div>

      <!-- Stock by warehouse -->
      <div v-if="data.stock_by_warehouse?.length" class="card">
        <h3 class="font-semibold text-gray-900 mb-4">Stock by Warehouse</h3>
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-xs text-gray-500 uppercase border-b border-gray-100">
              <th class="pb-2">Warehouse</th>
              <th class="pb-2 text-right">Qty</th>
              <th class="pb-2 text-right">Reserved</th>
              <th class="pb-2 text-right">Available</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="wh in data.stock_by_warehouse" :key="wh.warehouse">
              <td class="py-2 text-gray-700">{{ wh.warehouse }}</td>
              <td class="py-2 text-right">{{ wh.qty }}</td>
              <td class="py-2 text-right text-gray-500">{{ wh.reserved }}</td>
              <td class="py-2 text-right font-medium">{{ wh.qty - wh.reserved }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Variants -->
      <div v-if="data.variants?.length" class="card">
        <h3 class="font-semibold text-gray-900 mb-4">Variants ({{ data.variants.length }})</h3>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
          <div v-for="variant in data.variants" :key="variant.item_code" class="border border-gray-200 rounded-lg p-3 text-sm">
            <div class="font-medium text-gray-900 truncate">{{ variant.item_name }}</div>
            <div class="text-xs text-gray-500">{{ variant.item_code }}</div>
            <div class="mt-1 text-xs" :class="variant.stock_qty > 0 ? 'text-green-600' : 'text-red-600'">
              {{ variant.stock_qty }} in stock
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
import { useProductDetail } from "@/composables/useProducts";

const route = useRoute();
const { product } = useProductDetail(route.params.code);
const data = computed(() => product.data);
</script>
