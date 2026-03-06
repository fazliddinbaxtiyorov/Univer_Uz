/* ===================================
   UniBase - Timer Component
   Countdown timer for test-taking
   =================================== */

class TestTimer {
    constructor(durationMinutes, onTimeUp) {
        this.duration = durationMinutes * 60; // Convert to seconds
        this.remainingTime = this.duration;
        this.onTimeUp = onTimeUp;
        this.intervalId = null;
        this.isPaused = false;
    }

    start() {
        if (this.intervalId) return; // Already running

        this.intervalId = setInterval(() => {
            if (!this.isPaused) {
                this.remainingTime--;
                this.updateDisplay();

                // Check warnings
                if (this.remainingTime === 300) { // 5 minutes
                    this.showWarning('5 minutes remaining!');
                } else if (this.remainingTime === 60) { // 1 minute
                    this.showWarning('1 minute remaining!');
                }

                // Time up
                if (this.remainingTime <= 0) {
                    this.stop();
                    if (this.onTimeUp) {
                        this.onTimeUp();
                    }
                }
            }
        }, 1000);
    }

    stop() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    pause() {
        this.isPaused = true;
    }

    resume() {
        this.isPaused = false;
    }

    updateDisplay() {
        const timerElement = document.getElementById('timer-display');
        if (!timerElement) return;

        const minutes = Math.floor(this.remainingTime / 60);
        const seconds = this.remainingTime % 60;

        timerElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        // Update timer class based on time remaining
        timerElement.classList.remove('warning', 'danger');
        if (this.remainingTime <= 60) {
            timerElement.classList.add('danger');
        } else if (this.remainingTime <= 300) {
            timerElement.classList.add('warning');
        }
    }

    showWarning(message) {
        // Show alert
        const alertContainer = document.getElementById('alert-container');
        if (alertContainer) {
            alertContainer.innerHTML = `
        <div class="alert alert-warning">
          <strong>⚠️ Warning:</strong> ${message}
        </div>
      `;

            // Auto-hide after 5 seconds
            setTimeout(() => {
                alertContainer.innerHTML = '';
            }, 5000);
        }
    }

    getTimeSpent() {
        return this.duration - this.remainingTime;
    }

    getFormattedTimeSpent() {
        const timeSpent = this.getTimeSpent();
        const minutes = Math.floor(timeSpent / 60);
        const seconds = timeSpent % 60;
        return `${minutes}m ${seconds}s`;
    }
}
