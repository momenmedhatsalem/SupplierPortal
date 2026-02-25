<template>
  <div class="space-y-6 max-w-2xl">
    <div class="card">
      <h3 class="font-semibold text-gray-900 mb-4">Company Information</h3>
      <div v-if="!supplier" class="text-gray-400 text-sm">Loading...</div>
      <form v-else @submit.prevent="saveProfile" class="space-y-4">
        <div>
          <label class="label">Company Name</label>
          <input :value="supplier.supplier_name" type="text" disabled class="input-field bg-gray-50" />
          <p class="text-xs text-gray-400 mt-1">Contact support to change your company name</p>
        </div>
        <div>
          <label class="label">Country</label>
          <input :value="supplier.country" type="text" disabled class="input-field bg-gray-50" />
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

        <h3 class="font-semibold text-gray-900 pt-4">Banking Information</h3>
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

        <div class="flex items-center gap-3 pt-2">
          <button type="submit" :disabled="saving" class="btn-primary">
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
          <span v-if="saved" class="text-sm text-green-600">Saved!</span>
        </div>
      </form>
    </div>

    <!-- Contact info (read-only) -->
    <div v-if="supplier?.contact" class="card">
      <h3 class="font-semibold text-gray-900 mb-4">Contact Information</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
        <div>
          <span class="text-gray-500">Name:</span>
          <span class="ml-2 text-gray-900">{{ supplier.contact.contact_name || '-' }}</span>
        </div>
        <div>
          <span class="text-gray-500">Email:</span>
          <span class="ml-2 text-gray-900">{{ supplier.contact.email || '-' }}</span>
        </div>
        <div>
          <span class="text-gray-500">Phone:</span>
          <span class="ml-2 text-gray-900">{{ supplier.contact.phone || '-' }}</span>
        </div>
      </div>
    </div>

    <!-- Change password -->
    <div class="card">
      <h3 class="font-semibold text-gray-900 mb-4">Security</h3>
      <form @submit.prevent="changePassword" class="space-y-4 max-w-sm">
        <div>
          <label class="label">New Password</label>
          <input v-model="newPassword" type="password" minlength="8" required class="input-field" placeholder="At least 8 characters" />
        </div>
        <div>
          <label class="label">Confirm Password</label>
          <input v-model="confirmPassword" type="password" required class="input-field" placeholder="Repeat password" />
        </div>
        <div v-if="passwordError" class="text-sm text-red-600">{{ passwordError }}</div>
        <div v-if="passwordSaved" class="text-sm text-green-600">Password updated successfully!</div>
        <button type="submit" :disabled="changingPassword" class="btn-primary">
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
  } catch (e) {
    passwordError.value = "Failed to update password";
  } finally {
    changingPassword.value = false;
  }
}
</script>
