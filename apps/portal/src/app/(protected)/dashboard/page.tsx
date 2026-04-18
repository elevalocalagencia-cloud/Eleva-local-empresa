import { EmptyState } from "@/components/portal/empty-state";
import { StatCard } from "@/components/portal/stat-card";
import { dashboardMetrics } from "@/lib/portal-data";

export default function DashboardPage() {
  const hasData = dashboardMetrics.conversations > 0;

  return (
    <div>
      <section className="mb-8">
        <p className="text-sm text-sky-100/70">Bem-vindo(a), Eleva Ops.</p>
        <h2 className="mt-2 max-w-4xl text-3xl font-semibold leading-tight text-white md:text-5xl">
          {hasData
            ? `Este mês: ${dashboardMetrics.conversations} conversas atendidas, ${dashboardMetrics.bookings} agendamentos gerados, ${dashboardMetrics.monthlyDelta}% a mais que mês passado.`
            : "Bem-vindo(a), Eleva Ops. Sua operação já está rodando. Abaixo, o resumo em tempo real."}
        </h2>
      </section>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Conversas atendidas"
          value={String(dashboardMetrics.conversations)}
          description="Mensagens que o seu atendente automático já respondeu"
        />
        <StatCard
          label="Agendamentos gerados"
          value={String(dashboardMetrics.bookings)}
          description="Reuniões marcadas pelos seus clientes sem intervenção humana"
          tone="green"
        />
        <StatCard
          label="Tempo médio de resposta"
          value={dashboardMetrics.responseTime}
          description="Quanto seu cliente esperou para ser atendido"
          tone="yellow"
        />
        <StatCard
          label="Taxa de conversão"
          value={`${dashboardMetrics.conversionRate}%`}
          description="De cada 10 que chegaram, quantos agendaram"
          tone="rose"
        />
      </div>

      <section className="defer-paint mt-8 glass rounded-[20px] p-6">
        <h3 className="text-lg font-medium text-white">Hoje</h3>
        <div className="mt-5">
          <EmptyState title="Ainda não recebemos mensagens hoje. Assim que chegar, aparece aqui. ☕" />
        </div>
      </section>
    </div>
  );
}
