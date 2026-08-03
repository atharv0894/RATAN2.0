"use client";

import React from "react";
import { FileText, Upload } from "lucide-react";

export function EmptyState() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-6 select-none">
      <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-zinc-800 ring-1 ring-zinc-700 shadow-xl">
        <FileText className="h-9 w-9 text-zinc-300" />
      </div>
      <div className="text-center space-y-2 max-w-sm">
        <h2 className="text-lg font-semibold text-zinc-100">
          No documents yet
        </h2>
        <p className="text-sm text-zinc-400 leading-relaxed">
          Upload a <span className="text-zinc-200 font-medium">PDF</span> or{" "}
          <span className="text-zinc-200 font-medium">TXT</span> document to
          begin chatting.
          <br />
          Your files exist only for this session.
        </p>
      </div>
      <div className="flex items-center gap-2 rounded-full border border-dashed border-zinc-600 px-5 py-2.5 text-sm text-zinc-500">
        <Upload className="h-4 w-4" />
        <span>Use the sidebar to upload a file</span>
      </div>
    </div>
  );
}
