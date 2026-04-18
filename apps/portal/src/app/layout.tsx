import type { Metadata } from "next";

import "@/app/globals.css";

export const metadata: Metadata = {
  title: "Portal Eleva Local",
  description: "Resumo simples da operacao automatizada dos clientes Eleva Local.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
