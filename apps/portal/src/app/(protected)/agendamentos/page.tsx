import { BookingCard } from "@/components/portal/booking-card";
import { EmptyState } from "@/components/portal/empty-state";
import { MotionShell } from "@/components/portal/motion-shell";
import { getBookings, getPortalContext } from "@/lib/portal-data";

export default async function BookingsPage() {
  const context = await getPortalContext();

  if (!context) {
    return null;
  }

  const bookings = await getBookings(context.tenant.id);

  return (
    <MotionShell>
      <section>
        <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 className="text-2xl font-semibold text-white">Agendamentos</h2>
            <p className="mt-2 text-sm text-white/58">
              Lista dos horarios gerados pela sua operacao automatica.
            </p>
          </div>
          <div className="flex gap-2 text-sm text-white/64">
            <span className="rounded-[8px] border border-white/12 px-3 py-2">Hoje</span>
            <span className="rounded-[8px] border border-white/12 px-3 py-2">Este mes</span>
          </div>
        </div>
        {bookings.length > 0 ? (
          <div className="grid gap-4 md:grid-cols-2">
            {bookings.map((booking) => (
              <BookingCard key={booking.id} booking={booking} />
            ))}
          </div>
        ) : (
          <EmptyState title="Nenhum agendamento hoje. Vamos trabalhar para mudar isso." />
        )}
      </section>
    </MotionShell>
  );
}
