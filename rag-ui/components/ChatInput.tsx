"use client";

import React, { useCallback, useRef, useState } from "react";
import { Send, Paperclip } from "lucide-react";
import { useChat } from "@/context/ChatContext";
import { cn } from "@/lib/utils";

export function ChatInput() {
  const { sendMessage, isResponding, files, uploadFile } = useChat();
  const [text, setText] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const hasReadyFiles = files.some((f) => f.status === "ready");

  const handleSend = useCallback(async () => {
    const trimmed = text.trim();
    if (!trimmed || isResponding) return;
    setText("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
    await sendMessage(trimmed);
  }, [text, isResponding, sendMessage]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = Math.min(el.scrollHeight, 160) + "px";
    }
  };

  return (
    <div className="border-t border-zinc-800 bg-zinc-950/80 backdrop-blur px-4 py-3">
      <div className="flex items-end gap-2 rounded-2xl border border-zinc-700 bg-zinc-900 px-3 py-2 focus-within:border-indigo-500/60 transition-colors shadow-lg">
        {/* Upload attachment button */}
        <button
          onClick={() => fileInputRef.current?.click()}
          className="mb-1 shrink-0 rounded-lg p-1.5 text-zinc-500 hover:bg-zinc-800 hover:text-zinc-300 transition-colors"
          title="Attach file"
        >
          <Paperclip className="h-4 w-4" />
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.txt"
          multiple
          className="sr-only"
          onChange={(e) => {
            if (e.target.files) {
              Array.from(e.target.files).forEach((f) => uploadFile(f));
            }
          }}
        />

        {/* Textarea */}
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder={
            hasReadyFiles
              ? "Ask anything about your documents…"
              : "Upload a document to start chatting…"
          }
          disabled={isResponding}
          rows={1}
          className={cn(
            "flex-1 resize-none bg-transparent text-sm text-zinc-100 placeholder-zinc-600",
            "outline-none py-1 max-h-40 leading-relaxed",
            isResponding && "opacity-50 cursor-not-allowed"
          )}
        />

        {/* Send button */}
        <button
          onClick={handleSend}
          disabled={!text.trim() || isResponding}
          className={cn(
            "mb-1 shrink-0 flex h-8 w-8 items-center justify-center rounded-lg transition-all",
            text.trim() && !isResponding
              ? "bg-indigo-600 text-white hover:bg-indigo-500 shadow-md shadow-indigo-900/40"
              : "bg-zinc-800 text-zinc-600 cursor-not-allowed"
          )}
          title="Send (Enter)"
        >
          <Send className="h-4 w-4" />
        </button>
      </div>
      <p className="mt-1.5 text-center text-[10px] text-zinc-600">
        Enter to send · Shift+Enter for newline
      </p>
    </div>
  );
}
