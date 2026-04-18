import type { ChatwootConversation } from "@/lib/chatwoot";
import type { Booking, DashboardMetrics, PortalTenant } from "@/lib/portal-data";

export const DEMO_EXIT_URL = "https://elevalocal.shop";
export const DEMO_PORTAL_BANNER = "MODO DEMO";
export const DEMO_UI_BANNER = "AMBIENTE DEMO - DADOS NAO PRESERVADOS";

export function isDemoTenant(
  tenantId: string,
  demoTenantId = process.env.NEXT_PUBLIC_DEMO_TENANT_ID,
): boolean {
  return Boolean(demoTenantId) && tenantId === demoTenantId;
}

export function applyDemoTenantOverrides(tenant: PortalTenant): PortalTenant {
  if (!isDemoTenant(tenant.id)) {
    return tenant;
  }

  return {
    ...tenant,
    name: "Eleva Local Demo",
    plan: "Demo publica",
    billingCycle: "Reset semanal",
    ownerEmail: "demo@elevalocal.shop",
    whatsappNumber: "Integracao real so no onboarding",
    chatwootInboxName: "Nao conectado na demo",
    evolutionInstance: "Nao conectado na demo",
    subscriptionStatus: "Ativa",
  };
}

export function getDemoDashboardMetrics(): DashboardMetrics {
  return {
    conversations: 42,
    bookings: 11,
    responseTime: "2 min",
    conversionRate: 27,
    monthlyDelta: 18,
  };
}

export function getDemoBookings(): Booking[] {
  return [
    {
      id: "demo-booking-1",
      customerName: "Ana Prospect",
      date: "22/04/2026 14:00",
      source: "Formulario demo",
      status: "Confirmado",
    },
    {
      id: "demo-booking-2",
      customerName: "Bruno Lead",
      date: "23/04/2026 10:30",
      source: "Webhook agendamento",
      status: "Pendente",
    },
  ];
}

export function getDemoConversations(): ChatwootConversation[] {
  return [
    {
      id: 1001,
      inboxId: null,
      contactName: "Carla Interessada",
      lastMessage: "Quero ver como o fluxo responde fora do horario comercial.",
      status: "open",
      updatedAt: "2026-04-18T12:00:00.000Z",
    },
    {
      id: 1002,
      inboxId: null,
      contactName: "Diego Prospect",
      lastMessage: "Me mostra um exemplo de follow-up automatico para lead frio.",
      status: "pending",
      updatedAt: "2026-04-18T15:30:00.000Z",
    },
  ];
}
