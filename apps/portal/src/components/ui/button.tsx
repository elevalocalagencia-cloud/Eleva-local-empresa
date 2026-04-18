import type { ButtonHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "ghost";
};

export function Button({ className, variant = "primary", ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex min-h-11 items-center justify-center rounded-[8px] px-5 text-sm font-medium transition duration-200",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-300",
        variant === "primary" &&
          "bg-sky-200 text-slate-950 hover:bg-white active:scale-[0.98]",
        variant === "ghost" &&
          "border border-white/15 bg-white/5 text-white hover:bg-white/10 active:scale-[0.98]",
        className,
      )}
      {...props}
    />
  );
}
