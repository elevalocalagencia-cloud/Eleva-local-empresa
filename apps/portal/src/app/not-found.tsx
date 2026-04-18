import Link from "next/link";

export default function NotFound() {
  return (
    <main className="grid min-h-svh place-items-center px-6 text-center">
      <div>
        <h1 className="text-3xl font-semibold text-white">Essa página não existe.</h1>
        <p className="mt-3 text-white/58">Talvez tenha sido movida — volta pro início?</p>
        <Link className="mt-6 inline-flex rounded-[8px] bg-sky-200 px-5 py-3 text-sm font-medium text-slate-950" href="/dashboard">
          Voltar pro início
        </Link>
      </div>
    </main>
  );
}
