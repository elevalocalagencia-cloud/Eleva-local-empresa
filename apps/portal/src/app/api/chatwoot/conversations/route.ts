import { NextResponse } from "next/server";

import { chatwoot } from "@/lib/chatwoot";

export async function GET() {
  try {
    return NextResponse.json({ conversations: await chatwoot.listConversations() });
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
