const { createRuntime } = require('./src/create-runtime');
const { loadEnv } = require('./src/lib/load-env');

loadEnv(__dirname);

function printHelp() {
  console.log(`
Usage:
  node cli.js serve [--brand <brandKey>]
  node cli.js worker [--brand <brandKey>]
  node cli.js bootstrap-sheet [--brand <brandKey>]
  node cli.js process-next [--brand <brandKey>]
  node cli.js publish <postId> [--brand <brandKey>]
  node cli.js schedule <postId> <isoDate> [--brand <brandKey>]
  node cli.js list-posts [--brand <brandKey>]
  node cli.js export <postId> [--brand <brandKey>]
`.trim());
}

async function main() {
  const runtime = createRuntime({ rootDir: __dirname });
  const command = process.argv[2];
  const brandKey = resolveBrandArg(process.argv.slice(3));
  const workflowOptions = {
    brandKey,
  };

  if (!command || command === 'help' || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  if (command === 'serve') {
    if (brandKey) {
      process.env.ACTIVE_BRAND = brandKey;
    }
    require('./index');
    return;
  }

  if (command === 'worker') {
    if (brandKey) {
      process.env.ACTIVE_BRAND = brandKey;
    }

    if (!runtime.queueWorker.start()) {
      throw new Error('AUTO_QUEUE_ENABLED is not enabled or worker already running.');
    }

    console.log(
      `Auto queue worker running with interval ${runtime.queueWorker.getIntervalMs()} ms.`,
    );
    return;
  }

  if (command === 'bootstrap-sheet') {
    const headers = await runtime.workflow.bootstrapSheet();
    console.log('Sheet headers are ready:');
    console.log(headers.join(', '));
    return;
  }

  if (command === 'process-next') {
    const result = await runtime.workflow.processNext(workflowOptions);

    if (!result) {
      console.log('No post with status "new" was found.');
      return;
    }

    console.log(`Processed post ${result.id || result.topic}`);
    console.log(`Status: ${result.status}`);
    if (result.image_path) {
      console.log(`Image: ${result.image_path}`);
    }
    return;
  }

  if (command === 'list-posts') {
    const posts = await runtime.workflow.listPosts(workflowOptions);
    console.log(JSON.stringify(posts, null, 2));
    return;
  }

  if (command === 'publish') {
    const postId = process.argv[3];

    if (!postId) {
      throw new Error('Missing postId. Usage: node cli.js publish <postId>');
    }

    const published = await runtime.workflow.publishPost(postId, workflowOptions);
    console.log(`Published ${published.id || postId}`);
    if (published.instagram_permalink) {
      console.log(`Permalink: ${published.instagram_permalink}`);
    }
    return;
  }

  if (command === 'schedule') {
    const postId = process.argv[3];
    const isoDate = process.argv[4];

    if (!postId || !isoDate) {
      throw new Error('Missing arguments. Usage: node cli.js schedule <postId> <isoDate>');
    }

    const scheduled = await runtime.workflow.schedulePost(postId, isoDate, workflowOptions);
    console.log(`Scheduled ${scheduled.id || postId} for ${scheduled.scheduled_for}`);
    return;
  }

  if (command === 'export') {
    const postId = process.argv[3];

    if (!postId) {
      throw new Error('Missing postId. Usage: node cli.js export <postId>');
    }

    const exportResult = await runtime.workflow.exportPost(postId, workflowOptions);
    console.log(`Exported to ${exportResult.exportPath}`);
    return;
  }

  throw new Error(`Unknown command: ${command}`);
}

main().catch((error) => {
  console.error(error.message || error);
  process.exitCode = 1;
});

function resolveBrandArg(args) {
  for (let index = 0; index < args.length; index += 1) {
    const value = args[index];

    if (!value) {
      continue;
    }

    if (value.startsWith('--brand=')) {
      const inline = value.split('=')[1];
      return String(inline || '').trim() || undefined;
    }

    if (value === '--brand') {
      const nextValue = args[index + 1];
      return String(nextValue || '').trim() || undefined;
    }
  }

  return String(process.env.ACTIVE_BRAND || '').trim() || undefined;
}
