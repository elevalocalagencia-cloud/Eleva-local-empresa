import { NextResponse } from "next/server";

import { requireTenantAccess } from "@/lib/auth/server-tenant";
import { evolution } from "@/lib/evolution";
import { pilotTenant } from "@/lib/portal-data";

export async function GET() {
  const access = await requireTenantAccess(pilotTenant.id);

  if (!access.allowed) {
    return NextResponse.json({ message: access.message }, { status: access.status });
  }

  try {
    return NextResponse.json({
      status: await evolution.getInstanceStatus(pilotTenant.evolutionInstance),
    });
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
