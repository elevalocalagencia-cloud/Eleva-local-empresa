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

export const pilotTenant: PortalTenant = {
  id: "cli-eleva-pilot",
  name: "Eleva Local Pilot",
  slug: "eleva-pilot",
  plan: "Interno",
  billingCycle: "Mensal",
  ownerEmail: "ops@elevalocal.shop",
  whatsappNumber: "+55 11 99999-9999",
  chatwootInboxName: "cli-eleva-pilot-inbox",
  evolutionInstance: "cli-eleva-pilot-evo",
  subscriptionStatus: "Ativa",
};

export const dashboardMetrics: DashboardMetrics = {
  conversations: 0,
  bookings: 0,
  responseTime: "0 min",
  conversionRate: 0,
  monthlyDelta: 0,
};

export const bookings: Booking[] = [];
