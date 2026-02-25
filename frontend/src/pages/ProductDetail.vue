<template>
  <div class="space-y-6 animate-fade-in">
    <router-link to="/suppliers/products" class="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 transition-colors group">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="group-hover:-translate-x-0.5 transition-transform"><polyline points="15 18 9 12 15 6"/></svg>
      Back to Products
    </router-link>

    <!-- Skeleton loading -->
    <template v-if="product.loading">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="card lg:col-span-1"><div class="skeleton aspect-square rounded-lg" /></div>
        <div class="card lg:col-span-2 space-y-4">
          <div class="skeleton h-7 w-64" />
          <div class="skeleton h-4 w-32" />
          <div class="grid grid-cols-2 gap-4">
            <div v-for="i in 4" :key="i" class="space-y-1.5"><div class="skeleton h-3 w-16" /><div class="skeleton h-4 w-24" /></div>
          </div>
        </div>
      </div>
    </template>

    <template v-else-if="data">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Image -->
        <div class="card lg:col-span-1">
          <div class="aspect-square bg-gray-100 rounded-xl overflow-hidden">
            <img v-if="data.image" :src="data.image" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
            </div>
          </div>
        </div>

        <!-- Details -->
        <div class="card lg:col-span-2 space-y-5">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ data.item_name }}</h2>
            <div class="text-sm text-gray-500 mt-1">{{ data.item_code }}</div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="bg-gray-50 rounded-xl p-3">
              <div class="text-xs text-gray-500 uppercase tracking-wide">Item Group</div>
              <div class="text-sm font-semibold mt-0.5">{{ data.item_group || '-' }}</div>
            </div>
            <div class="bg-gray-50 rounded-xl p-3">
              <div class="text-xs text-gray-500 uppercase tracking-wide">Price</div>
              <div class="text-sm font-semibold mt-0.5">{{ data.standard_rate ? `${data.standard_rate} MAD` : '-' }}</div>
            </div>
            <div class="bg-gray-50 rounded-xl p-3">
              <div class="text-xs text-gray-500 uppercase tracking-wide">UOM</div>
              <div class="text-sm font-semibold mt-0.5">{{ data.stock_uom || 'Nos' }}</div>
            </div>
            <div class="bg-gray-50 rounded-xl p-3">
              <div class="text-xs text-gray-500 uppercase tracking-wide">Total Stock</div>
              <div class="text-sm font-semibold mt-0.5" :class="data.total_stock > 0 ? 'text-green-600' : 'text-red-600'">{{ data.total_stock }}</div>
            </div>
          </div>

          <div v-if="data.description">
            <div class="text-xs text-gray-500 uppercase tracking-wide mb-1.5">Description</div>
            <div class="text-sm text-gray-700 prose prose-sm max-w-none" v-html="data.description" />
          </div>
        </div>
      </div>

      <!-- Stock by warehouse -->
      <div v-if="data.stock_by_warehouse?.length" class="card">
        <h3 class="font-semibold text-gray-900 mb-4">Stock by Warehouse</h3>
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-xs text-gray-500 uppercase tracking-wide border-b border-gray-100">
              <th class="pb-2.5">Warehouse</th>
              <th class="pb-2.5 text-right">Qty</th>
              <th class="pb-2.5 text-right">Reserved</th>
              <th class="pb-2.5 text-right">Available</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="wh in data.stock_by_warehouse" :key="wh.warehouse" class="hover:bg-gray-50/80 transition-colors">
              <td class="py-2.5 text-gray-700">{{ wh.warehouse }}</td>
              <td class="py-2.5 text-right">{{ wh.qty }}</td>
              <td class="py-2.5 text-right text-gray-500">{{ wh.reserved }}</td>
              <td class="py-2.5 text-right font-semibold" :class="(wh.qty - wh.reserved) > 0 ? 'text-green-600' : 'text-red-600'">{{ wh.qty - wh.reserved }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Variants -->
      <div v-if="data.variants?.length" class="card">
        <h3 class="font-semibold text-gray-900 mb-4">Variants ({{ data.variants.length }})</h3>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
          <div
            v-for="variant in data.variants"
            :key="variant.item_code"
            class="border border-gray-200 rounded-xl p-3 text-sm hover:border-gray-300 hover:shadow-sm transition-all"
          >
            <div class="font-medium text-gray-900 truncate">{{ variant.item_name }}</div>
            <div class="text-xs text-gray-500 mt-0.5">{{ variant.item_code }}</div>
            <div class="mt-2">
              <span class="badge" :class="variant.stock_qty > 0 ? 'badge-green' : 'badge-red'">
                {{ variant.stock_qty }} in stock
              </span>
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
