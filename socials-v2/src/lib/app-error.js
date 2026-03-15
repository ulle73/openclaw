class AppError extends Error {
  constructor(message, options = {}) {
    super(message);
    this.name = 'AppError';
    this.statusCode = options.statusCode || 400;
    this.details = options.details;
    this.cause = options.cause;
  }
}

module.exports = { AppError };

