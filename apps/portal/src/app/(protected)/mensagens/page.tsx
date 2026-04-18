import { ConversationRow } from "@/components/portal/conversation-row";
import { EmptyState } from "@/components/portal/empty-state";
import { MotionShell } from "@/components/portal/motion-shell";
import { chatwoot } from "@/lib/chatwoot";
import { getDemoConversations, isDemoTenant } from "@/lib/demo-data";
import { getPortalContext } from "@/lib/portal-data";

export default async function MessagesPage() {
  const context = await getPortalContext();

  if (!context) {
    return null;
  }

  const conversations = isDemoTenant(context.tenant.id)
    ? getDemoConversations()
    : await chatwoot.listConversations();

  return (
    <MotionShell>
      <section className="glass rounded-[20px] p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold text-white">Mensagens</h2>
          <p className="mt-2 text-sm text-white/58">
            {isDemoTenant(context.tenant.id)
              ? "Conversas fake para demonstrar o portal sem encostar em dado real."
              : "Conversas recebidas pelo WhatsApp do seu atendimento."}
          </p>
        </div>
        {conversations.length > 0 ? (
          conversations.map((conversation) => (
            <ConversationRow key={conversation.id} conversation={conversation} />
          ))
        ) : (
          <EmptyState title="Nenhuma conversa por aqui ainda. Quando seu WhatsApp receber uma mensagem, ela aparece imediatamente." />
        )}
      </section>
    </MotionShell>
  );
}
