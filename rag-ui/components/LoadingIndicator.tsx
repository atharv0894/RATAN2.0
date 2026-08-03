"use client";

import React from "react";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

export function LoadingIndicator({ className }: { className?: string }) {
  return (
    <div className={cn("flex items-center gap-2 text-zinc-400 text-sm", className)}>
      <Loader2 className="h-4 w-4 animate-spin" />
      <span>Thinking…</span>
    </div>
  );
}

export function TypingAnimation() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="h-2 w-2 rounded-full bg-zinc-400 animate-bounce"
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </div>
  );
}
