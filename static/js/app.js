// FinanceAI Frontend Application
class FinanceApp {
    constructor() {
        this.isProcessing = false;
        this.uploadZone = document.querySelector('.border-dashed');
        this.fileInput = document.getElementById('fileInput');
        this.processingModal = document.getElementById('processingModal');
        this.statusSteps = document.querySelectorAll('.processing-step');
        this.initEventListeners();
    }

    initEventListeners() {
        if (!this.uploadZone) return;

        // Drag and drop events
        this.uploadZone.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadZone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadZone.addEventListener('drop', (e) => this.handleDrop(e));
        this.uploadZone.addEventListener('click', () => this.fileInput?.click());

        // File input change event
        if (this.fileInput) {
            this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadZone.classList.add('border-primary', 'bg-primary-container/10');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadZone.classList.remove('border-primary', 'bg-primary-container/10');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadZone.classList.remove('border-primary', 'bg-primary-container/10');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.uploadFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            this.uploadFile(files[0]);
        }
    }

    async uploadFile(file) {
        // Validate file type
        if (!file.name.endsWith('.csv')) {
            this.showError('Only CSV files are supported');
            return;
        }

        this.isProcessing = true;
        this.showProcessingModal();
        
        try {
            // Step 1: Upload file
            this.updateProcessingStep(0, 'uploading');
            const uploadResponse = await this.uploadFileToServer(file);
            this.updateProcessingStep(0, 'complete');

            // Step 2: Categorize transactions with Gemma
            this.updateProcessingStep(1, 'uploading');
            const categorizeResponse = await this.categorizeTransactions();
            this.updateProcessingStep(1, 'complete');

            // Step 3: Generate AI Insights with Gemma
            this.updateProcessingStep(2, 'uploading');
            const insightsResponse = await this.generateInsights();
            this.updateProcessingStep(2, 'complete');

            // Success
            this.updateProcessingStep(3, 'uploading');
            await new Promise(resolve => setTimeout(resolve, 1000));
            this.updateProcessingStep(3, 'complete');

            this.hideProcessingModal();
            this.showSuccess('File processed successfully! Data is ready for analysis.');
            
            // Reload the page or update UI with new data
            setTimeout(() => location.reload(), 2000);
        } catch (error) {
            this.hideProcessingModal();
            this.showError(error.message || 'An error occurred during processing');
            console.error('Error:', error);
        } finally {
            this.isProcessing = false;
        }
    }

    async uploadFileToServer(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Upload failed with status ${response.status}`);
        }

        return await response.json();
    }

    async categorizeTransactions() {
        const response = await fetch('/api/categorize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Categorization failed with status ${response.status}`);
        }

        return await response.json();
    }

    async generateInsights() {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Analysis failed with status ${response.status}`);
        }

        return await response.json();
    }

    showProcessingModal() {
        if (this.processingModal) {
            this.processingModal.classList.remove('hidden');
            this.processingModal.classList.add('flex');
        }
    }

    hideProcessingModal() {
        if (this.processingModal) {
            this.processingModal.classList.add('hidden');
            this.processingModal.classList.remove('flex');
        }
    }

    updateProcessingStep(stepIndex, status) {
        const step = this.statusSteps[stepIndex];
        if (!step) return;

        const icon = step.querySelector('.step-icon');
        const text = step.querySelector('.step-text');
        const statusBadge = step.querySelector('.step-status');

        // Remove all status classes
        step.classList.remove('step-pending', 'step-processing', 'step-complete');

        if (status === 'uploading') {
            step.classList.add('step-processing');
            if (icon) icon.textContent = 'hourglass_top';
            if (statusBadge) statusBadge.textContent = 'Processing...';
        } else if (status === 'complete') {
            step.classList.add('step-complete');
            if (icon) icon.textContent = 'check_circle';
            if (statusBadge) statusBadge.textContent = 'Complete';
        } else {
            step.classList.add('step-pending');
            if (icon) icon.textContent = 'schedule';
            if (statusBadge) statusBadge.textContent = 'Pending';
        }
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `fixed bottom-lg right-gutter p-md rounded-lg shadow-lg font-body-md text-white ${
            type === 'success' ? 'bg-on-tertiary-container' : 'bg-error'
        }`;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new FinanceApp();
});
