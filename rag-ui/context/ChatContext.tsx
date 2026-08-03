"use client";

import React, {
  createContext,
  useContext,
  useCallback,
  useReducer,
  useRef,
} from "react";
import {
  ingestDocument,
  queryDocuments,
  type QueryResponse,
  type Source,
  type RetrievedChunk,
} from "@/lib/api";

// ── Types ─────────────────────────────────────────────────────────────────────

export type UploadStatus =
  | "idle"
  | "uploading"
  | "processing"
  | "ready"
  | "error";

export interface UploadedFile {
  id: string;
  file: File;
  status: UploadStatus;
  statusLabel: string;
  chunks?: number;
  error?: string;
}

export type MessageRole = "user" | "assistant" | "error";

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  sources?: Source[];
  chunks?: RetrievedChunk[];
  model?: string;
  provider?: string;
  latency_ms?: number;
  timestamp: Date;
}

// ── State ──────────────────────────────────────────────────────────────────────

interface State {
  files: UploadedFile[];
  messages: Message[];
  isResponding: boolean;
}

type Action =
  | { type: "ADD_FILE"; file: UploadedFile }
  | { type: "UPDATE_FILE"; id: string; patch: Partial<UploadedFile> }
  | { type: "REMOVE_FILE"; id: string }
  | { type: "ADD_MESSAGE"; message: Message }
  | { type: "SET_RESPONDING"; value: boolean }
  | { type: "RESET" };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "ADD_FILE":
      return { ...state, files: [...state.files, action.file] };
    case "UPDATE_FILE":
      return {
        ...state,
        files: state.files.map((f) =>
          f.id === action.id ? { ...f, ...action.patch } : f
        ),
      };
    case "REMOVE_FILE":
      return { ...state, files: state.files.filter((f) => f.id !== action.id) };
    case "ADD_MESSAGE":
      return { ...state, messages: [...state.messages, action.message] };
    case "SET_RESPONDING":
      return { ...state, isResponding: action.value };
    case "RESET":
      return { files: [], messages: [], isResponding: false };
    default:
      return state;
  }
}

// ── Context ───────────────────────────────────────────────────────────────────

interface ChatContextValue {
  files: UploadedFile[];
  messages: Message[];
  isResponding: boolean;
  uploadFile: (file: File) => Promise<void>;
  removeFile: (id: string) => void;
  sendMessage: (text: string) => Promise<void>;
  clearChat: () => void;
  newSession: () => void;
}

const ChatContext = createContext<ChatContextValue | null>(null);

export function ChatProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, {
    files: [],
    messages: [],
    isResponding: false,
  });

  const uploadFile = useCallback(async (file: File) => {
    const id = crypto.randomUUID();
    const entry: UploadedFile = {
      id,
      file,
      status: "uploading",
      statusLabel: "Uploading…",
    };
    dispatch({ type: "ADD_FILE", file: entry });

    try {
      dispatch({
        type: "UPDATE_FILE",
        id,
        patch: { status: "processing", statusLabel: "Embedding…" },
      });
      const result = await ingestDocument(file);
      dispatch({
        type: "UPDATE_FILE",
        id,
        patch: {
          status: "ready",
          statusLabel: "Ready",
          chunks: result.chunks_created,
        },
      });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Upload failed";
      dispatch({
        type: "UPDATE_FILE",
        id,
        patch: { status: "error", statusLabel: "Error", error: msg },
      });
    }
  }, []);

  const removeFile = useCallback((id: string) => {
    dispatch({ type: "REMOVE_FILE", id });
  }, []);

  const sendMessage = useCallback(
    async (text: string) => {
      const userMsg: Message = {
        id: crypto.randomUUID(),
        role: "user",
        content: text,
        timestamp: new Date(),
      };
      dispatch({ type: "ADD_MESSAGE", message: userMsg });
      dispatch({ type: "SET_RESPONDING", value: true });

      try {
        const data: QueryResponse = await queryDocuments(text, 5);
        const aiMsg: Message = {
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.answer,
          sources: data.sources,
          chunks: data.retrieved_chunks,
          model: data.model,
          provider: data.provider,
          latency_ms: data.latency_ms,
          timestamp: new Date(),
        };
        dispatch({ type: "ADD_MESSAGE", message: aiMsg });
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : "Something went wrong";
        const errMsg: Message = {
          id: crypto.randomUUID(),
          role: "error",
          content: msg,
          timestamp: new Date(),
        };
        dispatch({ type: "ADD_MESSAGE", message: errMsg });
      } finally {
        dispatch({ type: "SET_RESPONDING", value: false });
      }
    },
    []
  );

  const clearChat = useCallback(() => {
    dispatch({ type: "RESET" });
    // Keep files, only clear messages
    // Re-add files back
  }, []);

  const newSession = useCallback(() => {
    dispatch({ type: "RESET" });
  }, []);

  return (
    <ChatContext.Provider
      value={{
        files: state.files,
        messages: state.messages,
        isResponding: state.isResponding,
        uploadFile,
        removeFile,
        sendMessage,
        clearChat: newSession,
        newSession,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const ctx = useContext(ChatContext);
  if (!ctx) throw new Error("useChat must be used inside ChatProvider");
  return ctx;
}
