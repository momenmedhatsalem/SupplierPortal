<template>
  <div class="space-y-4">
    <!-- Search -->
    <div class="card flex items-end gap-3">
      <div class="flex-1">
        <label class="label">Search Products</label>
        <input v-model="filters.search" type="text" class="input-field" placeholder="Product name or code..." @keyup.enter="filters.page = 1; fetchProducts()" />
      </div>
      <button @click="filters.page = 1; fetchProducts()" class="btn-primary">Search</button>
    </div>

    <!-- Products grid -->
    <div v-if="products.loading" class="text-center py-12 text-gray-400">Loading products...</div>
    <div v-else-if="!productList.length" class="card text-center py-12 text-gray-400">No products found</div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <router-link
        v-for="product in productList"
        :key="product.item_code"
        :to="`/suppliers/products/${product.item_code}`"
        class="card hover:shadow-md transition group p-4"
      >
        <!-- Image -->
        <div class="aspect-square bg-gray-100 rounded-lg overflow-hidden mb-3">
          <img v-if="product.image" :src="product.image" class="w-full h-full object-cover" />
          <div v-else class="w-full h-full flex items-center justify-center text-gray-300">
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
          </div>
        </div>

        <!-- Info -->
        <div class="text-sm font-medium text-gray-900 truncate group-hover:text-brand-600">
          {{ product.item_name }}
        </div>
        <div class="text-xs text-gray-500 truncate mt-0.5">{{ product.item_code }}</div>
        <div class="flex items-center justify-between mt-2">
          <span class="text-sm font-semibold text-gray-900">
            {{ product.standard_rate ? `${product.standard_rate} MAD` : '-' }}
          </span>
          <span
            class="text-xs px-2 py-0.5 rounded-full"
            :class="{
              'bg-green-100 text-green-700': product.stock_status === 'in_stock',
              'bg-yellow-100 text-yellow-700': product.stock_status === 'low_stock',
              'bg-red-100 text-red-700': product.stock_status === 'out_of_stock',
            }"
          >
            {{ product.stock_qty }} in stock
          </span>
        </div>
      </router-link>
    </div>

    <!-- Pagination -->
    <div v-if="productData" class="flex items-center justify-between text-sm text-gray-500">
      <span>{{ productData.total }} products total</span>
      <div class="flex gap-2">
        <button :disabled="filters.page <= 1" @click="filters.page--; fetchProducts()" class="btn-secondary text-xs px-3 py-1">Previous</button>
        <button :disabled="!productData.has_more" @click="filters.page++; fetchProducts()" class="btn-secondary text-xs px-3 py-1">Next</button>
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
