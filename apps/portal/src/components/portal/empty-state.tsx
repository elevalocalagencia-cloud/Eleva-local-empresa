export function EmptyState({ title }: { title: string }) {
  return (
    <div className="rounded-[12px] border border-dashed border-white/18 px-6 py-10 text-center">
      <p className="mx-auto max-w-xl text-sm leading-6 text-white/62">{title}</p>
    </div>
  );
}
