import { env } from "@/lib/env";

export type ChatwootConversation = {
  id: number;
  inboxId: number | null;
  contactName: string;
  lastMessage: string;
  status: "open" | "resolved" | "pending" | string;
  updatedAt: string;
};

type ChatwootApiConversation = {
  id: number;
  inbox_id?: number;
  status?: string;
  updated_at?: string;
  meta?: {
    sender?: {
      name?: string;
    };
  };
  messages?: Array<{
    content?: string;
  }>;
};

type ChatwootConversationResponse = {
  data?: {
    payload?: ChatwootApiConversation[];
  };
};

export class ChatwootClient {
  constructor(
    private readonly baseUrl = env.chatwootBaseUrl,
    private readonly accountId = env.chatwootAccountId,
    private readonly apiToken = env.chatwootApiToken,
  ) {}

  async listConversations(options: { inboxId?: number } = {}): Promise<ChatwootConversation[]> {
    if (!this.baseUrl || !this.accountId || !this.apiToken) {
      return [];
    }

    const response = await fetch(
      `${this.baseUrl}/api/v1/accounts/${this.accountId}/conversations`,
      {
        headers: {
          api_access_token: this.apiToken,
          "content-type": "application/json",
        },
        next: { revalidate: 30 },
      },
    );

    if (!response.ok) {
      throw new Error("chatwoot_conversations_failed");
    }

    const body = (await response.json()) as ChatwootConversationResponse;
    return (body.data?.payload ?? [])
      .filter((conversation) =>
        options.inboxId ? conversation.inbox_id === options.inboxId : true,
      )
      .map((conversation) => ({
        id: conversation.id,
        inboxId: conversation.inbox_id ?? null,
        contactName: conversation.meta?.sender?.name ?? "Cliente",
        lastMessage: conversation.messages?.at(-1)?.content ?? "Conversa sem mensagem recente",
        status: conversation.status ?? "open",
        updatedAt: conversation.updated_at ?? new Date().toISOString(),
      }));
  }
}

export const chatwoot = new ChatwootClient();
