<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md animate-fade-in-up">
      <router-link to="/suppliers" class="flex items-center justify-center gap-2 group">
        <div class="w-10 h-10 bg-brand-600 rounded-lg flex items-center justify-center shadow-lg shadow-brand-600/20 group-hover:scale-105 transition-transform">
          <span class="text-white font-bold text-lg">J</span>
        </div>
      </router-link>
      <h2 class="mt-6 text-center text-2xl font-bold text-gray-900">
        Reset Password
      </h2>
      <p class="mt-1 text-center text-sm text-gray-500">
        Enter your email and we'll send you a reset link
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md animate-fade-in-up stagger-2">
      <div class="card sm:px-10">
        <div v-if="sent" class="text-center py-6 animate-scale-in">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="mt-4 text-lg font-semibold text-gray-900">Check Your Email</h3>
          <p class="mt-2 text-sm text-gray-500 max-w-sm mx-auto">
            If an account exists for {{ email }}, we've sent a password reset link.
          </p>
          <router-link to="/suppliers/login" class="btn-secondary mt-6 inline-block">
            Back to Login
          </router-link>
        </div>

        <form v-else @submit.prevent="handleReset" class="space-y-5">
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3 flex items-start gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0 mt-0.5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/></svg>
            <span>{{ error }}</span>
          </div>

          <div>
            <label for="email" class="label">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              class="input-field"
              placeholder="you@company.com"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="btn-primary w-full flex items-center justify-center gap-2 py-2.5"
          >
            <svg v-if="loading" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            {{ loading ? 'Sending...' : 'Send Reset Link' }}
          </button>
        </form>

        <div v-if="!sent" class="mt-6 text-center">
          <router-link to="/suppliers/login" class="text-sm text-brand-600 hover:text-brand-700 font-medium">
            Back to Login
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const email = ref("");
const loading = ref(false);
const error = ref("");
const sent = ref(false);

async function handleReset() {
  error.value = "";
  loading.value = true;

  try {
    const response = await fetch(
      "/api/method/frappe.core.doctype.user.user.reset_password",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user: email.value }),
      }
    );

    if (!response.ok) {
      throw new Error("Failed to send reset email");
    }

    sent.value = true;
  } catch (e) {
    // Always show success to prevent email enumeration
    sent.value = true;
  } finally {
    loading.value = false;
  }
}
</script>
