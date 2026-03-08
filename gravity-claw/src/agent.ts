import OpenAI from "openai";
import { env } from "./config";
import { Memory, MemoryRecord } from "./memory";

const openai = new OpenAI({ apiKey: env.openRouterKey });

type Message = {
  role: "system" | "user" | "assistant";
  content: string;
};

export async function runGravityClaw(userId: string, text: string): Promise<string> {
  const memoryRecords: MemoryRecord[] = await Memory.query(text);
  const memories = memoryRecords.map((m) => `${m.type}: ${m.short}`).join("\n");
  const messages: Message[] = [
    {
      role: "system",
      content: "You are GravityClaw, a safe, local-first Claude-style assistant.",
    },
    {
      role: "user",
      content: `Memory context:\n${memories}\n\nUser says: ${text}`,
    },
  ];
  const response = await openai.chat.completions.create({
    model: "claude-3.5-sonic",
    messages,
    temperature: 0.3,
    max_tokens: 600,
  });
  const output = response.choices?.[0]?.message?.content?.trim() ?? "(no response)";
  await Memory.add("dialog", text, output);
  return output;
}
