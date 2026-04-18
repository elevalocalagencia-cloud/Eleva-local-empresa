import { Mail } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { sendMagicLink } from "@/app/login/actions";

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ sent?: string; error?: string }>;
}) {
  const params = await searchParams;
  const sent = params.sent === "1";

  return (
    <main className="grid min-h-svh place-items-center px-6 py-10">
      <section className="glass w-full max-w-md rounded-[20px] p-8">
        <div className="mb-8 grid size-12 place-items-center rounded-[12px] bg-sky-200 text-slate-950">
          <Mail size={20} />
        </div>
        <h1 className="text-3xl font-semibold text-white">Entre sem senha</h1>
        <p className="mt-3 text-sm leading-6 text-white/62">
          Enviamos um link para seu e-mail. Clique nele para acessar.
        </p>
        <form action={sendMagicLink} className="mt-8 grid gap-4">
          <Input name="email" type="email" placeholder="voce@empresa.com" required />
          <Button type="submit">Enviar link de acesso</Button>
        </form>
        {sent ? (
          <p className="mt-5 rounded-[8px] bg-green-300/12 px-4 py-3 text-sm text-green-100">
            Pronto! Abre seu e-mail e segue o link. O link vale por 15 minutos.
          </p>
        ) : null}
        {params.error ? (
          <p className="mt-5 rounded-[8px] bg-rose-300/12 px-4 py-3 text-sm text-rose-100">
            Confere o e-mail e tenta de novo.
          </p>
        ) : null}
      </section>
    </main>
  );
}
