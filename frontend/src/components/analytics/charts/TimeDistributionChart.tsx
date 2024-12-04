
import { ChartData } from 'chart.js';
import BaseChart from './BaseChart';
import { ChartPreferences } from '../../../types/preferences';

interface TimeDistributionData {
  timestamp: string;
  messageCount: number;
  responseTime: number;
  tokenCount: number;
}

interface Props {
  data: TimeDistributionData[];
  preferences: ChartPreferences;
  metric: 'messageCount' | 'responseTime' | 'tokenCount';
  timeRange: '24h' | '7d' | '30d' | '90d';
}

export default function TimeDistributionChart({ data, preferences, metric, timeRange }: Props) {
  const formatData = (): ChartData<'line' | 'bar'> => {
    const labels = data.map(d => {
      const date = new Date(d.timestamp);
      switch (timeRange) {
        case '24h':
          return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        case '7d':
          return date.toLocaleDateString([], { weekday: 'short' });
        default:
          return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
      }
    });

    const metricLabels = {
      messageCount: 'Messages',
      responseTime: 'Response Time (s)',
      tokenCount: 'Tokens',
    };

    return {
      labels,
      datasets: [
        {
          label: metricLabels[metric],
          data: data.map(d => d[metric]),
          backgroundColor: preferences.colorScheme[0],
          borderColor: preferences.colorScheme[0],
          fill: false,
        },
      ],
    };
  };

  const title = {
    messageCount: 'Message Distribution Over Time',
    responseTime: 'Response Time Distribution',
    tokenCount: 'Token Usage Distribution',
  }[metric];

  return <BaseChart data={formatData()} preferences={preferences} title={title} />;
}
