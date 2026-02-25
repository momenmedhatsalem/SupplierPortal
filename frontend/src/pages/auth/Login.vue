<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <router-link to="/suppliers" class="flex items-center justify-center gap-2">
        <div class="w-10 h-10 bg-brand-600 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-lg">J</span>
        </div>
      </router-link>
      <h2 class="mt-6 text-center text-2xl font-bold text-gray-900">
        Supplier Portal
      </h2>
      <p class="mt-1 text-center text-sm text-gray-600">
        Sign in to manage your account
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="card sm:px-10">
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3">
            {{ error }}
          </div>

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
            />
          </div>

          <div>
            <div class="flex justify-between">
              <label for="password" class="label">Password</label>
              <router-link to="/suppliers/forgot-password" class="text-xs text-brand-600 hover:text-brand-700">
                Forgot password?
              </router-link>
            </div>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              autocomplete="current-password"
              placeholder="Enter your password"
              class="input-field"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="btn-primary w-full flex items-center justify-center gap-2"
          >
            <svg v-if="loading" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Don't have an account?
            <router-link to="/suppliers/register" class="text-brand-600 font-medium hover:text-brand-700">
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
