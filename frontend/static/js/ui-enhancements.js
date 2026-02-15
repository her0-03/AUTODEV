// AutoDev - UI Enhancements & Utilities

// Toast Notifications
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="flex items-center gap-3">
            <span class="text-xl">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Confirm Dialog
function confirmDialog(message, onConfirm) {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 modal-container animate-fadeIn';
    modal.innerHTML = `
        <div class="modal-content bg-white rounded-xl p-6 max-w-md shadow-2xl">
            <h3 class="text-lg sm:text-xl font-bold mb-4">Confirmation</h3>
            <p class="text-sm sm:text-base text-gray-600 mb-6">${message}</p>
            <div class="flex gap-3 justify-end">
                <button onclick="this.closest('.fixed').remove()" class="px-4 py-2 rounded-lg border hover:bg-gray-50 text-sm sm:text-base">
                    Annuler
                </button>
                <button onclick="this.closest('.fixed').remove(); (${onConfirm})()" class="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 text-sm sm:text-base">
                    Confirmer
                </button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

// Loading Spinner
function showLoading(message = 'Chargement...') {
    const loader = document.createElement('div');
    loader.id = 'globalLoader';
    loader.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 modal-container';
    loader.innerHTML = `
        <div class="modal-content bg-white rounded-xl p-6 sm:p-8 text-center max-w-sm">
            <div class="animate-spin rounded-full h-12 w-12 sm:h-16 sm:w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
            <p class="text-sm sm:text-base text-gray-700 font-medium">${message}</p>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.getElementById('globalLoader');
    if (loader) loader.remove();
}

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K - Quick search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        // Trigger search if exists
        const searchInput = document.querySelector('[data-search]');
        if (searchInput) searchInput.focus();
    }
    
    // Ctrl/Cmd + S - Save
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const saveBtn = document.querySelector('[data-save]');
        if (saveBtn) saveBtn.click();
    }
});

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Auto-save indicator
let autoSaveTimeout;
function triggerAutoSave(callback) {
    clearTimeout(autoSaveTimeout);
    const indicator = document.getElementById('autoSaveIndicator');
    if (indicator) indicator.textContent = '💾 Sauvegarde...';
    
    autoSaveTimeout = setTimeout(() => {
        callback();
        if (indicator) {
            indicator.textContent = '✅ Sauvegardé';
            setTimeout(() => indicator.textContent = '', 2000);
        }
    }, 1000);
}

// Copy to Clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copié dans le presse-papier!', 'success', 2000);
    });
}

// Format File Size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Format Date
function formatDate(date) {
    const d = new Date(date);
    const now = new Date();
    const diff = now - d;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return 'À l\'instant';
    if (minutes < 60) return `Il y a ${minutes} min`;
    if (hours < 24) return `Il y a ${hours}h`;
    if (days < 7) return `Il y a ${days}j`;
    return d.toLocaleDateString('fr-FR');
}

// Debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-tooltip]').forEach(el => {
        el.classList.add('tooltip');
    });
});
