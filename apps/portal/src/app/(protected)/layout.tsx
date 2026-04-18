import { AccessState } from "@/components/portal/access-state";
import { Sidebar } from "@/components/portal/sidebar";
import { Topbar } from "@/components/portal/topbar";
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

  return (
    <main className="min-h-svh px-4 py-6 md:px-8">
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
