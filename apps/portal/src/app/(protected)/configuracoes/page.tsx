import { MotionShell } from "@/components/portal/motion-shell";
import { evolution } from "@/lib/evolution";
import { pilotTenant } from "@/lib/portal-data";

export default async function SettingsPage() {
  const status = await evolution.getInstanceStatus(pilotTenant.evolutionInstance);

  const rows = [
    ["Empresa", pilotTenant.name],
    ["Tenant", pilotTenant.id],
    ["Plano", pilotTenant.plan],
    ["Assinatura", pilotTenant.subscriptionStatus],
    ["Contato", pilotTenant.ownerEmail],
    ["WhatsApp", pilotTenant.whatsappNumber],
    ["Inbox", pilotTenant.chatwootInboxName],
    ["Evolution", status?.connected ? "Conectado" : "Aguardando conexão"],
  ];

  return (
    <MotionShell>
      <section className="glass rounded-[20px] p-6">
        <h2 className="text-2xl font-semibold text-white">Configurações</h2>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-white/58">
          Dados principais da sua operação. Configurações críticas ficam protegidas pelo time
          Eleva Local.
        </p>
        <div className="mt-8 divide-y divide-white/10">
          {rows.map(([label, value]) => (
            <div key={label} className="grid gap-1 py-4 md:grid-cols-[180px_1fr]">
              <p className="text-sm text-white/45">{label}</p>
              <p className="text-sm font-medium text-white">{value}</p>
            </div>
          ))}
        </div>
      </section>
    </MotionShell>
  );
}
