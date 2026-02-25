import { createResource } from "frappe-ui";

export function usePerformance(fromDate, toDate) {
  const performanceResource = createResource({
    url: "supplier_portal.api.performance.get_performance",
    params: {
      from_date: fromDate || undefined,
      to_date: toDate || undefined,
    },
    auto: true,
  });

  const trendsResource = createResource({
    url: "supplier_portal.api.performance.get_trends",
    params: {
      from_date: fromDate || undefined,
      to_date: toDate || undefined,
    },
    auto: true,
  });

  return {
    performance: performanceResource,
    trends: trendsResource,
  };
}
