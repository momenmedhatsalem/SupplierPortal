<template>
  <div class="space-y-4 animate-fade-in">
    <!-- Search -->
    <div class="card flex items-end gap-3">
      <div class="flex-1">
        <label class="label">Search Products</label>
        <div class="relative">
          <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input v-model="filters.search" type="text" class="input-field pl-9" placeholder="Product name or code..." @keyup.enter="filters.page = 1; fetchProducts()" />
        </div>
      </div>
      <button @click="filters.page = 1; fetchProducts()" class="btn-primary">Search</button>
    </div>

    <!-- Skeleton loading -->
    <template v-if="products.loading">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div v-for="i in 8" :key="i" class="card p-4">
          <div class="skeleton aspect-square rounded-lg mb-3" />
          <div class="skeleton h-4 w-3/4 mb-1.5" />
          <div class="skeleton h-3 w-1/2 mb-3" />
          <div class="flex justify-between">
            <div class="skeleton h-4 w-16" />
            <div class="skeleton h-5 w-20 rounded-full" />
          </div>
        </div>
      </div>
    </template>

    <!-- Empty state -->
    <div v-else-if="!productList.length" class="card text-center py-12">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-gray-400"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
      </div>
      <p class="text-sm font-medium text-gray-900">No products found</p>
      <p class="text-xs text-gray-500 mt-1">Try a different search or check back later</p>
    </div>

    <!-- Products grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <router-link
        v-for="(product, i) in productList"
        :key="product.item_code"
        :to="`/suppliers/products/${product.item_code}`"
        class="card-hover group p-4 animate-fade-in-up"
        :class="`stagger-${Math.min(i + 1, 6)}`"
      >
        <!-- Image -->
        <div class="aspect-square bg-gray-100 rounded-xl overflow-hidden mb-3">
          <img
            v-if="product.image"
            :src="product.image"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            loading="lazy"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
          </div>
        </div>

        <!-- Info -->
        <div class="text-sm font-medium text-gray-900 truncate group-hover:text-brand-600 transition-colors">
          {{ product.item_name }}
        </div>
        <div class="text-xs text-gray-500 truncate mt-0.5">{{ product.item_code }}</div>
        <div class="flex items-center justify-between mt-3">
          <span class="text-sm font-bold text-gray-900">
            {{ product.standard_rate ? `${product.standard_rate} MAD` : '-' }}
          </span>
          <span
            class="badge"
            :class="{
              'badge-green': product.stock_status === 'in_stock',
              'badge-yellow': product.stock_status === 'low_stock',
              'badge-red': product.stock_status === 'out_of_stock',
            }"
          >
            {{ product.stock_qty }} in stock
          </span>
        </div>
      </router-link>
    </div>

    <!-- Pagination -->
    <div v-if="productData && productList.length" class="flex items-center justify-between text-sm text-gray-500">
      <span>{{ productData.total }} products total</span>
      <div class="flex gap-2">
        <button :disabled="filters.page <= 1" @click="filters.page--; fetchProducts()" class="btn-secondary text-xs px-3 py-1.5">
          <svg xmlns="http://www.w3.org/2000/svg" class="inline w-3.5 h-3.5 mr-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
          Previous
        </button>
        <button :disabled="!productData.has_more" @click="filters.page++; fetchProducts()" class="btn-secondary text-xs px-3 py-1.5">
          Next
          <svg xmlns="http://www.w3.org/2000/svg" class="inline w-3.5 h-3.5 ml-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useProducts } from "@/composables/useProducts";

const { products, filters, fetchProducts } = useProducts();

onMounted(() => fetchProducts());

const productList = computed(() => products.data?.data || []);
const productData = computed(() => products.data);
</script>
