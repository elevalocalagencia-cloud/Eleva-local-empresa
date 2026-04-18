import type { ChatwootConversation } from "@/lib/chatwoot";

export function ConversationRow({ conversation }: { conversation: ChatwootConversation }) {
  return (
    <article className="grid gap-3 border-b border-white/10 py-4 last:border-b-0 md:grid-cols-[1fr_auto]">
      <div>
        <p className="font-medium text-white">{conversation.contactName}</p>
        <p className="mt-1 max-w-3xl text-sm leading-6 text-white/58">{conversation.lastMessage}</p>
      </div>
      <div className="text-left text-sm text-white/45 md:text-right">
        <p>{conversation.status === "open" ? "Em atendimento" : "Resolvida"}</p>
        <p>{new Date(conversation.updatedAt).toLocaleDateString("pt-BR")}</p>
      </div>
    </article>
  );
}
