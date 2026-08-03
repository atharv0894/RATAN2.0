"use client";

import React, { useState } from "react";
import { ChevronDown, ChevronRight, BookOpen } from "lucide-react";
import type { Source, RetrievedChunk } from "@/lib/api";
import { cn } from "@/lib/utils";

interface SourceCitationProps {
  sources: Source[];
  chunks?: RetrievedChunk[];
}

export function SourceCitation({ sources, chunks }: SourceCitationProps) {
  const [open, setOpen] = useState(false);

  if (!sources.length) return null;

  return (
    <div className="mt-3 border-t border-zinc-700/50 pt-3">
      <button
        onClick={() => setOpen((p) => !p)}
        className="flex items-center gap-1.5 text-xs text-zinc-400 hover:text-zinc-200 transition-colors"
      >
        <BookOpen className="h-3.5 w-3.5" />
        <span>{sources.length} source{sources.length > 1 ? "s" : ""}</span>
        {open ? (
          <ChevronDown className="h-3.5 w-3.5" />
        ) : (
          <ChevronRight className="h-3.5 w-3.5" />
        )}
      </button>

      {open && (
        <div className="mt-2 space-y-2">
          {sources.map((src, i) => {
            const chunk = chunks?.find((c) => c.chunk_id === src.chunk_id);
            return (
              <div
                key={i}
                className="rounded-lg bg-zinc-800/60 border border-zinc-700/40 px-3 py-2 text-xs space-y-1"
              >
                <div className="flex items-center gap-2 font-medium text-zinc-300">
                  <BookOpen className="h-3 w-3 text-indigo-400 shrink-0" />
                  <span className="truncate">{src.filename}</span>
                </div>
                <div className="flex gap-3 text-zinc-500">
                  <span>Page {src.page_number}</span>
                  <span className="font-mono truncate max-w-[140px]">
                    {src.chunk_id.slice(0, 8)}…
                  </span>
                  {chunk && (
                    <span className="text-emerald-500/80">
                      score {chunk.score.toFixed(3)}
                    </span>
                  )}
                </div>
                {chunk && (
                  <p className="text-zinc-500 line-clamp-2 leading-relaxed">
                    {chunk.text}
                  </p>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
