import { createResource } from "frappe-ui";

export function useStockSummary() {
  const stockResource = createResource({
    url: "supplier_portal.api.inventory.get_stock_summary",
    auto: true,
  });

  return { stock: stockResource };
}

export function useStockLevels() {
  const stockResource = createResource({
    url: "supplier_portal.api.inventory.get_stock_levels",
    auto: false,
  });

  return { stockLevels: stockResource };
}
