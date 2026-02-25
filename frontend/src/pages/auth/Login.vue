<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md animate-fade-in-up">
      <router-link to="/suppliers" class="flex items-center justify-center gap-2 group">
        <div class="w-10 h-10 bg-brand-600 rounded-lg flex items-center justify-center shadow-lg shadow-brand-600/20 group-hover:scale-105 transition-transform">
          <span class="text-white font-bold text-lg">J</span>
        </div>
      </router-link>
      <h2 class="mt-6 text-center text-2xl font-bold text-gray-900">
        Welcome Back
      </h2>
      <p class="mt-1 text-center text-sm text-gray-500">
        Sign in to your supplier portal
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md animate-fade-in-up stagger-2">
      <div class="card sm:px-10">
        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Error alert -->
          <transition name="shake">
            <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3 flex items-start gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0 mt-0.5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/></svg>
              <span>{{ error }}</span>
            </div>
          </transition>

          <div>
            <label for="email" class="label">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              autocomplete="email"
              placeholder="you@company.com"
              class="input-field"
              :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': error }"
            />
          </div>

          <div>
            <div class="flex justify-between">
              <label for="password" class="label">Password</label>
              <router-link to="/suppliers/forgot-password" class="text-xs text-brand-600 hover:text-brand-700 font-medium">
                Forgot password?
              </router-link>
            </div>
            <div class="relative">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
                placeholder="Enter your password"
                class="input-field pr-10"
                :class="{ 'border-red-300 focus:ring-red-500 focus:border-red-500': error }"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                tabindex="-1"
              >
                <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              </button>
            </div>
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
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-500">
            Don't have an account?
            <router-link to="/suppliers/register" class="text-brand-600 font-medium hover:text-brand-700 ml-1">
              Register here
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuth } from "@/composables/useAuth";

const router = useRouter();
const route = useRoute();
const { login } = useAuth();

const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");
const showPassword = ref(false);

async function handleLogin() {
  error.value = "";
  loading.value = true;

  try {
    await login(email.value, password.value);
    const redirect = route.query.redirect || "/suppliers/dashboard";
    router.push(redirect);
  } catch (e) {
    error.value = e.message || "Invalid email or password. Please try again.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.shake-enter-active {
  animation: shakeX 0.5s ease;
}

@keyframes shakeX {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-8px); }
  40% { transform: translateX(8px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}
</style>
