import "./globals.css";

import { Inter } from "next/font/google";
import type { Metadata } from "next";
import { Toaster } from "@/components/ui/toaster"; // Import Toaster

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "Doc-gen Questionnaire",
  description: "MAZE Lab Questionnaire",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.variable} font-sans antialiased`}
        suppressHydrationWarning
      >
        {children}
        <Toaster /> {/* Add Toaster here */}
      </body>
    </html>
  );
}
