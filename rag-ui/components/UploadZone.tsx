"use client";

import React, { useCallback, useRef, useState } from "react";
import { Upload, FileText, AlertCircle } from "lucide-react";
import { useChat } from "@/context/ChatContext";
import { cn } from "@/lib/utils";

const SUPPORTED = [".pdf", ".txt"];
const MAX_MB = 20;

export function UploadZone() {
  const { uploadFile } = useChat();
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validate = (file: File) => {
    const ext = "." + file.name.split(".").pop()?.toLowerCase();
    if (!SUPPORTED.includes(ext)) {
      return `Unsupported type: ${ext}. Use PDF or TXT.`;
    }
    if (file.size > MAX_MB * 1024 * 1024) {
      return `File too large. Max ${MAX_MB}MB.`;
    }
    return null;
  };

  const handleFiles = useCallback(
    (files: FileList | null) => {
      if (!files?.length) return;
      setError(null);
      Array.from(files).forEach((file) => {
        const err = validate(file);
        if (err) {
          setError(err);
          return;
        }
        uploadFile(file);
      });
    },
    [uploadFile]
  );

  return (
    <div className="px-3 pb-3">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => inputRef.current?.click()}
        className={cn(
          "cursor-pointer rounded-xl border-2 border-dashed px-4 py-5 text-center transition-all",
          dragging
            ? "border-indigo-500 bg-indigo-500/10"
            : "border-zinc-700 hover:border-zinc-500 hover:bg-zinc-800/50"
        )}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.txt"
          multiple
          className="sr-only"
          onChange={(e) => handleFiles(e.target.files)}
        />
        <div className="flex flex-col items-center gap-2">
          <Upload className={cn("h-7 w-7", dragging ? "text-indigo-400" : "text-zinc-500")} />
          <p className="text-xs text-zinc-400 leading-relaxed">
            <span className="font-medium text-zinc-300">Click to upload</span>
            <br />
            or drag & drop
          </p>
          <p className="text-[10px] text-zinc-600">PDF · TXT · max {MAX_MB}MB</p>
        </div>
      </div>

      {error && (
        <div className="mt-2 flex items-center gap-1.5 text-xs text-red-400">
          <AlertCircle className="h-3.5 w-3.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
