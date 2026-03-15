class QueueWorkerService {
  constructor({ workflow }) {
    this.workflow = workflow;
    this.intervalId = null;
    this.isRunning = false;
  }

  isEnabled() {
    return toBoolean(process.env.AUTO_QUEUE_ENABLED);
  }

  getIntervalMs() {
    return Number(process.env.AUTO_QUEUE_INTERVAL_MS || 300000);
  }

  start() {
    if (!this.isEnabled() || this.intervalId) {
      return false;
    }

    this.intervalId = setInterval(() => {
      this.runSafely();
    }, this.getIntervalMs());

    this.runSafely();
    return true;
  }

  async runSafely() {
    if (this.isRunning) {
      return null;
    }

    this.isRunning = true;

    try {
      const activeBrand = String(process.env.ACTIVE_BRAND || '').trim() || undefined;
      const queueResult = await this.workflow.runQueueTick({ brandKey: activeBrand });

      if (queueResult?.post) {
        console.log(
          `[queue-worker] ${queueResult.type} ${queueResult.post.id || queueResult.post.topic || 'row'}`,
        );
      }

      return queueResult;
    } catch (error) {
      console.error(`[queue-worker] ${error.message || error}`);
      return null;
    } finally {
      this.isRunning = false;
    }
  }

  stop() {
    if (!this.intervalId) {
      return;
    }

    clearInterval(this.intervalId);
    this.intervalId = null;
  }
}

function toBoolean(value) {
  return ['1', 'true', 'yes', 'on'].includes(String(value || '').trim().toLowerCase());
}

module.exports = { QueueWorkerService };
