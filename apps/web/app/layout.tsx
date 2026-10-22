import type { Metadata } from "next";
import "./globals.css";
import vi from "@/messages/vi.json";

export const metadata: Metadata = {
  title: vi.app.title,
  description: vi.app.description,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi">
      <body className="min-h-screen bg-slate-50 antialiased flex flex-col">
        {children}
      </body>
    </html>
  );
}
