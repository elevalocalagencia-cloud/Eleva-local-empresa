import Link from "next/link";

import { DEMO_EXIT_URL, DEMO_PORTAL_BANNER, isDemoTenant } from "@/lib/demo-data";
import type { PortalTenant } from "@/lib/portal-data";

export function Topbar({ tenant }: { tenant: PortalTenant }) {
  const demoMode = isDemoTenant(tenant.id);

  return (
    <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
      {demoMode ? (
        <div className="sticky top-4 z-20 flex w-full flex-wrap items-center justify-between gap-3 rounded-[8px] border border-amber-300/30 bg-amber-300/12 px-4 py-3 text-sm text-amber-50">
          <strong>{DEMO_PORTAL_BANNER} - dados fake e reset semanal</strong>
          <Link
            className="rounded-[8px] border border-amber-200/40 px-3 py-2 text-xs font-medium text-amber-50 transition hover:bg-amber-200/10"
            href={DEMO_EXIT_URL}
          >
            Sair do modo demo
          </Link>
        </div>
      ) : null}
      <div>
        <p className="text-sm text-white/48">Operacao em tempo real</p>
        <h1 className="mt-1 text-2xl font-semibold text-white">{tenant.name}</h1>
      </div>
      <div className="flex items-center gap-2 rounded-full border border-white/12 bg-white/7 px-4 py-2 text-sm text-white/70">
        <span className="size-2 rounded-full bg-green-300" />
        {tenant.subscriptionStatus}
      </div>
      <nav className="flex w-full gap-2 overflow-x-auto text-sm text-white/70 lg:hidden">
        <Link className="rounded-[8px] bg-white/8 px-3 py-2" href="/dashboard">
          Resumo
        </Link>
        <Link className="rounded-[8px] bg-white/8 px-3 py-2" href="/mensagens">
          Mensagens
        </Link>
        <Link className="rounded-[8px] bg-white/8 px-3 py-2" href="/agendamentos">
          Agendamentos
        </Link>
        <Link className="rounded-[8px] bg-white/8 px-3 py-2" href="/configuracoes">
          Configuracoes
        </Link>
      </nav>
    </header>
  );
}
