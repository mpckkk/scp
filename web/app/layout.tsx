import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PlantCell Library — A living library of plant cells",
  description: "An evidence-led research notebook for plant single-cell studies across space and measured time. Discover, read, review, and export a living collection.",
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
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
