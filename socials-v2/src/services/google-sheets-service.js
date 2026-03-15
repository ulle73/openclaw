const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');
const { AppError } = require('../lib/app-error');

const REQUIRED_HEADERS = [
  'brand_key',
  'id',
  'topic',
  'platform',
  'status',
  'scheduled_for',
  'title',
  'hook',
  'caption',
  'image_prompt',
  'image_path',
  'image_public_url',
  'review_notes',
  'instagram_container_id',
  'instagram_media_id',
  'instagram_permalink',
  'publish_error',
  'approved_at',
  'publish_attempted_at',
  'published_at',
  'created_at',
  'updated_at',
];

class GoogleSheetsService {
  constructor({ rootDir }) {
    this.rootDir = rootDir;
    this.clientPromise = null;
  }

  isConfigured() {
    const spreadsheetId = process.env.GOOGLE_SHEETS_SPREADSHEET_ID;
    const serviceAccountPath = this.getServiceAccountPath();
    return Boolean(spreadsheetId && fs.existsSync(serviceAccountPath));
  }

  getServiceAccountPath() {
    const configuredPath = path.resolve(
      this.rootDir,
      process.env.GOOGLE_SERVICE_ACCOUNT_KEY_PATH || './config/google-service-account.json',
    );

    if (fs.existsSync(configuredPath)) {
      return configuredPath;
    }

    const fallbacks = [
      path.resolve(this.rootDir, './config/google-service-accounts.json'),
      path.resolve(this.rootDir, './config/google-service-account.json'),
    ];

    return fallbacks.find((candidate) => fs.existsSync(candidate)) || configuredPath;
  }

  getSpreadsheetId() {
    const spreadsheetId = process.env.GOOGLE_SHEETS_SPREADSHEET_ID;

    if (!spreadsheetId) {
      throw new AppError('GOOGLE_SHEETS_SPREADSHEET_ID is missing.', { statusCode: 500 });
    }

    return spreadsheetId;
  }

  getTabName() {
    return process.env.GOOGLE_SHEETS_TAB_NAME || 'Sheet1';
  }

  async getClient() {
    if (this.clientPromise) {
      return this.clientPromise;
    }

    const keyFile = this.getServiceAccountPath();

    if (!fs.existsSync(keyFile)) {
      throw new AppError(`Google service account key not found at ${keyFile}`, {
        statusCode: 500,
      });
    }

    const auth = new google.auth.GoogleAuth({
      keyFile,
      scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });

    this.clientPromise = auth.getClient().then((client) =>
      google.sheets({
        version: 'v4',
        auth: client,
      }),
    );

    return this.clientPromise;
  }

  async ensureHeaders() {
    const { values } = await this.getRawValues();

    if (!values.length) {
      await this.writeSheet([REQUIRED_HEADERS]);
      return REQUIRED_HEADERS;
    }

    const currentHeaders = values[0].map((header) => String(header || '').trim());
    const missingHeaders = REQUIRED_HEADERS.filter((header) => !currentHeaders.includes(header));

    if (!missingHeaders.length) {
      return currentHeaders;
    }

    const nextHeaders = currentHeaders.concat(missingHeaders);
    const rewrittenValues = values.map((row, index) => {
      const paddedRow = Array(nextHeaders.length).fill('');

      for (let columnIndex = 0; columnIndex < row.length; columnIndex += 1) {
        paddedRow[columnIndex] = row[columnIndex] || '';
      }

      if (index === 0) {
        return nextHeaders;
      }

      return paddedRow;
    });

    await this.writeSheet(rewrittenValues);
    return nextHeaders;
  }

  async listRows() {
    await this.ensureHeaders();
    const { values } = await this.getRawValues();
    const headers = values[0] || [];
    const rows = values
      .slice(1)
      .map((row, index) => this.toRowObject(headers, row, index + 2))
      .filter((row) => Object.values(row).some((value) => value !== ''));

    return rows;
  }

