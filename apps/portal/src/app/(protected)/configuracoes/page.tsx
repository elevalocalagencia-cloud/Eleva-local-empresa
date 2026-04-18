import { MotionShell } from "@/components/portal/motion-shell";
import { evolution } from "@/lib/evolution";
import { getPortalContext } from "@/lib/portal-data";

export default async function SettingsPage() {
  const context = await getPortalContext();

  if (!context) {
    return null;
  }

  const { tenant } = context;
  const status = await evolution.getInstanceStatus(tenant.evolutionInstance);

  const rows = [
    ["Empresa", tenant.name],
    ["Tenant", tenant.id],
    ["Plano", tenant.plan],
    ["Assinatura", tenant.subscriptionStatus],
    ["Contato", tenant.ownerEmail],
    ["WhatsApp", tenant.whatsappNumber],
    ["Inbox", tenant.chatwootInboxName],
    ["Evolution", status?.connected ? "Conectado" : "Aguardando conexao"],
  ];

  return (
    <MotionShell>
      <section className="glass rounded-[20px] p-6">
        <h2 className="text-2xl font-semibold text-white">Configuracoes</h2>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-white/58">
          Dados principais da sua operacao. Configuracoes criticas ficam protegidas pelo time
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
