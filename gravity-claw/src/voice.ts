import fetch from "node-fetch";
import { env } from "./config";

export async function textToSpeech(text: string): Promise<void> {
  if (!env.elevenLabsKey) return;
  console.log(`[Voice] Sending to ElevenLabs voice ${env.elevenLabsVoice}`);
  await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${env.elevenLabsVoice}`, {
    method: "POST",
    headers: {
      "xi-api-key": env.elevenLabsKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
}

export async function transcribeAudio(base64: string): Promise<string> {
  if (!env.groKey || !env.groProjectId) {
    return "(Gro key missing)";
  }
  const response = await fetch(`https://api.gro.com/v1/audio:transcribe`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.groKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ data: base64, model: env.whisperModel, project: env.groProjectId }),
  });
  const json = (await response.json()) as { text?: string; result?: { text?: string } };
  return json?.text ?? json?.result?.text ?? "(empty transcription)";
}
