import type { Booking } from "@/lib/portal-data";

export function BookingCard({ booking }: { booking: Booking }) {
  return (
    <article className="glass rounded-[12px] p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-lg font-medium text-white">{booking.customerName}</p>
          <p className="mt-1 text-sm text-white/58">{booking.source}</p>
        </div>
        <span className="rounded-full border border-white/15 px-3 py-1 text-xs text-white/70">
          {booking.status}
        </span>
      </div>
      <p className="mt-5 text-sm text-white/70">{booking.date}</p>
    </article>
  );
}
