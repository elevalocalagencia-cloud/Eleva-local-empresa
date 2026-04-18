import { describe, expect, it } from "vitest";

import { canAccessTenant } from "@/lib/auth/tenant-access";

describe("tenant access", () => {
  it("allows a user to read rows for tenants where they are a member", () => {
    expect(
      canAccessTenant({
        userId: "user-a",
        tenantId: "tenant-a",
        memberships: [
          { tenantId: "tenant-a", userId: "user-a", role: "owner" },
          { tenantId: "tenant-b", userId: "user-b", role: "owner" },
        ],
      }),
    ).toBe(true);
  });

  it("blocks tenant B data for a user that only belongs to tenant A", () => {
    expect(
      canAccessTenant({
        userId: "user-a",
        tenantId: "tenant-b",
        memberships: [
          { tenantId: "tenant-a", userId: "user-a", role: "owner" },
          { tenantId: "tenant-b", userId: "user-b", role: "owner" },
        ],
      }),
    ).toBe(false);
  });
});
