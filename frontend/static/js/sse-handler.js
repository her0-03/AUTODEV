// SSE (Server-Sent Events) Handler for real-time streaming

class SSEHandler {
    constructor(url, options = {}) {
        this.url = url;
        this.options = options;
        this.eventSource = null;
    }
    
    connect(onMessage, onError, onComplete) {
        this.eventSource = new EventSource(this.url);
        
        this.eventSource.onmessage = (event) => {
            if (onMessage) onMessage(event.data);
        };
        
        this.eventSource.onerror = (error) => {
            if (onError) onError(error);
            this.close();
            if (onComplete) onComplete();
        };
    }
    
    close() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }
}

// Export for use in other scripts
window.SSEHandler = SSEHandler;
