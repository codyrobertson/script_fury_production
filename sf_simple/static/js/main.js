/**
 * Script Fury Simple - Main JavaScript
 * Common utilities and functions
 */

// Global utilities
window.SF = {
    // Format time strings
    formatTime: function(timestamp) {
        if (!timestamp) return '';
        const date = new Date(timestamp);
        return date.toLocaleTimeString();
    },
    
    // Format file sizes
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    // Show loading state
    showLoading: function(element, text = 'Loading...') {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        
        if (element) {
            element.innerHTML = `
                <div class="loading-spinner">
                    <div class="spinner"></div>
                    <p>${text}</p>
                </div>
            `;
        }
    },
    
    // Hide loading state
    hideLoading: function(element) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        
        if (element) {
            const spinner = element.querySelector('.loading-spinner');
            if (spinner) {
                spinner.remove();
            }
        }
    },
    
    // Show toast notification
    showToast: function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-message">${message}</span>
                <button class="toast-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    },
    
    // API helper
    api: {
        request: async function(url, options = {}) {
            const defaultOptions = {
                headers: {
                    'Content-Type': 'application/json',
                },
            };
            
            const mergedOptions = { ...defaultOptions, ...options };
            
            try {
                const response = await fetch(url, mergedOptions);
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || `HTTP ${response.status}`);
                }
                
                return data;
            } catch (error) {
                console.error('API Error:', error);
                throw error;
            }
        },
        
        get: function(url) {
            return this.request(url, { method: 'GET' });
        },
        
        post: function(url, data) {
            return this.request(url, {
                method: 'POST',
                body: JSON.stringify(data)
            });
        }
    },
    
    // Session storage helpers
    storage: {
        get: function(key) {
            try {
                const item = sessionStorage.getItem(key);
                return item ? JSON.parse(item) : null;
            } catch (error) {
                console.error('Storage get error:', error);
                return null;
            }
        },
        
        set: function(key, value) {
            try {
                sessionStorage.setItem(key, JSON.stringify(value));
            } catch (error) {
                console.error('Storage set error:', error);
            }
        },
        
        remove: function(key) {
            sessionStorage.removeItem(key);
        }
    }
};

// Initialize common functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add loading spinner styles
    if (!document.getElementById('loading-styles')) {
        const style = document.createElement('style');
        style.id = 'loading-styles';
        style.textContent = `
            .loading-spinner {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 2rem;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #3498db;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin-bottom: 1rem;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .toast {
                position: fixed;
                top: 20px;
                right: 20px;
                max-width: 400px;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                z-index: 1000;
                animation: slideIn 0.3s ease;
            }
            
            .toast-info {
                background: #3498db;
                color: white;
            }
            
            .toast-success {
                background: #27ae60;
                color: white;
            }
            
            .toast-error {
                background: #e74c3c;
                color: white;
            }
            
            .toast-warning {
                background: #f39c12;
                color: white;
            }
            
            .toast-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .toast-close {
                background: none;
                border: none;
                color: inherit;
                font-size: 1.5rem;
                cursor: pointer;
                padding: 0;
                margin-left: 1rem;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Handle navigation state
    updateNavigationState();
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add form validation helpers
    addFormValidation();
    
    // Handle back button
    window.addEventListener('popstate', function(event) {
        // Handle browser back button if needed
        console.log('Navigation state changed');
    });
});

function updateNavigationState() {
    // Update navigation indicators based on current page
    const path = window.location.pathname;
    const navSteps = document.querySelectorAll('.nav-step');
    
    navSteps.forEach(step => {
        step.classList.remove('active', 'completed');
    });
    
    if (path === '/') {
        // Upload step
        const uploadStep = document.querySelector('.nav-step[data-step="upload"]');
        if (uploadStep) uploadStep.classList.add('active');
    } else if (path.includes('/generate')) {
        // Generate step
        const generateStep = document.querySelector('.nav-step[data-step="generate"]');
        if (generateStep) generateStep.classList.add('active');
    } else if (path.includes('/processing')) {
        // Processing step
        const processingStep = document.querySelector('.nav-step[data-step="processing"]');
        if (processingStep) processingStep.classList.add('active');
    }
}

function addFormValidation() {
    // Add validation to forms
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                SF.showToast('Please fill in all required fields', 'error');
            }
        });
    });
}

// Utility functions for specific pages
window.PageUtils = {
    // Upload page utilities
    upload: {
        validateFile: function(file) {
            const maxSize = 16 * 1024 * 1024; // 16MB
            const allowedTypes = ['.pdf', '.txt', '.fountain'];
            
            if (file.size > maxSize) {
                return { valid: false, error: 'File is too large. Maximum size is 16MB.' };
            }
            
            const extension = '.' + file.name.split('.').pop().toLowerCase();
            if (!allowedTypes.includes(extension)) {
                return { valid: false, error: 'Invalid file type. Please upload PDF, TXT, or Fountain files.' };
            }
            
            return { valid: true };
        },
        
        updateProgress: function(percent) {
            const progressFill = document.getElementById('progress-fill');
            if (progressFill) {
                progressFill.style.width = `${percent}%`;
            }
        }
    },
    
    // Generate page utilities
    generate: {
        updateEstimates: function(maxScenes, frameDensity) {
            let framesPerScene;
            switch(frameDensity) {
                case 'low': framesPerScene = 1; break;
                case 'medium': framesPerScene = 1.5; break;
                case 'high': framesPerScene = 2.5; break;
                default: framesPerScene = 1.5;
            }
            
            const estimatedFrames = Math.round(maxScenes * framesPerScene);
            const estimatedTime = Math.round(estimatedFrames * 0.5); // 0.5 min per frame
            
            return {
                frames: estimatedFrames,
                time: estimatedTime
            };
        }
    },
    
    // Processing page utilities
    processing: {
        updateProgress: function(status) {
            const progressFill = document.getElementById('progress-fill');
            const progressPercent = document.getElementById('progress-percent');
            const progressTitle = document.getElementById('progress-title');
            const progressDetail = document.getElementById('progress-detail');
            
            if (progressFill) {
                progressFill.style.width = `${status.progress || 0}%`;
            }
            
            if (progressPercent) {
                progressPercent.textContent = `${status.progress || 0}%`;
            }
            
            if (progressTitle) {
                progressTitle.textContent = status.current_step || 'Processing...';
            }
            
            if (progressDetail) {
                progressDetail.textContent = status.current_step || 'Starting generation...';
            }
        },
        
        createFrameCard: function(frame) {
            return `
                <div class="frame-card">
                    <div class="frame-header">
                        <span class="frame-title">Scene ${frame.scene_number}.${frame.frame_number}</span>
                        <span class="frame-status ${frame.status}">${frame.status}</span>
                    </div>
                    <div class="frame-image">
                        <img src="${frame.image_url}" alt="Frame ${frame.frame_id}"
                             onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                        <div class="image-placeholder" style="display: none;">
                            <p>Frame ${frame.scene_number}.${frame.frame_number}</p>
                            <p>${frame.location}</p>
                        </div>
                    </div>
                    <div class="frame-info">
                        <p class="frame-location">${frame.location} - ${frame.time_of_day}</p>
                        <p class="frame-description">${frame.key_visual}</p>
                    </div>
                </div>
            `;
        }
    }
};

// Error handling
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    SF.showToast('An unexpected error occurred', 'error');
});

// Unhandled promise rejections
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    SF.showToast('An unexpected error occurred', 'error');
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SF, PageUtils };
}