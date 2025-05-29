// NoteTrail Writers Hub - Main JavaScript

// Utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    // Insert at top of content area or body
    const target = document.querySelector('.content') || document.body;
    target.insertBefore(alertDiv, target.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Project management functions
function deleteProject(projectId) {
    if (confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
        fetch(`/api/projects/${projectId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                showAlert('Project deleted successfully', 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to delete project');
                });
            }
        })
        .catch(error => {
            showAlert(`Error deleting project: ${error.message}`, 'error');
        });
    }
}

function deleteChapter(chapterId) {
    if (confirm('Are you sure you want to delete this chapter? This action cannot be undone.')) {
        fetch(`/api/chapters/${chapterId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                showAlert('Chapter deleted successfully', 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to delete chapter');
                });
            }
        })
        .catch(error => {
            showAlert(`Error deleting chapter: ${error.message}`, 'error');
        });
    }
}

// Community functions
function likePost(postId) {
    fetch(`/api/posts/${postId}/like`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to like post');
        }
    })
    .then(data => {
        // Update like count in UI
        const likeButton = document.querySelector(`[data-post-id="${postId}"] .like-count`);
        if (likeButton) {
            likeButton.textContent = data.likes_count;
        }
    })
    .catch(error => {
        showAlert(`Error: ${error.message}`, 'error');
    });
}

// Form validation and enhancement
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });
    
    return isValid;
}

// Auto-save functionality for writing workspace
let autoSaveTimer;
function enableAutoSave(textareaElement, saveUrl) {
    if (!textareaElement || !saveUrl) return;
    
    textareaElement.addEventListener('input', function() {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(() => {
            const content = textareaElement.value;
            
            fetch(saveUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: content })
            })
            .then(response => {
                if (response.ok) {
                    // Show subtle save indicator
                    showSaveIndicator();
                }
            })
            .catch(error => {
                console.error('Auto-save failed:', error);
            });
        }, 2000); // Save after 2 seconds of inactivity
    });
}

function showSaveIndicator() {
    const indicator = document.getElementById('save-indicator') || createSaveIndicator();
    indicator.textContent = 'Saved';
    indicator.style.opacity = '1';
    
    setTimeout(() => {
        indicator.style.opacity = '0';
    }, 2000);
}

function createSaveIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'save-indicator';
    indicator.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--primary);
        color: var(--primary-foreground);
        padding: 8px 16px;
        border-radius: 4px;
        font-size: 14px;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1000;
    `;
    document.body.appendChild(indicator);
    return indicator;
}

// Word count tracker
function updateWordCount(textElement, countElement) {
    if (!textElement || !countElement) return;
    
    textElement.addEventListener('input', function() {
        const text = textElement.value;
        const wordCount = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
        countElement.textContent = `${wordCount} words`;
    });
}

// Character count for social features
function updateCharacterCount(textElement, countElement, maxLength = 280) {
    if (!textElement || !countElement) return;
    
    textElement.addEventListener('input', function() {
        const remaining = maxLength - textElement.value.length;
        countElement.textContent = remaining;
        countElement.style.color = remaining < 20 ? 'var(--destructive)' : 'var(--muted-foreground)';
    });
}

// Mobile menu toggle
function initMobileMenu() {
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-open');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('mobile-open');
            }
        });
    }
}

// Theme toggle
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput) {
        let searchTimer;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimer);
            const query = searchInput.value.trim();
            
            if (query.length < 2) {
                if (searchResults) searchResults.innerHTML = '';
                return;
            }
            
            searchTimer = setTimeout(() => {
                fetch(`/api/search?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        displaySearchResults(data, searchResults);
                    })
                    .catch(error => {
                        console.error('Search error:', error);
                    });
            }, 300);
        });
    }
}

function displaySearchResults(results, container) {
    if (!container) return;
    
    if (results.length === 0) {
        container.innerHTML = '<div class="text-center py-4 text-muted-foreground">No results found</div>';
        return;
    }
    
    const html = results.map(result => `
        <a href="${result.url}" class="block p-3 hover:bg-secondary border-b border-border">
            <div class="font-medium">${result.title}</div>
            <div class="text-sm text-muted-foreground">${result.description}</div>
        </a>
    `).join('');
    
    container.innerHTML = html;
}

// Keyboard shortcuts
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + S to save (prevent default and trigger auto-save)
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const activeTextarea = document.querySelector('textarea:focus, input:focus');
            if (activeTextarea && activeTextarea.dataset.autoSave) {
                // Trigger auto-save immediately
                const event = new Event('input');
                activeTextarea.dispatchEvent(event);
                showAlert('Content saved', 'success');
            }
        }
        
        // Ctrl/Cmd + / to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.focus();
            }
        }
    });
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initMobileMenu();
    initThemeToggle();
    initSearch();
    initKeyboardShortcuts();
    
    // Auto-enhance forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
                showAlert('Please fill in all required fields', 'error');
            }
        });
    });
    
    // Auto-enhance textareas with word count
    const textareas = document.querySelectorAll('textarea[data-word-count]');
    textareas.forEach(textarea => {
        const countElement = document.querySelector(textarea.dataset.wordCount);
        if (countElement) {
            updateWordCount(textarea, countElement);
        }
    });
    
    // Auto-enhance textareas with character count
    const charCountTextareas = document.querySelectorAll('textarea[data-char-count]');
    charCountTextareas.forEach(textarea => {
        const countElement = document.querySelector(textarea.dataset.charCount);
        if (countElement) {
            updateCharacterCount(textarea, countElement);
        }
    });
    
    // Enable auto-save for writing workspace
    const autoSaveTextarea = document.querySelector('textarea[data-auto-save]');
    if (autoSaveTextarea) {
        enableAutoSave(autoSaveTextarea, autoSaveTextarea.dataset.autoSave);
    }
});

// Export functions for global use
window.NoteTrail = {
    deleteProject,
    deleteChapter,
    likePost,
    showAlert,
    updateWordCount,
    updateCharacterCount,
    enableAutoSave
};