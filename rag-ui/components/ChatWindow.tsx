"use client";

import React, { useEffect, useRef } from "react";
import { useChat } from "@/context/ChatContext";
import { MessageBubble } from "./MessageBubble";
import { ChatInput } from "./ChatInput";
import { EmptyState } from "./EmptyState";
import { LoadingIndicator } from "./LoadingIndicator";

export function ChatWindow() {
  const { messages, isResponding, files } = useChat();
  const bottomRef = useRef<HTMLDivElement>(null);
  const hasFiles = files.length > 0;
  const hasMessages = messages.length > 0;

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isResponding]);

  return (
    <div className="flex flex-1 flex-col min-h-0">
      {/* Message list */}
      <div className="flex-1 overflow-y-auto py-4 space-y-2 scroll-smooth">
        {!hasMessages && !hasFiles && (
          <EmptyState />
        )}

        {!hasMessages && hasFiles && (
          <div className="flex flex-1 flex-col items-center justify-center gap-3 py-16 select-none">
            <p className="text-sm text-zinc-400">
              Documents ready. Ask a question below.
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble
            key={msg.id}
            message={msg}
            isLast={i === messages.length - 1}
            isResponding={isResponding}
          />
        ))}

        {/* Typing indicator when AI is generating */}
        {isResponding && (
          <div className="px-4">
            <LoadingIndicator />
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <ChatInput />
    </div>
  );
}
