import { forbiddenMessage } from "@/lib/auth/tenant-access";
import { createSupabaseServerClient } from "@/lib/supabase/server";

export type TenantAccess =
  | {
      allowed: true;
      tenantId: string;
      userId: string;
    }
  | {
      allowed: false;
      message: string;
      status: 403;
    };

export async function requireTenantAccess(tenantId: string): Promise<TenantAccess> {
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
    .select("tenant_id")
    .eq("tenant_id", tenantId)
    .eq("user_id", user.id)
    .maybeSingle();

  if (error || !data) {
    return { allowed: false, message: forbiddenMessage, status: 403 };
  }

  return { allowed: true, tenantId, userId: user.id };
}
