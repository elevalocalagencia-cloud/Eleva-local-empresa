import { AccessState } from "@/components/portal/access-state";
import { Sidebar } from "@/components/portal/sidebar";
import { Topbar } from "@/components/portal/topbar";
import { DEMO_UI_BANNER, isDemoTenant } from "@/lib/demo-data";
import { buildPortalTenant } from "@/lib/portal-data";
import { resolveCurrentTenantAccess } from "@/lib/auth/server-tenant";

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const access = await resolveCurrentTenantAccess();

  if (!access.allowed) {
    return <AccessState message={access.message} />;
  }

  const tenant = buildPortalTenant(access.tenantId, access.userEmail);
  const demoMode = isDemoTenant(access.tenantId);

  return (
    <main className="min-h-svh px-4 py-6 md:px-8">
      {demoMode ? (
        <div className="sticky top-0 z-30 mb-4 rounded-[8px] border border-rose-300/30 bg-rose-300/12 px-4 py-3 text-center text-sm font-medium text-rose-100">
          {DEMO_UI_BANNER}
        </div>
      ) : null}
      <div className="mx-auto grid max-w-7xl gap-8 lg:grid-cols-[260px_1fr]">
        <Sidebar />
        <section>
          <Topbar tenant={tenant} />
          {children}
        </section>
      </div>
    </main>
  );
}
