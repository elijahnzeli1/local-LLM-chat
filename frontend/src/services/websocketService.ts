interface WebSocketMessage<T = unknown> {
  type: string;
  data: T;
}

type MessageHandler<T = unknown> = (data: T) => void;

export class WebSocketService {
  private static instance: WebSocketService;
  private ws: WebSocket | null = null;
  private messageHandlers: Map<string, Set<MessageHandler>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  private constructor() {
    this.connect();
  }

  static getInstance(): WebSocketService {
    if (!WebSocketService.instance) {
      WebSocketService.instance = new WebSocketService();
    }
    return WebSocketService.instance;
  }

  private connect() {
    this.ws = new WebSocket('ws://localhost:8000/ws');

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event: MessageEvent) => {
      try {
        const message = JSON.parse(event.data) as WebSocketMessage;
        const { type, data } = message;
        
        if (this.messageHandlers.has(type)) {
          this.messageHandlers.get(type)?.forEach(handler => handler(data));
        }
      } catch (error) {
        console.error('Error processing WebSocket message:', error instanceof Error ? error.message : 'Unknown error');
      }
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.attemptReconnect();
    };

    this.ws.onerror = (error: Event) => {
      console.error('WebSocket error:', error);
    };
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => {
        console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        this.connect();
      }, this.reconnectDelay * this.reconnectAttempts);
    }
  }

  subscribe<T = unknown>(type: string, handler: MessageHandler<T>) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, new Set());
    }
    this.messageHandlers.get(type)?.add(handler as MessageHandler);
  }

  unsubscribe<T = unknown>(type: string, handler: MessageHandler<T>) {
    this.messageHandlers.get(type)?.delete(handler as MessageHandler);
  }

  send<T = unknown>(type: string, data: T) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      const message: WebSocketMessage<T> = { type, data };
      this.ws.send(JSON.stringify(message));
    }
  }
}

export const analyticsSocket = WebSocketService.getInstance();
