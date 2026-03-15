const { createRuntime } = require('./src/create-runtime');
const { createApp } = require('./src/server/create-app');
const { loadEnv } = require('./src/lib/load-env');

loadEnv(__dirname);

async function main() {
  const runtime = createRuntime({ rootDir: __dirname });
  const app = createApp({ runtime });
  const port = runtime.getPort();

  if (runtime.queueWorker.start()) {
    console.log(
      `Auto queue worker enabled (${runtime.queueWorker.getIntervalMs()} ms interval).`,
    );
  }

  app.listen(port, () => {
    console.log(`Social Media Manager running on http://localhost:${port}`);
  });
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
