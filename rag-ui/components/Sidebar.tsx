"use client";

import React from "react";
import { Files, Trash2 } from "lucide-react";
import { useChat } from "@/context/ChatContext";
import { UploadZone } from "./UploadZone";
import { FileCard } from "./FileCard";
import { cn } from "@/lib/utils";

export function Sidebar() {
  const { files, removeFile, newSession, clearChat } = useChat();

  return (
    <aside className="flex w-64 shrink-0 flex-col border-r border-zinc-800 bg-zinc-900">
      {/* Header */}
      <div className="flex items-center gap-2 border-b border-zinc-800 px-4 py-3">
        <Files className="h-4 w-4 text-zinc-400" />
        <span className="text-sm font-medium text-zinc-300">Documents</span>
        {files.length > 0 && (
          <span className="ml-auto rounded-full bg-indigo-600/80 px-1.5 py-0.5 text-[10px] font-semibold text-white">
            {files.length}
          </span>
        )}
      </div>

      {/* Upload zone */}
      <div className="pt-3">
        <UploadZone />
      </div>

      {/* File list */}
      <div className="flex-1 overflow-y-auto px-3 space-y-2 pb-3">
        {files.length === 0 ? (
          <p className="text-center text-xs text-zinc-600 py-4">
            No documents uploaded
          </p>
        ) : (
          files.map((f) => (
            <FileCard key={f.id} file={f} onRemove={removeFile} />
          ))
        )}
      </div>

      {/* Bottom controls */}
      <div className="border-t border-zinc-800 p-3 space-y-1.5">
        <button
          onClick={clearChat}
          className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-xs text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200 transition-colors"
        >
          <Trash2 className="h-3.5 w-3.5" />
          Clear chat
        </button>
        <button
          onClick={newSession}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-zinc-800 px-3 py-2 text-xs font-medium text-zinc-200 hover:bg-zinc-700 transition-colors border border-zinc-700"
        >
          New Session
        </button>
      </div>
    </aside>
  );
}
