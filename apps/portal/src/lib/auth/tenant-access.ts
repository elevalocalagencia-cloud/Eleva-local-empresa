export type TenantRole = "owner" | "ops" | "viewer";

export type TenantMembership = {
  tenantId: string;
  userId: string;
  role: TenantRole;
};

type CanAccessTenantInput = {
  userId: string | null;
  tenantId: string;
  memberships: readonly TenantMembership[];
};

export function canAccessTenant({
  userId,
  tenantId,
  memberships,
}: CanAccessTenantInput): boolean {
  if (!userId) {
    return false;
  }

  return memberships.some(
    (membership) => membership.userId === userId && membership.tenantId === tenantId,
  );
}

export const forbiddenMessage =
  "Parece que você não tem acesso a essa área. Se achar que é engano, fala com seu gerente de conta.";
