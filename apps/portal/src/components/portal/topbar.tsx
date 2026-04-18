import Link from "next/link";

import { pilotTenant } from "@/lib/portal-data";

export function Topbar() {
  return (
    <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
      <div>
        <p className="text-sm text-white/48">Operação em tempo real</p>
        <h1 className="mt-1 text-2xl font-semibold text-white">{pilotTenant.name}</h1>
      </div>
      <div className="flex items-center gap-2 rounded-full border border-white/12 bg-white/7 px-4 py-2 text-sm text-white/70">
        <span className="size-2 rounded-full bg-green-300" />
        Assinatura ativa
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
          Configurações
        </Link>
      </nav>
    </header>
  );
}
