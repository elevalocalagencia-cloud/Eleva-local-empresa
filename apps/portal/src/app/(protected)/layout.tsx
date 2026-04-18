import { Sidebar } from "@/components/portal/sidebar";
import { Topbar } from "@/components/portal/topbar";

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-svh px-4 py-6 md:px-8">
      <div className="mx-auto grid max-w-7xl gap-8 lg:grid-cols-[260px_1fr]">
        <Sidebar />
        <section>
          <Topbar />
          {children}
        </section>
      </div>
    </main>
  );
}
