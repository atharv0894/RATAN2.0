import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ChatProvider } from "@/context/ChatContext";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "RAGChat — Document Q&A",
  description:
    "Upload PDF or TXT documents and ask questions powered by retrieval-augmented generation.",
  keywords: ["RAG", "AI", "document chat", "PDF Q&A"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} font-sans bg-zinc-950 text-zinc-100 antialiased`}>
        <ChatProvider>{children}</ChatProvider>
      </body>
    </html>
  );
}
