import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { PineconeClient } from "@pinecone-database/pinecone";
import { env } from "./config";

export type MemoryRecord = {
  id: number;
  type: string;
  short: string;
  long: string;
  createdAt: string;
};

type MemorySchema = {
  memories: MemoryRecord[];
};

const filePath = join(process.cwd(), "gravity-claw-memory.json");
let memoryData: MemorySchema = { memories: [] };
let initialized = false;

function loadMemory() {
  if (existsSync(filePath)) {
    try {
      const json = readFileSync(filePath, "utf-8");
      memoryData = JSON.parse(json) as MemorySchema;
    } catch (error) {
      console.warn("[Memory] Failed to parse memory file, resetting", error);
      memoryData = { memories: [] };
    }
  }
  initialized = true;
}

function persistMemory() {
  writeFileSync(filePath, JSON.stringify(memoryData, null, 2), "utf-8");
}

async function ensureDb() {
  if (!initialized) {
    loadMemory();
  }
}

const pinecone = new PineconeClient();

async function initPinecone() {
  if (!env.pineconeApiKey || !env.pineconeEnvironment) {
    return;
  }
  pinecone.init({
    environment: env.pineconeEnvironment,
    apiKey: env.pineconeApiKey,
  });
}

export async function ensurePinecone() {
  await initPinecone();
  if (!env.pineconeApiKey || !env.pineconeEnvironment) {
    return;
  }
  const indexes = await pinecone.listIndexes();
  if (!indexes.includes(env.pineconeIndex)) {
    await pinecone.createIndex({
      createRequest: {
        name: env.pineconeIndex,
        dimension: 1536,
      },
    });
  }
}

export const Memory = {
  async add(type: string, short: string, long: string) {
    await ensureDb();
    const id = (memoryData.memories.length ?? 0) + 1;
    memoryData.memories.push({
      id,
      type,
      short,
      long,
      createdAt: new Date().toISOString(),
    });
    persistMemory();
  },
  async query(term: string) {
    await ensureDb();
    const query = term.toLowerCase();
    const frames = memoryData.memories.filter(
      (m) => m.short.toLowerCase().includes(query) || m.long.toLowerCase().includes(query)
    );
    return frames.slice(-10);
  },
  async pineconeUpsert(id: string, vector: number[], metadata: Record<string, string>) {
    if (!env.pineconeApiKey || !env.pineconeEnvironment) return;
    const index = pinecone.Index(env.pineconeIndex);
    await index.upsert({
      upsertRequest: { vectors: [{ id, values: vector, metadata }] },
    });
  },
};
