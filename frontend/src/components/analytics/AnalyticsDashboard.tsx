import { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Heading,
  Text,
  Select,
  useToast,
  Button,
  Flex,
} from '@chakra-ui/react';
import { AnalyticsService } from '../../services/analyticsService';
import { UserAnalytics } from '../../types/analytics';
import MessageStatsCard from './cards/MessageStatsCard';
import TimeStatsCard from './cards/TimeStatsCard';
import CategoryStatsCard from './cards/CategoryStatsCard';
import TagStatsCard from './cards/TagStatsCard';
import ConversationStatsCard from './cards/ConversationStatsCard';

const TIME_RANGES = {
  '7d': { days: 7, label: 'Last 7 Days' },
  '30d': { days: 30, label: 'Last 30 Days' },
  '90d': { days: 90, label: 'Last 90 Days' },
};

export default function AnalyticsDashboard() {
  const [analytics, setAnalytics] = useState<UserAnalytics | null>(null);
  const [timeRange, setTimeRange] = useState('30d');
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  useEffect(() => {
    loadAnalytics();
  }, [timeRange]);

  const loadAnalytics = async () => {
    try {
      setIsLoading(true);
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(endDate.getDate() - TIME_RANGES[timeRange as keyof typeof TIME_RANGES].days);
      
      const data = await AnalyticsService.getUserAnalytics(startDate, endDate);
      setAnalytics(data);
    } catch (error) {
      toast({
        title: 'Error loading analytics',
        description: 'Failed to load analytics data. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = async (format: 'csv' | 'json') => {
    try {
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(endDate.getDate() - TIME_RANGES[timeRange as keyof typeof TIME_RANGES].days);
      
      const blob = await AnalyticsService.exportAnalytics(startDate, endDate, format);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analytics_${startDate.toISOString().split('T')[0]}_${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      toast({
        title: 'Export failed',
        description: 'Failed to export analytics data. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box p={4}>
      <Flex justify="space-between" align="center" mb={6}>
        <Heading size="lg">Analytics Dashboard</Heading>
        <Flex gap={4}>
          <Select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            width="200px"
          >
            {Object.entries(TIME_RANGES).map(([key, { label }]) => (
              <option key={key} value={key}>
                {label}
              </option>
            ))}
          </Select>
          <Button
            onClick={() => handleExport('csv')}
            colorScheme="blue"
            variant="outline"
          >
            Export CSV
          </Button>
          <Button
            onClick={() => handleExport('json')}
            colorScheme="blue"
            variant="outline"
          >
            Export JSON
          </Button>
        </Flex>
      </Flex>

      {isLoading ? (
        <Text>Loading analytics...</Text>
      ) : analytics ? (
        <Grid
          templateColumns="repeat(2, 1fr)"
          gap={6}
        >
          <MessageStatsCard stats={analytics.messageStats} />
          <TimeStatsCard stats={analytics.timeStats} />
          <CategoryStatsCard stats={analytics.categoryStats} />
          <TagStatsCard stats={analytics.tagStats} />
          <ConversationStatsCard
            stats={analytics.conversationStats}
            gridColumn="1 / -1"
          />
        </Grid>
      ) : (
        <Text>No analytics data available</Text>
      )}
    </Box>
  );
}
