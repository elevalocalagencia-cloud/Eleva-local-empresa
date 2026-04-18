import Link from "next/link";
import { BarChart3, CalendarDays, MessageCircle, Settings, Sparkles } from "lucide-react";

const items = [
  { href: "/dashboard", label: "Resumo", icon: BarChart3 },
  { href: "/mensagens", label: "Mensagens", icon: MessageCircle },
  { href: "/agendamentos", label: "Agendamentos", icon: CalendarDays },
  { href: "/configuracoes", label: "Configurações", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="glass sticky top-6 hidden h-[calc(100svh-48px)] rounded-[20px] p-5 lg:block">
      <Link href="/dashboard" className="flex items-center gap-3">
        <span className="grid size-10 place-items-center rounded-[8px] bg-sky-200 text-slate-950">
          <Sparkles size={18} />
        </span>
        <span>
          <strong className="block text-sm text-white">Eleva Local</strong>
          <span className="text-xs text-white/48">Portal do cliente</span>
        </span>
      </Link>
      <nav className="mt-10 grid gap-2">
        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="flex items-center gap-3 rounded-[8px] px-3 py-3 text-sm text-white/68 transition hover:bg-white/10 hover:text-white"
          >
            <item.icon size={17} />
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
