"use client";

import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { cn } from "@/lib/utils";
import { SourceCitation } from "./SourceCitation";
import { TypingAnimation } from "./LoadingIndicator";
import { AlertCircle, Bot, User } from "lucide-react";
import type { Message } from "@/context/ChatContext";

interface MessageBubbleProps {
  message: Message;
  isLast?: boolean;
  isResponding?: boolean;
}

export function MessageBubble({ message, isLast, isResponding }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const isError = message.role === "error";
  const isAI = message.role === "assistant";

  return (
    <div
      className={cn(
        "group flex gap-3 px-4 py-3 rounded-2xl transition-all",
        isUser && "flex-row-reverse"
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          "flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-semibold",
          isUser && "bg-indigo-600 text-white",
          isAI && "bg-zinc-700 text-zinc-200 ring-1 ring-zinc-600",
          isError && "bg-red-900/60 text-red-300"
        )}
      >
        {isUser ? <User className="h-4 w-4" /> : isError ? <AlertCircle className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>

      {/* Bubble */}
      <div
        className={cn(
          "max-w-[78%] space-y-1",
          isUser && "items-end"
        )}
      >
        <div
          className={cn(
            "rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm",
            isUser &&
              "bg-indigo-600 text-white rounded-tr-sm",
            isAI &&
              "bg-zinc-800 text-zinc-100 border border-zinc-700/50 rounded-tl-sm",
            isError &&
              "bg-red-900/30 text-red-300 border border-red-800/50 rounded-tl-sm"
          )}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : isError ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                code({ className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || "");
                  const isBlock = className?.includes("language-");
                  return isBlock ? (
                    <div className="mt-2 mb-1 rounded-lg overflow-hidden">
                      {match && (
                        <div className="bg-zinc-900 px-3 py-1 text-xs text-zinc-400 border-b border-zinc-700/50 font-mono">
                          {match[1]}
                        </div>
                      )}
                      <pre className="bg-zinc-900 p-3 overflow-x-auto text-xs leading-relaxed">
                        <code className={cn("font-mono text-zinc-200", className)} {...props}>
                          {children}
                        </code>
                      </pre>
                    </div>
                  ) : (
                    <code
                      className="bg-zinc-700/60 rounded px-1.5 py-0.5 font-mono text-xs text-indigo-300"
                      {...props}
                    >
                      {children}
                    </code>
                  );
                },
                table({ children }) {
                  return (
                    <div className="overflow-x-auto mt-2">
                      <table className="w-full text-xs border-collapse">{children}</table>
                    </div>
                  );
                },
                th({ children }) {
                  return (
                    <th className="border border-zinc-600 bg-zinc-700/50 px-3 py-1.5 text-left font-semibold text-zinc-300">
                      {children}
                    </th>
                  );
                },
                td({ children }) {
                  return (
                    <td className="border border-zinc-700 px-3 py-1.5 text-zinc-300">
                      {children}
                    </td>
                  );
                },
                ul({ children }) {
                  return <ul className="list-disc list-inside space-y-1 mt-1">{children}</ul>;
                },
                ol({ children }) {
                  return <ol className="list-decimal list-inside space-y-1 mt-1">{children}</ol>;
                },
                li({ children }) {
                  return <li className="text-zinc-200">{children}</li>;
                },
                p({ children }) {
                  return <p className="mb-2 last:mb-0">{children}</p>;
                },
                h1({ children }) {
                  return <h1 className="text-base font-bold mb-2">{children}</h1>;
                },
                h2({ children }) {
                  return <h2 className="text-sm font-semibold mb-1.5">{children}</h2>;
                },
                h3({ children }) {
                  return <h3 className="text-sm font-medium mb-1">{children}</h3>;
                },
                blockquote({ children }) {
                  return (
                    <blockquote className="border-l-2 border-indigo-500 pl-3 my-2 text-zinc-400 italic">
                      {children}
                    </blockquote>
                  );
                },
              }}
            >
              {message.content}
            </ReactMarkdown>
          )}

          {/* Typing indicator for last AI message while responding */}
          {isLast && isResponding && isAI && (
            <TypingAnimation />
          )}
        </div>

        {/* Citations */}
        {isAI && message.sources && message.sources.length > 0 && (
          <SourceCitation sources={message.sources} chunks={message.chunks} />
        )}

        {/* Meta */}
        {isAI && message.latency_ms && (
          <p className="text-[10px] text-zinc-600 px-1">
            {message.latency_ms.toFixed(0)}ms · {message.provider} / {message.model}
          </p>
        )}
      </div>
    </div>
  );
}
