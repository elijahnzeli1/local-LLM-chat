import { Grid } from '@chakra-ui/react';
import { FiMessageCircle, FiClock, FiHash, FiUsers } from 'react-icons/fi';
import MetricsCard from './MetricsCard';

interface Metrics {
  totalMessages: number;
  averageResponseTime: number;
  totalTokens: number;
  activeConversations: number;
  messageChange: number;
  responseTimeChange: number;
  tokenChange: number;
  conversationChange: number;
}

interface Props {
  metrics: Metrics;
}

export default function MetricsGrid({ metrics }: Props) {
  const formatResponseTime = (time: number) => {
    return time < 1 ? `${(time * 1000).toFixed(0)}ms` : `${time.toFixed(1)}s`;
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`;
    }
    return num.toString();
  };

  return (
    <Grid
      templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(4, 1fr)' }}
      gap={4}
    >
      <MetricsCard
        label="Total Messages"
        value={metrics.totalMessages}
        change={metrics.messageChange}
        icon={FiMessageCircle}
        format={formatNumber}
      />
      <MetricsCard
        label="Average Response Time"
        value={metrics.averageResponseTime}
        change={metrics.responseTimeChange}
        icon={FiClock}
        format={formatResponseTime}
      />
      <MetricsCard
        label="Total Tokens"
        value={metrics.totalTokens}
        change={metrics.tokenChange}
        icon={FiHash}
        format={formatNumber}
      />
      <MetricsCard
        label="Active Conversations"
        value={metrics.activeConversations}
        change={metrics.conversationChange}
        icon={FiUsers}
        format={formatNumber}
      />
    </Grid>
  );
}
