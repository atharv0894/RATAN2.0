"use client";

import React from "react";
import { BrainCircuit, RotateCcw } from "lucide-react";
import { Sidebar } from "./Sidebar";
import { ChatWindow } from "./ChatWindow";
import { useChat } from "@/context/ChatContext";

export function ChatLayout() {
  const { newSession } = useChat();

  return (
    <div className="flex h-screen flex-col bg-zinc-950 text-zinc-100 antialiased">
      {/* Top nav */}
      <header className="flex h-12 shrink-0 items-center justify-between border-b border-zinc-800 px-4">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-indigo-600 shadow-md shadow-indigo-900/50">
            <BrainCircuit className="h-4 w-4 text-white" />
          </div>
          <span className="text-sm font-semibold tracking-tight text-zinc-100">
            RAG<span className="text-indigo-400">Chat</span>
          </span>
        </div>
        <button
          onClick={newSession}
          className="flex items-center gap-1.5 rounded-lg border border-zinc-700 px-3 py-1.5 text-xs text-zinc-400 hover:border-zinc-500 hover:text-zinc-200 transition-colors"
        >
          <RotateCcw className="h-3.5 w-3.5" />
          New Session
        </button>
      </header>

      {/* Body */}
      <div className="flex flex-1 min-h-0">
        <Sidebar />
        <main className="flex flex-1 flex-col min-w-0">
          <ChatWindow />
        </main>
      </div>
    </div>
  );
}
