import { Bot, GrammyError, HttpError } from "grammy";
import fetch from "node-fetch";
import { env } from "./config";
import { runGravityClaw } from "./agent";
import { textToSpeech, transcribeAudio } from "./voice";

export function createBot() {
  if (!env.telegramBotToken) {
    throw new Error("Telegram bot token is missing in .env");
  }
  const bot = new Bot(env.telegramBotToken);
  bot.on("message", async (ctx) => {
    const fromId = String(ctx.from?.id ?? "");
    if (fromId !== env.telegramUserId) {
      return;
    }
    try {
      if (ctx.message.voice) {
        const file = await ctx.api.getFile(ctx.message.voice.file_id);
        const url = `https://api.telegram.org/file/bot${env.telegramBotToken}/${file.file_path}`;
        const audio = await fetch(url).then((res) => res.arrayBuffer());
        const base64 = Buffer.from(audio).toString("base64");
        const transcript = await transcribeAudio(base64);
        await ctx.reply(`Transcribed voice: ${transcript}`);
        const answer = await runGravityClaw(fromId, transcript);
        await ctx.reply(answer);
        await textToSpeech(answer);
        return;
      }
      const text = ctx.message.text ?? "";
      const reply = await runGravityClaw(fromId, text);
      await ctx.reply(reply);
    } catch (error) {
      console.error("Telegram handler error", error);
      await ctx.reply("Sorry, GravityClaw hit a snag. Please try again.");
    }
  });

  bot.catch((err) => {
    console.error("Bot error", err);
    const detail = err.error as { description?: string; message?: string } | undefined;
    if (detail) {
      console.error("Request failed", detail.description ?? detail.message);
    }
  });
  return bot;
}
