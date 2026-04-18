import "server-only";

import { createSupabaseServerClient } from "@/lib/supabase/server";
import { resolveCurrentTenantAccess } from "@/lib/auth/server-tenant";

export type PortalTenant = {
  id: string;
  name: string;
  slug: string;
  plan: string;
  billingCycle: string;
  ownerEmail: string;
  whatsappNumber: string;
  chatwootInboxName: string;
  evolutionInstance: string;
  subscriptionStatus: "Ativa" | "Pendente" | "Pausada";
};

export type DashboardMetrics = {
  conversations: number;
  bookings: number;
  responseTime: string;
  conversionRate: number;
  monthlyDelta: number;
};

export type Booking = {
  id: string;
  customerName: string;
  date: string;
  source: string;
  status: "Confirmado" | "Pendente" | "Reagendar";
};

export type PortalContext = {
  tenant: PortalTenant;
  userEmail: string | null;
  userId: string;
};

const emptyMetrics: DashboardMetrics = {
  conversations: 0,
  bookings: 0,
  responseTime: "-",
  conversionRate: 0,
  monthlyDelta: 0,
};

const bookingDateFormatter = new Intl.DateTimeFormat("pt-BR", {
  dateStyle: "short",
  timeStyle: "short",
});

function humanizeTenantName(tenantId: string): string {
  return tenantId
    .replace(/^cli-/, "")
    .split("-")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function tenantIdToSlug(tenantId: string): string {
  return tenantId.replace(/^cli-/, "");
}

export function buildPortalTenant(tenantId: string, userEmail?: string | null): PortalTenant {
  const slug = tenantIdToSlug(tenantId);

  return {
    id: tenantId,
    name: humanizeTenantName(tenantId),
    slug,
    plan: "A confirmar no contrato",
    billingCycle: "A confirmar",
    ownerEmail: userEmail ?? "owner@cliente.com",
    whatsappNumber: "Aguardando numero dedicado",
    chatwootInboxName: `${tenantId}-inbox`,
    evolutionInstance: `${tenantId}-evo`,
    subscriptionStatus: "Pendente",
  };
}

export async function getPortalContext(): Promise<PortalContext | null> {
  const access = await resolveCurrentTenantAccess();

  if (!access.allowed) {
    return null;
  }

  return {
    tenant: buildPortalTenant(access.tenantId, access.userEmail),
    userEmail: access.userEmail,
    userId: access.userId,
  };
}

export async function getDashboardMetrics(tenantId: string): Promise<DashboardMetrics> {
  const supabase = await createSupabaseServerClient();

  if (!supabase) {
    return emptyMetrics;
  }

  const [{ count: conversations }, { count: bookings }] = await Promise.all([
    supabase
      .from("portal_conversation_snapshots")
      .select("id", { head: true, count: "exact" })
      .eq("tenant_id", tenantId),
    supabase
      .from("portal_bookings")
      .select("id", { head: true, count: "exact" })
      .eq("tenant_id", tenantId),
  ]);

  return {
    conversations: conversations ?? 0,
    bookings: bookings ?? 0,
    responseTime: "-",
    conversionRate: 0,
    monthlyDelta: 0,
  };
}

export async function getBookings(tenantId: string): Promise<Booking[]> {
  const supabase = await createSupabaseServerClient();

  if (!supabase) {
    return [];
  }

  const { data } = await supabase
    .from("portal_bookings")
    .select("id, customer_name, starts_at, source, status")
    .eq("tenant_id", tenantId)
    .order("starts_at", { ascending: true })
    .limit(12);

  return (data ?? []).map((booking) => ({
    id: booking.id,
    customerName: booking.customer_name,
    date: bookingDateFormatter.format(new Date(booking.starts_at)),
    source: booking.source,
    status: booking.status,
  }));
}
