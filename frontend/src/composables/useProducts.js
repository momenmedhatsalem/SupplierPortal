import { ref } from "vue";
import { createResource } from "frappe-ui";

export function useProducts() {
  const filters = ref({ search: "", page: 1 });

  const productsResource = createResource({
    url: "supplier_portal.api.products.get_products",
    params: filters.value,
    auto: false,
  });

  function fetchProducts() {
    productsResource.fetch({
      params: {
        search: filters.value.search || undefined,
        page: filters.value.page,
      },
    });
  }

  return { products: productsResource, filters, fetchProducts };
}

export function useProductDetail(itemCode) {
  const productResource = createResource({
    url: "supplier_portal.api.products.get_product_detail",
    params: { item_code: itemCode },
    auto: true,
  });

  return { product: productResource };
}
