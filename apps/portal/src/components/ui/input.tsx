import type { InputHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "h-12 w-full rounded-[8px] border border-white/15 bg-white/8 px-4 text-sm text-white outline-none",
        "placeholder:text-white/45 focus:border-sky-200 focus:ring-2 focus:ring-sky-200/20",
        className,
      )}
      {...props}
    />
  );
}
