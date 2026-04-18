import { afterEach, beforeEach, describe, expect, it } from "vitest";

import {
  applyDemoTenantOverrides,
  getDemoBookings,
  getDemoConversations,
  getDemoDashboardMetrics,
  isDemoTenant,
} from "@/lib/demo-data";

describe("demo data", () => {
  const previousDemoTenantId = process.env.NEXT_PUBLIC_DEMO_TENANT_ID;

  beforeEach(() => {
    process.env.NEXT_PUBLIC_DEMO_TENANT_ID = "cli-demo-externo";
  });

  afterEach(() => {
    if (previousDemoTenantId === undefined) {
      delete process.env.NEXT_PUBLIC_DEMO_TENANT_ID;
      return;
    }

    process.env.NEXT_PUBLIC_DEMO_TENANT_ID = previousDemoTenantId;
  });

  it("recognizes only the configured demo tenant", () => {
    expect(isDemoTenant("cli-demo-externo", "cli-demo-externo")).toBe(true);
    expect(isDemoTenant("cli-eleva-pilot", "cli-demo-externo")).toBe(false);
  });

  it("applies demo overrides without touching other tenants", () => {
    const original = {
      id: "cli-demo-externo",
      name: "Original",
      slug: "demo-externo",
      plan: "Plano",
      billingCycle: "Mensal",
      ownerEmail: "owner@cliente.com",
      whatsappNumber: "+5511999999999",
      chatwootInboxName: "inbox",
      evolutionInstance: "evo",
      subscriptionStatus: "Pendente" as const,
    };

    expect(applyDemoTenantOverrides(original).name).toBe("Eleva Local Demo");
    expect(applyDemoTenantOverrides({ ...original, id: "cli-real-1" }).name).toBe("Original");
  });

  it("returns only fake data in demo helpers", () => {
    expect(getDemoDashboardMetrics().conversations).toBeGreaterThan(0);
    expect(getDemoBookings().every((item) => item.id.startsWith("demo-"))).toBe(true);
    expect(getDemoConversations().every((item) => item.id >= 1000)).toBe(true);
  });
});
