<template>
  <div class="min-h-screen bg-white">
    <!-- Navbar -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-lg border-b border-gray-100">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center shadow-sm">
              <span class="text-white font-bold text-sm">J</span>
            </div>
            <span class="text-xl font-bold text-gray-900">Justyol</span>
            <span class="text-sm text-gray-400 ml-0.5 hidden sm:inline">Supplier Portal</span>
          </div>
          <div class="flex items-center gap-2 sm:gap-3">
            <router-link to="/suppliers/login" class="btn-ghost text-sm px-3 py-2 sm:px-4">
              Log In
            </router-link>
            <router-link to="/suppliers/register" class="btn-primary text-sm px-3 py-2 sm:px-5">
              Get Started
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="relative pt-32 pb-20 sm:pt-40 sm:pb-28 overflow-hidden">
      <!-- Background gradient -->
      <div class="absolute inset-0 bg-gradient-to-br from-brand-50 via-white to-purple-50" />
      <div class="absolute top-0 right-0 w-[600px] h-[600px] bg-brand-100 rounded-full blur-3xl opacity-30 -translate-y-1/2 translate-x-1/4" />
      <div class="absolute bottom-0 left-0 w-[400px] h-[400px] bg-purple-100 rounded-full blur-3xl opacity-30 translate-y-1/2 -translate-x-1/4" />

      <div class="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div class="animate-fade-in-up">
          <div class="inline-flex items-center gap-2 bg-brand-50 text-brand-700 text-sm font-medium px-4 py-1.5 rounded-full ring-1 ring-brand-100 mb-6">
            <span class="w-1.5 h-1.5 bg-brand-500 rounded-full animate-pulse" />
            Trusted by 300+ suppliers across Morocco & Turkey
          </div>
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight tracking-tight">
            Grow Your Business
            <br class="hidden sm:block" />
            with <span class="text-gradient">Justyol</span>
          </h1>
          <p class="mt-6 text-lg sm:text-xl text-gray-500 max-w-2xl mx-auto leading-relaxed">
            Join our marketplace and reach thousands of customers. Manage orders, track performance, and scale your business — all from one dashboard.
          </p>
          <div class="mt-10 flex flex-col sm:flex-row justify-center gap-3 sm:gap-4">
            <router-link to="/suppliers/register" class="btn-primary text-base px-8 py-3.5 shadow-lg shadow-brand-600/20 hover:shadow-xl hover:shadow-brand-600/30">
              Start Selling Today
              <svg xmlns="http://www.w3.org/2000/svg" class="inline w-5 h-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
            </router-link>
            <a href="#how-it-works" class="btn-secondary text-base px-8 py-3.5">
              How It Works
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats bar -->
    <section class="relative py-16 bg-white border-y border-gray-100">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-8 sm:gap-12">
          <div v-for="stat in stats" :key="stat.label" class="text-center animate-fade-in-up" :class="stat.stagger">
            <div class="text-4xl sm:text-5xl font-bold text-gray-900">
              {{ stat.value }}
            </div>
            <div class="text-sm text-gray-500 mt-2 font-medium">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section id="how-it-works" class="py-20 sm:py-28 bg-gray-50/50">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 tracking-tight">How It Works</h2>
          <p class="text-gray-500 mt-3 max-w-xl mx-auto text-lg">
            Start selling on Justyol in three simple steps
          </p>
        </div>
        <div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 lg:gap-12">
          <div v-for="(step, i) in steps" :key="i" class="relative text-center group">
            <!-- Connector line -->
            <div v-if="i < 2" class="hidden md:block absolute top-7 left-[60%] w-[80%] h-[2px] bg-gradient-to-r from-brand-200 to-brand-100" />
            <div class="relative z-10 w-14 h-14 bg-brand-600 text-white rounded-2xl flex items-center justify-center mx-auto text-xl font-bold shadow-lg shadow-brand-600/20 group-hover:scale-110 transition-transform duration-300">
              {{ i + 1 }}
            </div>
            <h3 class="mt-6 text-lg font-semibold text-gray-900">{{ step.title }}</h3>
            <p class="mt-2 text-sm text-gray-500 leading-relaxed max-w-xs mx-auto">
              {{ step.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-20 sm:py-28">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 tracking-tight">Your Supplier Dashboard</h2>
          <p class="text-gray-500 mt-3 max-w-xl mx-auto text-lg">
            Everything you need to manage and grow your business
          </p>
        </div>
        <div class="mt-16 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div
            v-for="(feature, i) in features"
            :key="i"
            class="group bg-white rounded-2xl border border-gray-200 p-6 hover:shadow-lg hover:border-gray-300 hover:-translate-y-1 transition-all duration-300"
          >
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-lg" :class="feature.iconBg">
              <div v-html="feature.icon" />
            </div>
            <h3 class="mt-5 font-semibold text-gray-900 group-hover:text-brand-700 transition-colors">{{ feature.title }}</h3>
            <p class="mt-2 text-sm text-gray-500 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-20 sm:py-28">
      <div class="max-w-4xl mx-auto px-4">
        <div class="relative bg-gradient-to-br from-brand-600 to-brand-800 rounded-3xl p-10 sm:p-16 text-center overflow-hidden">
          <!-- Decorative elements -->
          <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-2xl -translate-y-1/2 translate-x-1/4" />
          <div class="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full blur-2xl translate-y-1/3 -translate-x-1/4" />

          <div class="relative">
            <h2 class="text-3xl sm:text-4xl font-bold text-white tracking-tight">Ready to Get Started?</h2>
            <p class="text-brand-100 mt-4 text-lg max-w-lg mx-auto">
              Join our growing network of suppliers and start reaching customers across Morocco today.
            </p>
            <div class="mt-8 flex flex-col sm:flex-row justify-center gap-3">
              <router-link
                to="/suppliers/register"
                class="bg-white text-brand-700 font-semibold px-8 py-3.5 rounded-lg hover:bg-brand-50 active:scale-[0.98] transition-all duration-150 shadow-lg"
              >
                Register as a Supplier
              </router-link>
              <router-link
                to="/suppliers/login"
                class="text-white font-medium px-8 py-3.5 rounded-lg ring-1 ring-white/30 hover:bg-white/10 active:scale-[0.98] transition-all duration-150"
              >
                Already a partner? Sign In
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-gray-200 bg-gray-50/50">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-8">
          <div>
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center">
                <span class="text-white font-bold text-sm">J</span>
              </div>
              <span class="font-bold text-gray-900">Justyol</span>
            </div>
            <p class="text-sm text-gray-500 mt-3 leading-relaxed">
              Morocco's growing marketplace connecting suppliers with customers across the country.
            </p>
          </div>
          <div>
            <h4 class="text-sm font-semibold text-gray-900 mb-3">Portal</h4>
            <ul class="space-y-2 text-sm">
              <li><router-link to="/suppliers/login" class="text-gray-500 hover:text-brand-600 transition-colors">Supplier Login</router-link></li>
              <li><router-link to="/suppliers/register" class="text-gray-500 hover:text-brand-600 transition-colors">Register</router-link></li>
            </ul>
          </div>
          <div>
            <h4 class="text-sm font-semibold text-gray-900 mb-3">Support</h4>
            <ul class="space-y-2 text-sm">
              <li><a href="mailto:support@justyol.com" class="text-gray-500 hover:text-brand-600 transition-colors">support@justyol.com</a></li>
            </ul>
          </div>
        </div>
        <div class="mt-10 pt-6 border-t border-gray-200 text-center text-sm text-gray-400">
          &copy; {{ new Date().getFullYear() }} Justyol. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
const stats = [
  { value: "300+", label: "Active Suppliers", stagger: "stagger-1" },
  { value: "190K+", label: "Orders Processed", stagger: "stagger-2" },
  { value: "149K+", label: "Products Listed", stagger: "stagger-3" },
];

const steps = [
  {
    title: "Register",
    description: "Create your supplier account with your company details. Our team will review and approve your application quickly.",
  },
  {
    title: "List Products",
    description: "Add your products to our catalog. Set prices, upload images, and manage your inventory through the portal.",
  },
  {
    title: "Fulfill & Earn",
    description: "Receive orders, confirm and ship them. Track your performance, revenue, and ratings in real-time.",
  },
];

const features = [
  {
    title: "Performance Tracking",
    description: "Real-time KPIs, supplier ratings, and actionable recommendations to improve your business.",
    iconBg: "bg-green-50 text-green-600",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
  },
  {
    title: "Order Management",
    description: "View, confirm, and track all your orders. Update item statuses and manage fulfillment in one place.",
    iconBg: "bg-blue-50 text-blue-600",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
  },
  {
    title: "Product Catalog",
    description: "Manage your products, pricing, and stock levels. Browse variants and monitor inventory health.",
    iconBg: "bg-purple-50 text-purple-600",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',
  },
  {
    title: "Account Settings",
    description: "Update your profile, banking information, and documents. Manage security and contact details.",
    iconBg: "bg-amber-50 text-amber-600",
    icon: '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
  },
];
</script>
