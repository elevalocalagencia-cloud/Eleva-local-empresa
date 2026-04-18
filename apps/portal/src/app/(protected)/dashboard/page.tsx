import { EmptyState } from "@/components/portal/empty-state";
import { StatCard } from "@/components/portal/stat-card";
import { getDashboardMetrics, getPortalContext } from "@/lib/portal-data";

export default async function DashboardPage() {
  const context = await getPortalContext();

  if (!context) {
    return null;
  }

  const dashboardMetrics = await getDashboardMetrics(context.tenant.id);
  const hasData = dashboardMetrics.conversations > 0;

  return (
    <div>
      <section className="mb-8">
        <p className="text-sm text-sky-100/70">Tenant ativo: {context.tenant.id}</p>
        <h2 className="mt-2 max-w-4xl text-3xl font-semibold leading-tight text-white md:text-5xl">
          {hasData
            ? `Este mes: ${dashboardMetrics.conversations} conversas atendidas, ${dashboardMetrics.bookings} agendamentos gerados, ${dashboardMetrics.monthlyDelta}% a mais que no periodo anterior.`
            : `Bem-vindo(a) ao portal de ${context.tenant.name}. Assim que o tenant receber trafego real, o resumo aparece aqui sem depender de piloto hardcoded.`}
        </h2>
      </section>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Conversas atendidas"
          value={String(dashboardMetrics.conversations)}
          description="Mensagens que o seu atendente automatico ja respondeu"
        />
        <StatCard
          label="Agendamentos gerados"
          value={String(dashboardMetrics.bookings)}
          description="Reunioes marcadas pelos seus clientes sem intervencao humana"
          tone="green"
        />
        <StatCard
          label="Tempo medio de resposta"
          value={dashboardMetrics.responseTime}
          description="Quanto seu cliente esperou para ser atendido"
          tone="yellow"
        />
        <StatCard
          label="Taxa de conversao"
          value={`${dashboardMetrics.conversionRate}%`}
          description="De cada 10 que chegaram, quantos agendaram"
          tone="rose"
        />
      </div>

      <section className="defer-paint mt-8 glass rounded-[20px] p-6">
        <h3 className="text-lg font-medium text-white">Hoje</h3>
        <div className="mt-5">
          <EmptyState title="Ainda nao recebemos mensagens hoje. Assim que chegar, aparece aqui." />
        </div>
      </section>
    </div>
  );
}
