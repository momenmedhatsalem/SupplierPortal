<template>
  <div class="space-y-6 max-w-2xl animate-fade-in">
    <!-- Company Information -->
    <div class="card">
      <div class="flex items-center gap-2 mb-5">
        <div class="w-8 h-8 bg-brand-50 text-brand-600 rounded-lg flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        </div>
        <h3 class="font-semibold text-gray-900">Company Information</h3>
      </div>
      <div v-if="!supplier" class="space-y-3">
        <div class="skeleton h-10 w-full rounded-lg" />
        <div class="skeleton h-10 w-full rounded-lg" />
        <div class="skeleton h-10 w-full rounded-lg" />
      </div>
      <form v-else @submit.prevent="saveProfile" class="space-y-4">
        <div>
          <label class="label">Company Name</label>
          <input :value="supplier.supplier_name" type="text" disabled class="input-field bg-gray-50 text-gray-500 cursor-not-allowed" />
          <p class="text-xs text-gray-400 mt-1">Contact support to change your company name</p>
        </div>
        <div>
          <label class="label">Country</label>
          <input :value="supplier.country" type="text" disabled class="input-field bg-gray-50 text-gray-500 cursor-not-allowed" />
        </div>
        <div>
          <label class="label">Website</label>
          <input v-model="form.website" type="url" class="input-field" placeholder="https://your-website.com" />
        </div>
        <div>
          <label class="label">Business Description</label>
          <textarea v-model="form.custom_business_description" rows="3" class="input-field" placeholder="Describe your business..." />
        </div>
        <div>
          <label class="label">Product Categories</label>
          <input v-model="form.custom_product_categories" type="text" class="input-field" placeholder="e.g., Clothing, Shoes, Accessories" />
        </div>

        <div class="pt-4 border-t border-gray-100">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 bg-green-50 text-green-600 rounded-lg flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
            </div>
            <h3 class="font-semibold text-gray-900">Banking Information</h3>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="label">Bank Name</label>
              <input v-model="form.custom_bank_name" type="text" class="input-field" placeholder="Bank name" />
            </div>
            <div>
              <label class="label">IBAN</label>
              <input v-model="form.custom_bank_iban" type="text" class="input-field" placeholder="MA00 0000 0000 0000 0000 0000" />
            </div>
          </div>
        </div>

        <div class="flex items-center gap-3 pt-3">
          <button type="submit" :disabled="saving" class="btn-primary flex items-center gap-2">
            <svg v-if="saving" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/></svg>
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
          <transition name="fade">
            <span v-if="saved" class="text-sm text-green-600 font-medium flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              Saved!
            </span>
          </transition>
        </div>
      </form>
    </div>

    <!-- Contact info (read-only) -->
    <div v-if="supplier?.contact" class="card">
      <div class="flex items-center gap-2 mb-4">
        <div class="w-8 h-8 bg-blue-50 text-blue-600 rounded-lg flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </div>
        <h3 class="font-semibold text-gray-900">Contact Information</h3>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="bg-gray-50 rounded-xl p-3">
          <span class="text-xs text-gray-500 uppercase tracking-wide">Name</span>
          <div class="text-sm font-medium text-gray-900 mt-0.5">{{ supplier.contact.contact_name || '-' }}</div>
        </div>
        <div class="bg-gray-50 rounded-xl p-3">
          <span class="text-xs text-gray-500 uppercase tracking-wide">Email</span>
          <div class="text-sm font-medium text-gray-900 mt-0.5">{{ supplier.contact.email || '-' }}</div>
        </div>
        <div class="bg-gray-50 rounded-xl p-3">
          <span class="text-xs text-gray-500 uppercase tracking-wide">Phone</span>
          <div class="text-sm font-medium text-gray-900 mt-0.5">{{ supplier.contact.phone || '-' }}</div>
        </div>
      </div>
    </div>

    <!-- Security -->
    <div class="card">
      <div class="flex items-center gap-2 mb-4">
        <div class="w-8 h-8 bg-red-50 text-red-600 rounded-lg flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        </div>
        <h3 class="font-semibold text-gray-900">Security</h3>
      </div>
      <form @submit.prevent="changePassword" class="space-y-4 max-w-sm">
        <div>
          <label class="label">New Password</label>
          <input v-model="newPassword" type="password" minlength="8" required class="input-field" placeholder="At least 8 characters" />
        </div>
        <div>
          <label class="label">Confirm Password</label>
          <input v-model="confirmPassword" type="password" required class="input-field" placeholder="Repeat password" />
        </div>
        <transition name="fade">
          <div v-if="passwordError" class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg p-3 flex items-start gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/></svg>
            {{ passwordError }}
          </div>
        </transition>
        <transition name="fade">
          <div v-if="passwordSaved" class="bg-green-50 border border-green-200 text-green-700 text-sm rounded-lg p-3 flex items-start gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            Password updated successfully!
          </div>
        </transition>
        <button type="submit" :disabled="changingPassword" class="btn-primary flex items-center gap-2">
          <svg v-if="changingPassword" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/></svg>
          {{ changingPassword ? 'Updating...' : 'Change Password' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import { useAuth } from "@/composables/useAuth";
import { createResource } from "frappe-ui";

const { supplier, refreshSupplier } = useAuth();

const form = reactive({
  website: "",
  custom_business_description: "",
  custom_product_categories: "",
  custom_bank_name: "",
  custom_bank_iban: "",
});

const saving = ref(false);
const saved = ref(false);
const newPassword = ref("");
const confirmPassword = ref("");
const passwordError = ref("");
const passwordSaved = ref(false);
const changingPassword = ref(false);

// Load form from supplier data
watch(supplier, (s) => {
  if (s) {
    form.website = s.website || "";
    form.custom_business_description = s.business_description || "";
    form.custom_product_categories = s.product_categories || "";
    form.custom_bank_name = s.bank_name || "";
    form.custom_bank_iban = s.bank_iban || "";
  }
}, { immediate: true });

const updateResource = createResource({
  url: "supplier_portal.api.auth.update_supplier_profile",
  auto: false,
});

async function saveProfile() {
  saving.value = true;
  saved.value = false;
  try {
    await updateResource.fetch({ params: { data: JSON.stringify(form) } });
    await refreshSupplier();
    saved.value = true;
    setTimeout(() => (saved.value = false), 3000);
  } catch (e) {
    alert(e.message || "Failed to save");
  } finally {
    saving.value = false;
  }
}

async function changePassword() {
  passwordError.value = "";
  passwordSaved.value = false;

  if (newPassword.value !== confirmPassword.value) {
    passwordError.value = "Passwords do not match";
    return;
  }

  changingPassword.value = true;
  try {
    await fetch("/api/method/frappe.core.doctype.user.user.update_password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        new_password: newPassword.value,
      }),
    });
    passwordSaved.value = true;
    newPassword.value = "";
    confirmPassword.value = "";
    setTimeout(() => (passwordSaved.value = false), 5000);
  } catch (e) {
    passwordError.value = "Failed to update password";
  } finally {
    changingPassword.value = false;
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
