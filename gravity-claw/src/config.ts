import "dotenv/config";

export const env = {
  telegramBotToken: process.env.TELEGRAM_BOT_TOKEN ?? "",
  telegramUserId: process.env.TELEGRAM_USER_ID ?? "",
  openRouterKey: process.env.OPEN_ROUTER_KEY ?? process.env.OPENAI_API_KEY ?? "",
  openRouterBase: process.env.OPEN_ROUTER_BASE_URL ?? "https://api.openrouter.ai/v1",
  pineconeApiKey: process.env.PINECONE_API_KEY ?? "",
  pineconeEnvironment: process.env.PINECONE_ENVIRONMENT ?? "",
  pineconeIndex: process.env.PINECONE_INDEX_NAME ?? "gravity-claw-memory",
  elevenLabsKey: process.env.ELEVEN_LABS_API_KEY ?? "",
  elevenLabsVoice: process.env.ELEVEN_LABS_VOICE ?? "alloy",
  groKey: process.env.GRO_API_KEY ?? "",
  groProjectId: process.env.GRO_PROJECT_ID ?? "",
  whisperModel: process.env.WHISPER_MODEL ?? "gpt-4o-mini-transcribe",
  railwayToken: process.env.RAILWAY_TOKEN ?? "",
  zappyApiKey: process.env.ZAPPY_API_KEY ?? "",
  supabaseUrl: process.env.SUPABASE_SERVICE_URL ?? "",
  supabaseAnonKey: process.env.SUPABASE_ANON_KEY ?? "",
  heartbeatHour: Number(process.env.HEARTBEAT_HOUR ?? "8"),
  heartbeatMinute: Number(process.env.HEARTBEAT_MINUTE ?? "0"),
};

if (!env.telegramBotToken || !env.telegramUserId) {
  console.warn("[GravityClaw] Telegram credentials are not fully configured.");
}
