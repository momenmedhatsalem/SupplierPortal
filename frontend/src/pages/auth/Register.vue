<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-lg animate-fade-in-up">
      <router-link to="/suppliers" class="flex items-center justify-center gap-2 group">
        <div class="w-10 h-10 bg-brand-600 rounded-lg flex items-center justify-center shadow-lg shadow-brand-600/20 group-hover:scale-105 transition-transform">
          <span class="text-white font-bold text-lg">J</span>
        </div>
      </router-link>
      <h2 class="mt-6 text-center text-2xl font-bold text-gray-900">
        Register as a Supplier
      </h2>
      <p class="mt-1 text-center text-sm text-gray-500">
        Step {{ step }} of 3
      </p>
      <!-- Progress bar -->
      <div class="mt-4 flex gap-2 max-w-xs mx-auto">
        <div
          v-for="s in 3"
          :key="s"
          class="h-1.5 flex-1 rounded-full transition-all duration-500"
          :class="s <= step ? 'bg-brand-600' : 'bg-gray-200'"
        />
      </div>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-lg animate-fade-in-up stagger-2">
      <div class="card sm:px-10">
        <!-- Success state -->
        <div v-if="success" class="text-center py-6 animate-scale-in">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 class="mt-4 text-lg font-semibold text-gray-900">Registration Submitted!</h3>
          <p class="mt-2 text-sm text-gray-500 max-w-sm mx-auto">
            Your account is pending approval. We'll notify you by email once it's activated.
          </p>
          <router-link to="/suppliers/login" class="btn-primary mt-6 inline-block">
            Go to Login
          </router-link>
        </div>

        <!-- Form -->
        <form v-else @submit.prevent="handleNext" class="space-y-5">
          <transition name="shake">
            <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3 flex items-start gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0 mt-0.5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/></svg>
              <span>{{ error }}</span>
            </div>
          </transition>

          <!-- Step 1: Contact Info -->
          <transition name="step" mode="out-in">
            <div v-if="step === 1" key="step1" class="space-y-5">
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
                <div class="relative">
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    minlength="8"
                    class="input-field pr-10"
                    placeholder="At least 8 characters"
                  />
                  <button
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                    tabindex="-1"
                  >
                    <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                  </button>
                </div>
                <!-- Password strength indicator -->
                <div v-if="form.password" class="mt-2 flex items-center gap-2">
                  <div class="flex-1 flex gap-1">
                    <div v-for="i in 4" :key="i" class="h-1 flex-1 rounded-full transition-colors" :class="i <= passwordStrength ? strengthColors[passwordStrength] : 'bg-gray-200'" />
                  </div>
                  <span class="text-xs" :class="strengthTextColors[passwordStrength]">{{ strengthLabels[passwordStrength] }}</span>
                </div>
              </div>
              <div>
                <label class="label">Phone</label>
                <input v-model="form.phone" type="tel" class="input-field" placeholder="+212 600 000 000" />
              </div>
            </div>

            <!-- Step 2: Company Info -->
            <div v-else-if="step === 2" key="step2" class="space-y-5">
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
            </div>

            <!-- Step 3: Product Categories -->
            <div v-else-if="step === 3" key="step3" class="space-y-5">
              <div>
                <label class="label">Product Categories</label>
                <p class="text-xs text-gray-500 mb-3">What types of products do you supply?</p>
                <div class="grid grid-cols-2 gap-2">
                  <label
                    v-for="cat in categories"
                    :key="cat"
                    class="flex items-center gap-2.5 p-3 border rounded-xl cursor-pointer text-sm transition-all duration-150 hover:bg-gray-50"
                    :class="selectedCategories.includes(cat) ? 'border-brand-500 bg-brand-50 ring-1 ring-brand-200' : 'border-gray-200'"
                  >
                    <input type="checkbox" :value="cat" v-model="selectedCategories" class="rounded text-brand-600 focus:ring-brand-500" />
                    {{ cat }}
                  </label>
                </div>
              </div>
              <div class="bg-gray-50 border border-gray-200 rounded-xl p-4 text-sm text-gray-500">
                <div class="flex items-start gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4m0-4h.01"/></svg>
                  <span>By registering, you agree to Justyol's supplier terms and conditions. Your account will be reviewed by our team before activation.</span>
                </div>
              </div>
            </div>
          </transition>

          <!-- Navigation buttons -->
          <div class="flex gap-3 pt-1">
            <button v-if="step > 1" type="button" @click="step--" class="btn-secondary flex-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="inline w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
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
              <svg v-if="step < 3" xmlns="http://www.w3.org/2000/svg" class="inline w-4 h-4 ml-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </form>

        <div v-if="!success" class="mt-6 text-center">
          <p class="text-sm text-gray-500">
            Already have an account?
            <router-link to="/suppliers/login" class="text-brand-600 font-medium hover:text-brand-700 ml-1">
              Sign in
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
import { useAuth } from "@/composables/useAuth";

const { register } = useAuth();

const step = ref(1);
const loading = ref(false);
const error = ref("");
const success = ref(false);
const showPassword = ref(false);

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

// Password strength
const passwordStrength = computed(() => {
  const p = form.password;
  if (!p) return 0;
  let score = 0;
  if (p.length >= 8) score++;
  if (/[A-Z]/.test(p)) score++;
  if (/[0-9]/.test(p)) score++;
  if (/[^A-Za-z0-9]/.test(p)) score++;
  return score;
});

const strengthLabels = { 0: "", 1: "Weak", 2: "Fair", 3: "Good", 4: "Strong" };
const strengthColors = { 1: "bg-red-400", 2: "bg-yellow-400", 3: "bg-blue-400", 4: "bg-green-400" };
const strengthTextColors = { 1: "text-red-500", 2: "text-yellow-600", 3: "text-blue-600", 4: "text-green-600" };

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

.step-enter-active, .step-leave-active {
  transition: all 0.25s ease;
}
.step-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.step-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
