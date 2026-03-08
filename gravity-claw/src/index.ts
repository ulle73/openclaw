import { createBot } from "./telegram";
import { env } from "./config";
import { ensurePinecone } from "./memory";

async function bootstrap() {
  console.log("[GravityClaw] Starting..." );
  await ensurePinecone();
  const bot = createBot();
  await bot.api.getMe().then((botInfo) => {
    console.log(`[GravityClaw] Connected as @${botInfo.username}`);
  });
  await bot.start({ drop_pending_updates: true });
}

bootstrap().catch((err) => {
  console.error("[GravityClaw] Boot failure", err);
  process.exit(1);
});

process.on("SIGINT", () => process.exit(0));
process.on("SIGTERM", () => process.exit(0));
