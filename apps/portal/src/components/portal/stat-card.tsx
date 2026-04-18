import { cn } from "@/lib/utils";

type StatCardProps = {
  label: string;
  description: string;
  value: string;
  tone?: "sky" | "green" | "yellow" | "rose";
};

const toneClasses = {
  sky: "text-sky-200",
  green: "text-green-300",
  yellow: "text-yellow-200",
  rose: "text-rose-200",
};

export function StatCard({ label, description, value, tone = "sky" }: StatCardProps) {
  return (
    <section className="glass rounded-[12px] p-5 transition duration-200 hover:-translate-y-0.5 hover:bg-white/12">
      <p className="text-sm text-white/60">{label}</p>
      <strong className={cn("mt-3 block text-3xl font-semibold", toneClasses[tone])}>
        {value}
      </strong>
      <p className="mt-3 text-sm leading-6 text-white/58">{description}</p>
    </section>
  );
}
