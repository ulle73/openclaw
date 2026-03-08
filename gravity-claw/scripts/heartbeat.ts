import { CronJob } from "cron";
import { Bot } from "grammy";
import { env } from "../src/config";

if (!env.telegramBotToken || !env.telegramUserId) {
  throw new Error("Missing telegram heartbeat credentials.");
}

const bot = new Bot(env.telegramBotToken);

const job = new CronJob(
  `0 ${env.heartbeatMinute} ${env.heartbeatHour} * * *`,
  async () => {
    try {
      const message = `Gravity Claw heartbeat:\n- Have you tracked your weight today?\n- What's one goal to crush?\n- Any quick wins from yesterday?`;
      await bot.api.sendMessage(env.telegramUserId, message);
      console.log("[Heartbeat] Message sent");
    } catch (error) {
      console.error("[Heartbeat] Failed", error);
    }
  },
  null,
  true
);

console.log("[Heartbeat] Scheduled", job.nextDates().toJSDate().toISOString());
job.start();
