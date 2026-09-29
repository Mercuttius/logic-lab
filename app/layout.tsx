import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Logic Lab · Exercícios de Node.js",
  description: "Pratique lógica de programação com 900 exercícios de lacunas e acompanhe seu aprendizado.",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="antialiased">{children}</body>
    </html>
  );
}
