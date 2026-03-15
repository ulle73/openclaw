const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const { AppError } = require('../lib/app-error');
const { listFilesRecursive, readText, readTextIfExists } = require('../lib/filesystem');
const { truncate } = require('../lib/string-utils');

class TemplateService {
  constructor({ rootDir }) {
    this.rootDir = rootDir;
    this.brandsDir = path.join(rootDir, 'brands');
    this.legacyCompanyPath = path.join(rootDir, 'config', 'company.yaml');
    this.legacyPlatformsPath = path.join(rootDir, 'config', 'platforms.yaml');
    this.legacyKnowledgeDir = path.join(rootDir, 'knowledge');
  }

  listBrandKeys() {
    if (!fs.existsSync(this.brandsDir)) {
      return [];
    }

    const entries = fs.readdirSync(this.brandsDir, { withFileTypes: true });
    return entries
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
      .sort((left, right) => left.localeCompare(right));
  }

  hasLegacyTemplate() {
    return (
      fs.existsSync(this.legacyCompanyPath) &&
      fs.existsSync(this.legacyPlatformsPath) &&
      fs.existsSync(this.legacyKnowledgeDir)
    );
  }

  resolveActiveBrandKey(requestedBrandKey) {
    const availableBrandKeys = this.listBrandKeys();
    const envBrandKey = String(process.env.ACTIVE_BRAND || '').trim();
    const candidate = String(requestedBrandKey || envBrandKey || 'default').trim();

    if (availableBrandKeys.includes(candidate)) {
      return candidate;
    }

    if (availableBrandKeys.length > 0) {
      if (candidate) {
        const normalized = candidate.toLowerCase();
        const fuzzy = availableBrandKeys.find((brandKey) => brandKey.toLowerCase() === normalized);
        if (fuzzy) {
          return fuzzy;
        }
      }

      return availableBrandKeys[0];
    }

    if (this.hasLegacyTemplate()) {
      return 'legacy';
    }

    throw new AppError(
      'No brand templates found. Add at least one brand folder under brands/<brand-key>/',
      { statusCode: 500 },
    );
  }

  getBrandPaths(brandKey) {
    if (brandKey === 'legacy') {
      return {
        companyPath: this.legacyCompanyPath,
        platformsPath: this.legacyPlatformsPath,
        knowledgeDir: this.legacyKnowledgeDir,
        editablePaths: ['config/company.yaml', 'config/platforms.yaml', '.env.local', 'knowledge/**'],
      };
    }

    const brandRoot = path.join(this.brandsDir, brandKey);
    return {
      companyPath: path.join(brandRoot, 'company.yaml'),
      platformsPath: path.join(brandRoot, 'platforms.yaml'),
      knowledgeDir: path.join(brandRoot, 'knowledge'),
      editablePaths: [
        `brands/${brandKey}/company.yaml`,
        `brands/${brandKey}/platforms.yaml`,
        `brands/${brandKey}/knowledge/**`,
        '.env.local',
      ],
    };
  }

  async load(options = {}) {
    const activeBrandKey = this.resolveActiveBrandKey(options.brandKey);
    const brandPaths = this.getBrandPaths(activeBrandKey);

    const [companyRaw, platformsRaw, knowledgeDocs, brandMetaRaw] = await Promise.all([
      readText(brandPaths.companyPath),
      readText(brandPaths.platformsPath),
      this.loadKnowledgeDocs({ brandKey: activeBrandKey }),
      this.loadBrandMeta(activeBrandKey),
    ]);

    const companyDocument = yaml.load(companyRaw) || {};
    const platformDocument = yaml.load(platformsRaw) || {};
    const company = companyDocument.company || {};
    const platforms = platformDocument.platforms || {};
    const brandMeta = brandMetaRaw || {};
    const availableBrandKeys = this.listBrandKeys();
    const availableBrands = await Promise.all(
      availableBrandKeys.map(async (brandKey) => this.loadBrandSummary(brandKey)),
    );

    return {
      brand: {
        key: activeBrandKey,
        name: brandMeta.name || company.name || activeBrandKey,
        description: brandMeta.description || '',
      },
      availableBrands,
      company,
      platforms,
      activePlatforms: Object.entries(platforms)
        .filter(([, config]) => config && config.active)
        .map(([platformKey]) => platformKey),
      knowledgeDocs,
      knowledgeBundle: knowledgeDocs
        .map((doc) => `## ${doc.relativePath}\n${doc.content.trim()}`)
        .join('\n\n'),
    };
  }

  async loadPlatform(platformKey, options = {}) {
    const template = await this.load(options);
    const platformConfig = template.platforms[platformKey];

    if (!platformConfig) {
      throw new AppError(`Unknown platform "${platformKey}"`, { statusCode: 404 });
    }

    return {
      ...template,
      platformKey,
      platformConfig,
    };
  }

  getTemplateStatus(brandKey) {
    const activeBrandKey = this.resolveActiveBrandKey(brandKey);
    const brandPaths = this.getBrandPaths(activeBrandKey);

    return {
      brandKey: activeBrandKey,
      companyConfigExists: fs.existsSync(brandPaths.companyPath),
      platformsConfigExists: fs.existsSync(brandPaths.platformsPath),
      knowledgeExists: fs.existsSync(brandPaths.knowledgeDir),
      editablePaths: brandPaths.editablePaths,
    };
  }

  async loadKnowledgeDocs(options = {}) {
    const activeBrandKey = this.resolveActiveBrandKey(options.brandKey);
    const brandPaths = this.getBrandPaths(activeBrandKey);

    if (!fs.existsSync(brandPaths.knowledgeDir)) {
      return [];
    }

    const files = await listFilesRecursive(brandPaths.knowledgeDir);
    const markdownFiles = files
      .filter((filePath) => filePath.endsWith('.md'))
      .sort((left, right) => left.localeCompare(right));

    return Promise.all(
      markdownFiles.map(async (filePath) => {
        const content = await readText(filePath);
        const relativePath = path.relative(this.rootDir, filePath).split(path.sep).join('/');
        const parts = relativePath.split('/');
        const category = activeBrandKey === 'legacy' ? parts[1] || 'knowledge' : parts[3] || 'knowledge';

        return {
          absolutePath: filePath,
          relativePath,
          category,
          fileName: path.basename(filePath),
          content,
          preview: truncate(content.replace(/\s+/g, ' ').trim(), 180),
        };
      }),
    );
  }

  async loadBrandMeta(brandKey) {
    if (brandKey === 'legacy') {
      return null;
    }

    const metaPath = path.join(this.brandsDir, brandKey, 'brand.yaml');
    const content = await readTextIfExists(metaPath);
    if (!content) {
      return null;
    }

    return yaml.load(content) || null;
  }

  async loadBrandSummary(brandKey) {
    const brandPaths = this.getBrandPaths(brandKey);
    const companyRaw = await readTextIfExists(brandPaths.companyPath);
    const brandMeta = await this.loadBrandMeta(brandKey);

    let company = {};
    if (companyRaw) {
      company = (yaml.load(companyRaw) || {}).company || {};
    }

    return {
      key: brandKey,
      name: brandMeta?.name || company.name || brandKey,
      description: brandMeta?.description || '',
      hasConfig:
        fs.existsSync(brandPaths.companyPath) &&
        fs.existsSync(brandPaths.platformsPath) &&
        fs.existsSync(brandPaths.knowledgeDir),
    };
  }
}

module.exports = { TemplateService };
