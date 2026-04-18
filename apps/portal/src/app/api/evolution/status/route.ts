import { NextResponse } from "next/server";

import { resolveCurrentTenantAccess } from "@/lib/auth/server-tenant";
import { evolution } from "@/lib/evolution";

export async function GET() {
  const access = await resolveCurrentTenantAccess();

  if (!access.allowed) {
    return NextResponse.json({ message: access.message }, { status: access.status });
  }

  try {
    return NextResponse.json({
      status: await evolution.getInstanceStatus(`${access.tenantId}-evo`),
    });
  } catch {
    return NextResponse.json(
      {
        message:
          "Tivemos um contratempo aqui do nosso lado. Ja fomos avisados e estamos resolvendo. Tenta de novo em 1 minuto?",
      },
      { status: 500 },
    );
  }
}
