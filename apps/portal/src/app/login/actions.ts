"use server";

import { redirect } from "next/navigation";

import { env } from "@/lib/env";
import { createSupabaseServerClient } from "@/lib/supabase/server";

export async function sendMagicLink(formData: FormData) {
  const email = String(formData.get("email") ?? "").trim().toLowerCase();

  if (!email) {
    redirect("/login?error=email");
  }

  const supabase = await createSupabaseServerClient();

  if (!supabase) {
    redirect("/login?sent=1");
  }

  await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: `${env.appUrl}/auth/callback`,
    },
  });

  redirect("/login?sent=1");
}