  async listRowsForBrand(brandKey) {
    const rows = await this.listRows();
    const normalizedBrandKey = normalizeBrandKey(brandKey);

    return rows.filter((row) => {
      const rowBrandKey = normalizeBrandKey(row.brand_key);
      if (!normalizedBrandKey) {
        return true;
      }

      if (!rowBrandKey) {
        return normalizedBrandKey === 'default';
      }

      return rowBrandKey === normalizedBrandKey;
    });
  }

  async findNextRow(brandKey) {
    const rows = await this.listRowsForBrand(brandKey);
    return rows.find((row) => String(row.status || '').trim().toLowerCase() === 'new') || null;
  }

  async findNextDueScheduledRow(brandKey, now = new Date()) {
    const rows = await this.listRowsForBrand(brandKey);
    const dueRows = rows
      .filter((row) => {
        const status = String(row.status || '').trim().toLowerCase();
        if (status !== 'scheduled') {
          return false;
        }

        const scheduledAt = parseDate(row.scheduled_for);
        if (!scheduledAt) {
          return false;
        }

        return scheduledAt <= now;
      })
      .sort((left, right) => {
        const leftDate = parseDate(left.scheduled_for) || new Date(0);
        const rightDate = parseDate(right.scheduled_for) || new Date(0);
        return leftDate.getTime() - rightDate.getTime();
      });

    return dueRows[0] || null;
  }

  async findRowById(postId, brandKey) {
    const rows = await this.listRowsForBrand(brandKey);
    const normalizedTarget = String(postId || '').trim();

    return (
      rows.find((row) => {
        const rowId = String(row.id || '').trim();
        return rowId === normalizedTarget || `row-${row.rowIndex}` === normalizedTarget;
      }) || null
    );
  }

  async updateRow(rowIndex, patch) {
    const { values } = await this.getRawValues();
    const headers = values[0] || [];
    const existingRow = values[rowIndex - 1] || Array(headers.length).fill('');
    const existingObject = this.toRowObject(headers, existingRow, rowIndex);

    const merged = {
      ...existingObject,
      ...patch,
    };

    const nextRow = headers.map((header) => {
      const value = merged[header];
      return value == null ? '' : String(value);
    });

    const range = `${this.getTabName()}!A${rowIndex}:${columnIndexToLetter(headers.length)}${rowIndex}`;
    const client = await this.getClient();

    await client.spreadsheets.values.update({
      spreadsheetId: this.getSpreadsheetId(),
      range,
      valueInputOption: 'RAW',
      requestBody: {
        values: [nextRow],
      },
    });

    return this.toRowObject(headers, nextRow, rowIndex);
  }

  async getRawValues() {
    const client = await this.getClient();
    const response = await client.spreadsheets.values.get({
      spreadsheetId: this.getSpreadsheetId(),
      range: this.getTabName(),
    });

    return {
      values: response.data.values || [],
    };
  }

  async writeSheet(values) {
    const client = await this.getClient();
    await client.spreadsheets.values.update({
      spreadsheetId: this.getSpreadsheetId(),
      range: this.getTabName(),
      valueInputOption: 'RAW',
      requestBody: { values },
    });
  }

  toRowObject(headers, rowValues, rowIndex) {
    const row = { rowIndex };

    headers.forEach((header, columnIndex) => {
      row[header] = rowValues[columnIndex] || '';
    });

    return row;
  }
}

function columnIndexToLetter(columnCount) {
  let value = columnCount;
  let result = '';

  while (value > 0) {
    const modulo = (value - 1) % 26;
    result = String.fromCharCode(65 + modulo) + result;
    value = Math.floor((value - modulo) / 26);
  }

  return result;
}

function normalizeBrandKey(value) {
  return String(value || '')
    .trim()
    .toLowerCase();
}

function parseDate(value) {
  if (!value) {
    return null;
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return null;
  }

  return parsed;
}

module.exports = {
  GoogleSheetsService,
  REQUIRED_HEADERS,
};
