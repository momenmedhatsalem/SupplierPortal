import { ref, computed } from "vue";
import { createResource } from "frappe-ui";

const user = ref(null);
const supplier = ref(null);
const isLoading = ref(true);
const isInitialized = ref(false);

const isLoggedIn = computed(() => user.value && user.value !== "Guest");
const isGuest = computed(() => !isLoggedIn.value);

const userResource = createResource({
  url: "frappe.auth.get_logged_user",
  cache: "current_user",
});

const supplierResource = createResource({
  url: "supplier_portal.api.auth.get_current_supplier",
  cache: "current_supplier",
});

async function init() {
  if (isInitialized.value) return;
  isLoading.value = true;
  try {
    await userResource.fetch();
    user.value = userResource.data;

    if (isLoggedIn.value) {
      try {
        await supplierResource.fetch();
        supplier.value = supplierResource.data;
      } catch (e) {
        // User exists but isn't linked to a supplier
        supplier.value = null;
      }
    }
  } catch (e) {
    user.value = null;
    supplier.value = null;
  } finally {
    isLoading.value = false;
    isInitialized.value = true;
  }
}

async function login(email, password) {
  const response = await fetch("/api/method/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ usr: email, pwd: password }),
  });

  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.message || "Login failed");
  }

  // Re-fetch user and supplier data
  isInitialized.value = false;
  await init();

  return { success: true };
}

async function logout() {
  await fetch("/api/method/logout", { method: "POST" });
  user.value = null;
  supplier.value = null;
  isInitialized.value = false;
}

async function register(data) {
  const response = await fetch(
    "/api/method/supplier_portal.api.auth.register_supplier",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }
  );

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.exc_type ? result._server_messages
      ? JSON.parse(JSON.parse(result._server_messages)[0]).message
      : "Registration failed"
      : result.message || "Registration failed");
  }

  return result.message;
}

export function useAuth() {
  return {
    user,
    supplier,
    isLoggedIn,
    isGuest,
    isLoading,
    init,
    login,
    logout,
    register,
    refreshSupplier: async () => {
      await supplierResource.fetch();
      supplier.value = supplierResource.data;
    },
  };
}
