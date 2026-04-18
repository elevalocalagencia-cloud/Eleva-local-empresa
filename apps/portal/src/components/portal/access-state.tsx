import { EmptyState } from "@/components/portal/empty-state";

export function AccessState({ message }: { message: string }) {
  return (
    <main className="grid min-h-svh place-items-center px-6 py-10">
      <section className="glass w-full max-w-2xl rounded-[20px] p-8">
        <h1 className="text-2xl font-semibold text-white">Sem acesso ao portal</h1>
        <div className="mt-6">
          <EmptyState title={message} />
        </div>
      </section>
    </main>
  );
}
