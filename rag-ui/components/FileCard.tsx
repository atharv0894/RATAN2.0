"use client";

import React from "react";
import { FileText, Trash2, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import type { UploadedFile } from "@/context/ChatContext";

interface FileCardProps {
  file: UploadedFile;
  onRemove: (id: string) => void;
}

const STATUS_ICONS = {
  idle: null,
  uploading: <Loader2 className="h-3.5 w-3.5 animate-spin text-zinc-400" />,
  processing: <Loader2 className="h-3.5 w-3.5 animate-spin text-indigo-400" />,
  ready: <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />,
  error: <AlertCircle className="h-3.5 w-3.5 text-red-400" />,
};

export function FileCard({ file, onRemove }: FileCardProps) {
  const icon = STATUS_ICONS[file.status];

  return (
    <div
      className={cn(
        "group flex items-start gap-2.5 rounded-xl px-3 py-2.5 transition-all",
        "bg-zinc-800/50 border border-zinc-700/40 hover:border-zinc-600/60"
      )}
    >
      <FileText className="h-4 w-4 shrink-0 text-indigo-400 mt-0.5" />
      <div className="min-w-0 flex-1">
        <p className="truncate text-xs font-medium text-zinc-200">
          {file.file.name}
        </p>
        <div className="flex items-center gap-1.5 mt-0.5">
          {icon}
          <p
            className={cn(
              "text-[10px]",
              file.status === "ready" && "text-emerald-400",
              file.status === "error" && "text-red-400",
              file.status === "uploading" && "text-zinc-400",
              file.status === "processing" && "text-indigo-400"
            )}
          >
            {file.status === "ready" && file.chunks
              ? `Ready · ${file.chunks} chunks`
              : file.status === "error"
              ? file.error ?? "Error"
              : file.statusLabel}
          </p>
        </div>
      </div>
      <button
        onClick={() => onRemove(file.id)}
        className="shrink-0 opacity-0 group-hover:opacity-100 transition-opacity text-zinc-500 hover:text-red-400"
        title="Remove file"
      >
        <Trash2 className="h-3.5 w-3.5" />
      </button>
    </div>
  );
}
