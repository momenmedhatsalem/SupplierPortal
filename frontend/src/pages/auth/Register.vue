<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-lg">
      <router-link to="/suppliers" class="flex items-center justify-center gap-2">
        <div class="w-10 h-10 bg-brand-600 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-lg">J</span>
        </div>
      </router-link>
      <h2 class="mt-6 text-center text-2xl font-bold text-gray-900">
        Register as a Supplier
      </h2>
      <p class="mt-1 text-center text-sm text-gray-600">
        Step {{ step }} of 3
      </p>
      <!-- Progress bar -->
      <div class="mt-4 flex gap-2 max-w-xs mx-auto">
        <div v-for="s in 3" :key="s" class="h-1.5 flex-1 rounded-full" :class="s <= step ? 'bg-brand-600' : 'bg-gray-200'" />
      </div>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-lg">
      <div class="card sm:px-10">
        <!-- Success state -->
        <div v-if="success" class="text-center py-4">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 class="mt-4 text-lg font-semibold text-gray-900">Registration Submitted!</h3>
          <p class="mt-2 text-sm text-gray-600">
            Your account is pending approval. We'll notify you by email once it's activated.
          </p>
          <router-link to="/suppliers/login" class="btn-primary mt-6 inline-block">
            Go to Login
          </router-link>
        </div>

        <!-- Form -->
        <form v-else @submit.prevent="handleNext" class="space-y-5">
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3">
            {{ error }}
          </div>

          <!-- Step 1: Contact Info -->
          <template v-if="step === 1">
            <div>
              <label class="label">Full Name *</label>
              <input v-model="form.contact_name" type="text" required class="input-field" placeholder="Your full name" />
            </div>
            <div>
              <label class="label">Email *</label>
              <input v-model="form.email" type="email" required class="input-field" placeholder="you@company.com" />
            </div>
            <div>
              <label class="label">Password *</label>
              <input v-model="form.password" type="password" required minlength="8" class="input-field" placeholder="At least 8 characters" />
            </div>
            <div>
              <label class="label">Phone</label>
              <input v-model="form.phone" type="tel" class="input-field" placeholder="+212 600 000 000" />
            </div>
          </template>

          <!-- Step 2: Company Info -->
          <template v-if="step === 2">
            <div>
              <label class="label">Company Name *</label>
              <input v-model="form.company_name" type="text" required class="input-field" placeholder="Your company or brand name" />
            </div>
            <div>
              <label class="label">Country *</label>
              <select v-model="form.country" required class="input-field">
                <option value="">Select country</option>
                <option value="Morocco">Morocco</option>
                <option value="Turkey">Turkey</option>
                <option value="China">China</option>
                <option value="India">India</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div>
              <label class="label">Business Description</label>
              <textarea v-model="form.business_description" rows="3" class="input-field" placeholder="Tell us about your business..." />
            </div>
          </template>

          <!-- Step 3: Product Categories -->
          <template v-if="step === 3">
            <div>
              <label class="label">Product Categories</label>
              <p class="text-xs text-gray-500 mb-2">What types of products do you supply?</p>
              <div class="grid grid-cols-2 gap-2">
                <label
                  v-for="cat in categories"
                  :key="cat"
                  class="flex items-center gap-2 p-3 border rounded-lg cursor-pointer text-sm hover:bg-gray-50"
                  :class="selectedCategories.includes(cat) ? 'border-brand-500 bg-brand-50' : 'border-gray-200'"
                >
                  <input type="checkbox" :value="cat" v-model="selectedCategories" class="rounded" />
                  {{ cat }}
                </label>
              </div>
            </div>
            <div class="bg-gray-50 border border-gray-200 rounded-lg p-4 text-sm text-gray-600">
              By registering, you agree to Justyol's supplier terms and conditions.
              Your account will be reviewed by our team before activation.
            </div>
          </template>

          <!-- Navigation buttons -->
          <div class="flex gap-3">
            <button v-if="step > 1" type="button" @click="step--" class="btn-secondary flex-1">
              Back
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="btn-primary flex-1 flex items-center justify-center gap-2"
            >
              <svg v-if="loading" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              {{ step < 3 ? 'Continue' : loading ? 'Submitting...' : 'Register' }}
            </button>
          </div>
        </form>

        <div v-if="!success" class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Already have an account?
            <router-link to="/suppliers/login" class="text-brand-600 font-medium hover:text-brand-700">
              Sign in
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useAuth } from "@/composables/useAuth";

const { register } = useAuth();

const step = ref(1);
const loading = ref(false);
const error = ref("");
const success = ref(false);

const form = reactive({
  contact_name: "",
  email: "",
  password: "",
  phone: "",
  company_name: "",
  country: "",
  business_description: "",
});

const categories = [
  "Clothing",
  "Shoes",
  "Accessories",
  "Home & Living",
  "Baby & Kids",
  "Beauty",
  "Electronics",
  "Other",
];
const selectedCategories = ref([]);

async function handleNext() {
  error.value = "";

  if (step.value < 3) {
    step.value++;
    return;
  }

  // Final step — submit registration
  loading.value = true;
  try {
    await register({
      ...form,
      product_categories: selectedCategories.value.join(", "),
    });
    success.value = true;
  } catch (e) {
    error.value = e.message || "Registration failed. Please try again.";
  } finally {
    loading.value = false;
  }
}
</script>
