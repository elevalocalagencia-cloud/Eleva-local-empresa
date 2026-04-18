import { NextResponse, type NextRequest } from "next/server";

import { evolution } from "@/lib/evolution";

export async function GET(request: NextRequest) {
  const instance = request.nextUrl.searchParams.get("instance");

  if (!instance) {
    return NextResponse.json({ message: "Essa página não existe. Talvez tenha sido movida — volta pro início?" }, { status: 404 });
  }

  try {
    return NextResponse.json({ status: await evolution.getInstanceStatus(instance) });
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
