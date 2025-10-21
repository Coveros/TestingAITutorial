// Chat Application JavaScript
class ChatApp {
    constructor() {
        this.isLoading = false;
        this.messageHistory = [];
        this.apiEndpoint = '/api/chat';
        this.statsEndpoint = '/api/stats';
        this.healthEndpoint = '/api/health';
        
        this.initializeElements();
        this.setupEventListeners();
        this.checkSystemHealth();
        
        // Auto-resize textarea
        this.setupAutoResize();
        
        console.log('GenAI Testing Tutorial Chat App initialized');
    }
    
    initializeElements() {
        // Core elements
        this.messagesContainer = document.getElementById('messagesContainer');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatForm = document.getElementById('chatForm');
        this.characterCount = document.getElementById('characterCount');
        
        // Header elements
        this.statusIndicator = document.getElementById('statusIndicator');
        this.clearChatButton = document.getElementById('clearChat');
        this.showStatsButton = document.getElementById('showStats');
        
        // Modal elements
        this.statsModal = document.getElementById('statsModal');
        this.statsContent = document.getElementById('statsContent');
        this.closeStatsButton = document.getElementById('closeStats');
        
        // Toast elements
        this.errorToast = document.getElementById('errorToast');
    }
    
    setupEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Input events
        this.messageInput.addEventListener('input', () => this.updateCharacterCount());
        this.messageInput.addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // Header actions
        this.clearChatButton.addEventListener('click', () => this.clearChat());
        this.showStatsButton.addEventListener('click', () => this.showStats());
        
        // Modal events
        this.closeStatsButton.addEventListener('click', () => this.closeStats());
        this.statsModal.addEventListener('click', (e) => {
            if (e.target === this.statsModal) this.closeStats();
        });
        
        // Example questions
        this.setupExampleQuestions();
        
        // Toast close
        const toastClose = this.errorToast.querySelector('.toast-close');
        if (toastClose) {
            toastClose.addEventListener('click', () => this.hideToast());
        }
        
