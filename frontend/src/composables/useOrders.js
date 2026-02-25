import { ref, watch } from "vue";
import { createResource } from "frappe-ui";

export function useOrders() {
  const filters = ref({
    status: "",
    from_date: "",
    to_date: "",
    search: "",
    page: 1,
  });

  const ordersResource = createResource({
    url: "supplier_portal.api.orders.get_orders",
    params: filters.value,
    auto: false,
  });

  function fetchOrders() {
    ordersResource.fetch({
      params: {
        status: filters.value.status || undefined,
        from_date: filters.value.from_date || undefined,
        to_date: filters.value.to_date || undefined,
        search: filters.value.search || undefined,
        page: filters.value.page,
      },
    });
  }

  return {
    orders: ordersResource,
    filters,
    fetchOrders,
  };
}

export function useOrderDetail(orderId) {
  const orderResource = createResource({
    url: "supplier_portal.api.orders.get_order_detail",
    params: { order_name: orderId },
    auto: true,
  });

  const updateStatusResource = createResource({
    url: "supplier_portal.api.orders.update_item_status",
    auto: false,
  });

  async function updateItemStatus(itemName, newStatus) {
    await updateStatusResource.fetch({
      params: {
        order_name: orderId,
        item_name: itemName,
        new_status: newStatus,
      },
    });
    // Refresh order detail
    orderResource.reload();
  }

  return {
    order: orderResource,
    updateItemStatus,
    updating: updateStatusResource.loading,
  };
}
