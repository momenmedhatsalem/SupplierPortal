<template>
  <div class="min-h-screen bg-white">
    <!-- Navbar -->
    <nav class="border-b border-gray-100">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-sm">J</span>
            </div>
            <span class="text-xl font-bold text-gray-900">Justyol</span>
            <span class="text-sm text-gray-500 ml-1">Supplier Portal</span>
          </div>
          <div class="flex items-center gap-3">
            <router-link to="/suppliers/login" class="btn-secondary text-sm">
              Log In
            </router-link>
            <router-link to="/suppliers/register" class="btn-primary text-sm">
              Become a Supplier
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="py-20 sm:py-28">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-4xl sm:text-5xl font-bold text-gray-900 leading-tight">
          Grow Your Business with
          <span class="text-brand-600">Justyol</span>
        </h1>
        <p class="mt-6 text-lg text-gray-600 max-w-2xl mx-auto">
          Join our marketplace and reach thousands of customers across Morocco.
          Manage your orders, track performance, and scale your business — all from one dashboard.
        </p>
        <div class="mt-10 flex justify-center gap-4">
          <router-link to="/suppliers/register" class="btn-primary text-base px-8 py-3">
            Get Started
          </router-link>
          <a href="#how-it-works" class="btn-secondary text-base px-8 py-3">
            How It Works
          </a>
        </div>
      </div>
    </section>

    <!-- Stats bar -->
    <section class="bg-gray-50 border-y border-gray-200 py-12">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-3 gap-8 text-center">
          <div>
            <div class="text-3xl font-bold text-brand-600">300+</div>
            <div class="text-sm text-gray-600 mt-1">Active Suppliers</div>
          </div>
          <div>
            <div class="text-3xl font-bold text-brand-600">190K+</div>
            <div class="text-sm text-gray-600 mt-1">Orders Processed</div>
          </div>
          <div>
            <div class="text-3xl font-bold text-brand-600">149K+</div>
            <div class="text-sm text-gray-600 mt-1">Products Listed</div>
          </div>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section id="how-it-works" class="py-20">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-gray-900 text-center">How It Works</h2>
        <p class="text-gray-600 text-center mt-3 max-w-xl mx-auto">
          Start selling on Justyol in three simple steps
        </p>
        <div class="mt-14 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="w-14 h-14 bg-brand-100 text-brand-700 rounded-2xl flex items-center justify-center mx-auto text-xl font-bold">
              1
            </div>
            <h3 class="mt-5 text-lg font-semibold text-gray-900">Register</h3>
            <p class="mt-2 text-sm text-gray-600">
              Create your supplier account with your company details. Our team will review and approve your application.
            </p>
          </div>
          <div class="text-center">
            <div class="w-14 h-14 bg-brand-100 text-brand-700 rounded-2xl flex items-center justify-center mx-auto text-xl font-bold">
              2
            </div>
            <h3 class="mt-5 text-lg font-semibold text-gray-900">List Products</h3>
            <p class="mt-2 text-sm text-gray-600">
              Add your products to our catalog. Set prices, upload images, and manage your inventory through the portal.
            </p>
          </div>
          <div class="text-center">
            <div class="w-14 h-14 bg-brand-100 text-brand-700 rounded-2xl flex items-center justify-center mx-auto text-xl font-bold">
              3
            </div>
            <h3 class="mt-5 text-lg font-semibold text-gray-900">Fulfill & Earn</h3>
            <p class="mt-2 text-sm text-gray-600">
              Receive orders, confirm and ship them. Track your performance, revenue, and ratings in real-time.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="bg-gray-50 py-20">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-gray-900 text-center">Your Supplier Dashboard</h2>
        <p class="text-gray-600 text-center mt-3 max-w-xl mx-auto">
          Everything you need to manage and grow your business
        </p>
        <div class="mt-14 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="card">
            <div class="w-10 h-10 bg-green-100 text-green-700 rounded-lg flex items-center justify-center text-lg">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            </div>
            <h3 class="mt-4 font-semibold text-gray-900">Performance Tracking</h3>
            <p class="mt-1 text-sm text-gray-600">Real-time KPIs, ratings, and AI-powered recommendations</p>
          </div>
          <div class="card">
            <div class="w-10 h-10 bg-blue-100 text-blue-700 rounded-lg flex items-center justify-center text-lg">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
            </div>
            <h3 class="mt-4 font-semibold text-gray-900">Order Management</h3>
            <p class="mt-1 text-sm text-gray-600">View, confirm, and track all your orders in one place</p>
          </div>
          <div class="card">
            <div class="w-10 h-10 bg-purple-100 text-purple-700 rounded-lg flex items-center justify-center text-lg">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
            </div>
            <h3 class="mt-4 font-semibold text-gray-900">Product Catalog</h3>
            <p class="mt-1 text-sm text-gray-600">Manage your products, pricing, and stock levels</p>
          </div>
          <div class="card">
            <div class="w-10 h-10 bg-amber-100 text-amber-700 rounded-lg flex items-center justify-center text-lg">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <h3 class="mt-4 font-semibold text-gray-900">Account Settings</h3>
            <p class="mt-1 text-sm text-gray-600">Update your profile, banking info, and documents</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-20">
      <div class="max-w-3xl mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold text-gray-900">Ready to Get Started?</h2>
        <p class="text-gray-600 mt-3">
          Join our network of suppliers and start growing your business today.
        </p>
        <router-link to="/suppliers/register" class="btn-primary text-base px-8 py-3 mt-8 inline-block">
          Register as a Supplier
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-gray-200 py-8">
      <div class="max-w-6xl mx-auto px-4 text-center text-sm text-gray-500">
        &copy; {{ new Date().getFullYear() }} Justyol. All rights reserved.
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>
