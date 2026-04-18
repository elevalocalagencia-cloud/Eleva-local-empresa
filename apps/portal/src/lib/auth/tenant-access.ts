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
  "Parece que voce nao tem acesso a essa area. Se achar que e engano, fala com seu gerente de conta.";
