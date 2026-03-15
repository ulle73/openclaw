const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');

function loadEnv(rootDir) {
  const candidates = ['.env.local', '.env'];

  for (const fileName of candidates) {
    const filePath = path.join(rootDir, fileName);

    if (!fs.existsSync(filePath)) {
      continue;
    }

    dotenv.config({
      path: filePath,
      quiet: true,
      override: false,
    });
  }
}

module.exports = { loadEnv };

