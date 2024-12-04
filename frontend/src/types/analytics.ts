export interface MessageStats {
  totalMessages: number;
  userMessages: number;
  assistantMessages: number;
  avgUserLength: number;
  avgAssistantLength: number;
}

export interface TimeStats {
  hourDistribution: Record<number, number>;
  dayDistribution: Record<number, number>;
  avgResponseTime: number;
}

export interface CategoryStats {
  categoryDistribution: Record<string, number>;
  mostUsedCategory: string | null;
}

export interface TagStats {
  tagDistribution: Record<string, number>;
  mostUsedTags: string[];
}

export interface ConversationStats {
  totalConversations: number;
  activeConversations: number;
  avgMessagesPerConversation: number;
  avgConversationLength: number;
  activeToday: number;
  averageLength: number;
  averageDuration: number;
}

export interface UserAnalytics {
  userId: string;
  periodStart: string;
  periodEnd: string;
  messageStats: MessageStats;
  timeStats: TimeStats;
  categoryStats: CategoryStats;
  tagStats: TagStats;
  conversationStats: ConversationStats;
}