        // Auto-hide toast after 5 seconds
        setTimeout(() => this.hideToast(), 5000);
    }
    
    setupExampleQuestions() {
        const exampleQuestions = document.querySelectorAll('.example-questions li');
        exampleQuestions.forEach(item => {
            item.addEventListener('click', () => {
                const question = item.textContent.replace(/^💬\s*"?/, '').replace(/"$/, '');
                this.messageInput.value = question;
                this.updateCharacterCount();
                this.messageInput.focus();
            });
        });
    }
    
    setupAutoResize() {
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
        });
    }
    
    updateCharacterCount() {
        const count = this.messageInput.value.length;
        const maxLength = 1000;
        
        this.characterCount.textContent = `${count}/${maxLength}`;
        
        // Update styling based on count
        this.characterCount.className = 'character-count';
        if (count > maxLength * 0.9) {
            this.characterCount.classList.add('warning');
        }
        if (count >= maxLength) {
            this.characterCount.classList.add('error');
        }
    }
    
    handleKeyDown(e) {
        // Send message with Ctrl+Enter or Cmd+Enter
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!this.isLoading && this.messageInput.value.trim()) {
                this.handleSubmit(e);
            }
        }
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input and show loading
        this.messageInput.value = '';
        this.updateCharacterCount();
        this.setLoading(true);
        
        // Show typing indicator
        const typingId = this.showTypingIndicator();
        
        try {
            // Send request to API
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator(typingId);
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }
            
            // Add assistant response
            this.addMessage(data.response, 'assistant', {
                sources: data.sources,
                responseTime: data.response_time,
                retrievalTime: data.retrieval_time,
                generationTime: data.generation_time
            });
            
            // Store in history
            this.messageHistory.push({
                user: message,
                assistant: data.response,
                timestamp: Date.now(),
                metadata: data
            });
            
        } catch (error) {
            console.error('Error sending message:', error);
            
            // Remove typing indicator
            this.removeTypingIndicator(typingId);
            
            // Show error message
            this.addMessage(
                `I apologize, but I encountered an error: ${error.message}. Please try again.`,
                'assistant',
                { error: true }
            );
            
            // Show error toast
            this.showErrorToast(`Failed to send message: ${error.message}`);
        } finally {
            this.setLoading(false);
        }
    }
    
    addMessage(content, type, metadata = {}) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.innerHTML = this.createMessageHTML(content, type, metadata);
        
        // Remove welcome message if it exists
        const welcomeMessage = this.messagesContainer.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    createMessageHTML(content, type, metadata) {
        const timestamp = new Date().toLocaleTimeString();
        const avatar = type === 'user' ? '👤' : '🤖';
        
        let sourcesHTML = '';
        if (metadata.sources && metadata.sources.length > 0) {
            const sourceItems = metadata.sources.map(source => `
                <div class="source-item">
                    <div class="source-header">
                        <div class="source-title">📄 ${source.metadata && source.metadata.source ? source.metadata.source : 'Unknown Document'}</div>
                        <div class="source-similarity">Similarity: ${source.similarity}%</div>
                    </div>
                    <div class="source-content">${this.escapeHtml(source.content)}</div>
                </div>
            `).join('');
            
            sourcesHTML = `
                <div class="message-sources">
                    <div class="sources-header">📚 Sources (${metadata.sources.length}):</div>
                    ${sourceItems}
                </div>
            `;
        }
        
        let metaInfo = timestamp;
        if (metadata.responseTime) {
            metaInfo += ` • ${(metadata.responseTime * 1000).toFixed(0)}ms`;
        }
        if (metadata.error) {
            metaInfo += ' • Error';
        }
        
        return `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-bubble">
                    ${this.formatMessageContent(content)}
                    ${sourcesHTML}
                </div>
                <div class="message-meta">
                    <span>${metaInfo}</span>
                </div>
            </div>
        `;
    }
    
    formatMessageContent(content) {
        // Basic formatting for better readability
        return this.escapeHtml(content)
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    showTypingIndicator() {
        const typingId = `typing-${Date.now()}`;
        const typingElement = document.createElement('div');
        typingElement.className = 'message assistant';
        typingElement.id = typingId;
        typingElement.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        `;
        
        this.messagesContainer.appendChild(typingElement);
        this.scrollToBottom();
        
        return typingId;
    }
    
    removeTypingIndicator(typingId) {
        const typingElement = document.getElementById(typingId);
        if (typingElement) {
            typingElement.remove();
        }
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        
        const buttonText = this.sendButton.querySelector('.button-text');
        const loadingSpinner = this.sendButton.querySelector('.loading-spinner');
        
        if (loading) {
            buttonText.style.display = 'none';
            loadingSpinner.style.display = 'flex';
            this.sendButton.disabled = true;
            this.messageInput.disabled = true;
        } else {
            buttonText.style.display = 'inline';
            loadingSpinner.style.display = 'none';
            this.sendButton.disabled = false;
            this.messageInput.disabled = false;
            this.messageInput.focus();
        }
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    clearChat() {
        // Remove all messages except welcome
        const messages = this.messagesContainer.querySelectorAll('.message');
        messages.forEach(message => message.remove());
        
        // Reset message history
        this.messageHistory = [];
        
        // Show welcome message again if it doesn't exist
        if (!this.messagesContainer.querySelector('.welcome-message')) {
            location.reload(); // Simple way to restore welcome message
        }
        
        console.log('Chat cleared');
    }
    
    async showStats() {
        this.statsModal.style.display = 'block';
        this.statsContent.innerHTML = '<div class="loading">Loading statistics...</div>';
        
        try {
            // Fetch system stats
            const response = await fetch(this.statsEndpoint);
            const stats = await response.json();
            
            // Fetch health status
            const healthResponse = await fetch(this.healthEndpoint);
            const health = await healthResponse.json();
            
            this.renderStats(stats, health);
            
        } catch (error) {
            console.error('Error fetching stats:', error);
            this.statsContent.innerHTML = `
                <div class="error">
                    <p>Failed to load statistics: ${error.message}</p>
                </div>
            `;
        }
    }
    
    renderStats(stats, health) {
        const statsHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">${stats.queries_processed || 0}</div>
                    <div class="stat-label">Queries Processed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.average_response_time || 0}s</div>
                    <div class="stat-label">Avg Response Time</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.documents_loaded || 0}</div>
                    <div class="stat-label">Documents Loaded</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${((stats.error_rate || 0) * 100).toFixed(1)}%</div>
                    <div class="stat-label">Error Rate</div>
                </div>
            </div>
            
            <div class="health-check">
                <h4 style="margin-bottom: 12px; color: #374151;">System Health</h4>
                <div class="health-item">
                    <span>Cohere API</span>
                    <span class="health-status ${health.cohere_client ? 'healthy' : 'unhealthy'}">
                        ${health.cohere_client ? 'Connected' : 'Disconnected'}
                    </span>
                </div>
                <div class="health-item">
                    <span>Vector Database</span>
                    <span class="health-status ${health.vector_db ? 'healthy' : 'unhealthy'}">
                        ${health.vector_db ? 'Connected' : 'Disconnected'}
                    </span>
                </div>
                <div class="health-item">
                    <span>Document Collection</span>
                    <span class="health-status ${health.collection ? 'healthy' : 'unhealthy'}">
                        ${health.collection ? 'Ready' : 'Not Ready'}
                    </span>
                </div>
                <div class="health-item">
                    <span>Knowledge Base</span>
                    <span class="health-status ${health.documents_loaded ? 'healthy' : 'unhealthy'}">
                        ${health.documents_loaded ? 'Loaded' : 'Empty'}
                    </span>
                </div>
            </div>
            
            <div style="margin-top: 20px; padding-top: 16px; border-top: 1px solid #e5e7eb; font-size: 0.8rem; color: #6b7280;">
                <p><strong>Session Info:</strong> ${this.messageHistory.length} messages in history</p>
                <p><strong>Last Updated:</strong> ${new Date().toLocaleString()}</p>
            </div>
        `;
        
        this.statsContent.innerHTML = statsHTML;
    }
    
    closeStats() {
        this.statsModal.style.display = 'none';
    }
    
    async checkSystemHealth() {
        try {
            const response = await fetch(this.healthEndpoint);
            const health = await response.json();
            
            this.updateStatusIndicator(health);
            
        } catch (error) {
            console.error('Health check failed:', error);
            this.updateStatusIndicator({ status: 'unhealthy' });
        }
    }
    
    updateStatusIndicator(health) {
        const statusDot = this.statusIndicator.querySelector('.status-dot');
        const statusText = this.statusIndicator.querySelector('span');
        
        if (health.status === 'healthy') {
            statusDot.className = 'status-dot connected';
            statusText.textContent = 'Connected';
        } else {
            statusDot.className = 'status-dot error';
            statusText.textContent = 'Connection Issues';
        }
    }
    
    showErrorToast(message) {
        const toastMessage = this.errorToast.querySelector('.toast-message');
        toastMessage.textContent = message;
        
        this.errorToast.classList.add('show');
        
        // Auto-hide after 5 seconds
        setTimeout(() => this.hideToast(), 5000);
    }
    
    hideToast() {
        this.errorToast.classList.remove('show');
    }
}

// Initialize the chat app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatApp = new ChatApp();
});

// Export for potential testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatApp;
}