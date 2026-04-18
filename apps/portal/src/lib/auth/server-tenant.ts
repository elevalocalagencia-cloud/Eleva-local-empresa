import { forbiddenMessage } from "@/lib/auth/tenant-access";
import { createSupabaseServerClient } from "@/lib/supabase/server";

export type TenantAccess =
  | {
      allowed: true;
      tenantId: string;
      userId: string;
      userEmail: string | null;
      role: string;
    }
  | {
      allowed: false;
      message: string;
      status: 403;
    };

export async function resolveCurrentTenantAccess(): Promise<TenantAccess> {
  const supabase = await createSupabaseServerClient();

  if (!supabase) {
    return { allowed: false, message: forbiddenMessage, status: 403 };
  }

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return { allowed: false, message: forbiddenMessage, status: 403 };
  }

  const { data, error } = await supabase
    .from("tenant_members")
    .select("tenant_id, role")
    .eq("user_id", user.id)
    .order("created_at", { ascending: true })
    .limit(1)
    .maybeSingle();

  if (error || !data) {
    return { allowed: false, message: forbiddenMessage, status: 403 };
  }

  return {
    allowed: true,
    tenantId: data.tenant_id,
    userId: user.id,
    userEmail: user.email ?? null,
    role: data.role,
  };
}

export async function requireTenantAccess(tenantId: string): Promise<TenantAccess> {
  const access = await resolveCurrentTenantAccess();

  if (!access.allowed) {
    return access;
  }

  if (access.tenantId !== tenantId) {
    return { allowed: false, message: forbiddenMessage, status: 403 };
  }

  return access;
}
