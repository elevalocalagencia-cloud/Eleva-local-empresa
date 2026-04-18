import { NextResponse } from "next/server";

import { requireTenantAccess } from "@/lib/auth/server-tenant";
import { chatwoot } from "@/lib/chatwoot";
import { env } from "@/lib/env";
import { pilotTenant } from "@/lib/portal-data";

export async function GET() {
  const access = await requireTenantAccess(pilotTenant.id);

  if (!access.allowed) {
    return NextResponse.json({ message: access.message }, { status: access.status });
  }

  const inboxId = env.chatwootInboxId ? Number(env.chatwootInboxId) : null;

  if (!inboxId || Number.isNaN(inboxId)) {
    return NextResponse.json({ conversations: [] });
  }

  try {
    return NextResponse.json({ conversations: await chatwoot.listConversations({ inboxId }) });
  } catch {
    return NextResponse.json(
      {
        message:
          "Tivemos um contratempo aqui do nosso lado. Já fomos avisados e estamos resolvendo. Tenta de novo em 1 minuto?",
      },
      { status: 500 },
    );
  }
}
