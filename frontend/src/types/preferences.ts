export interface ChartPreferences {
  chartType: 'bar' | 'line' | 'pie' | 'radar';
  showLegend: boolean;
  enableAnimation: boolean;
  colorScheme: string[];
}

export interface AnalyticsPreferences {
  refreshInterval: number;  // in seconds
  defaultTimeRange: '7d' | '30d' | '90d';
  charts: {
    timeDistribution: ChartPreferences;
    categoryDistribution: ChartPreferences;
    tagDistribution: ChartPreferences;
  };
  dashboardLayout: {
    messageStats: { x: number; y: number; w: number; h: number };
    timeStats: { x: number; y: number; w: number; h: number };
    categoryStats: { x: number; y: number; w: number; h: number };
    tagStats: { x: number; y: number; w: number; h: number };
    conversationStats: { x: number; y: number; w: number; h: number };
  };
  notifications: {
    enableRealTime: boolean;
    notifyOnThreshold: boolean;
    thresholds: {
      activeConversations: number;
      messageCount: number;
      responseTime: number;
    };
  };
}

export const defaultPreferences: AnalyticsPreferences = {
  refreshInterval: 30,
  defaultTimeRange: '30d',
  charts: {
    timeDistribution: {
      chartType: 'bar',
      showLegend: true,
      enableAnimation: true,
      colorScheme: ['#3182CE', '#63B3ED', '#4FD1C5', '#38B2AC'],
    },
    categoryDistribution: {
      chartType: 'pie',
      showLegend: true,
      enableAnimation: true,
      colorScheme: ['#9F7AEA', '#B794F4', '#D6BCFA', '#E9D8FD'],
    },
    tagDistribution: {
      chartType: 'radar',
      showLegend: false,
      enableAnimation: true,
      colorScheme: ['#F6AD55', '#ED8936', '#DD6B20', '#C05621'],
    },
  },
  dashboardLayout: {
    messageStats: { x: 0, y: 0, w: 6, h: 2 },
    timeStats: { x: 6, y: 0, w: 6, h: 4 },
    categoryStats: { x: 0, y: 2, w: 6, h: 3 },
    tagStats: { x: 6, y: 4, w: 6, h: 3 },
    conversationStats: { x: 0, y: 5, w: 12, h: 2 },
  },
  notifications: {
    enableRealTime: true,
    notifyOnThreshold: true,
    thresholds: {
      activeConversations: 10,
      messageCount: 1000,
      responseTime: 5,
    },
  },
};
