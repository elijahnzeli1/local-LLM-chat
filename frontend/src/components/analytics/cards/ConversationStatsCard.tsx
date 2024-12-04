import {
  Box,
  SimpleGrid,
  Text,
  useToken,
} from '@chakra-ui/react';
import { useColorMode } from '@chakra-ui/color-mode';
import {
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
} from '@chakra-ui/stat';
import { FiUsers, FiClock, FiMessageCircle, FiActivity } from 'react-icons/fi';
import { ConversationStats } from '../../../types/analytics';

interface Props {
  stats: ConversationStats;
  previousStats?: ConversationStats;
}

export default function ConversationStatsCard({ stats, previousStats }: Props) {
  const { colorMode } = useColorMode();
  const [lightBg, darkBg] = useToken('colors', ['white', 'gray.800']);
  const [lightBorder, darkBorder] = useToken('colors', ['gray.200', 'gray.700']);
  const [lightText, darkText] = useToken('colors', ['gray.600', 'gray.400']);

  const bgColor = colorMode === 'light' ? lightBg : darkBg;
  const borderColor = colorMode === 'light' ? lightBorder : darkBorder;
  const textColor = colorMode === 'light' ? lightText : darkText;

  const calculateChange = (current: number, previous?: number) => {
    if (!previous) return undefined;
    return ((current - previous) / previous) * 100;
  };

  const metrics = [
    {
      label: 'Total Conversations',
      value: stats.totalConversations,
      icon: FiUsers,
      helpText: 'All time',
      change: calculateChange(stats.totalConversations, previousStats?.totalConversations),
    },
    {
      label: 'Active Today',
      value: stats.activeToday,
      icon: FiActivity,
      helpText: 'Last 24 hours',
      change: calculateChange(stats.activeToday, previousStats?.activeToday),
    },
    {
      label: 'Average Length',
      value: stats.averageLength,
      icon: FiMessageCircle,
      helpText: 'Messages per conversation',
      format: (val: number) => val.toFixed(1),
      change: calculateChange(stats.averageLength, previousStats?.averageLength),
    },
    {
      label: 'Average Duration',
      value: stats.averageDuration,
      icon: FiClock,
      helpText: 'Minutes per conversation',
      format: (val: number) => val.toFixed(1),
      change: calculateChange(stats.averageDuration, previousStats?.averageDuration),
    },
  ];

  return (
    <Box
      p={6}
      bg={bgColor}
      borderRadius="xl"
      borderWidth="1px"
      borderColor={borderColor}
      boxShadow="sm"
      transition="all 0.2s"
      _hover={{ boxShadow: 'md' }}
    >
      <Text fontSize="lg" fontWeight="bold" mb={6}>
        Conversation Statistics
      </Text>
      <SimpleGrid
        columns={{ base: 1, sm: 2, lg: 4 }}
        gap={6}
        minChildWidth="0"
      >
        {metrics.map((metric) => (
          <Stat
            key={metric.label}
            p={4}
            borderRadius="lg"
            borderWidth="1px"
            borderColor={borderColor}
            transition="all 0.2s"
            _hover={{ transform: 'translateY(-2px)', boxShadow: 'sm' }}
          >
            <StatLabel display="flex" alignItems="center" gap={2} color={textColor}>
              <metric.icon />
              {metric.label}
            </StatLabel>
            <StatNumber fontSize="2xl">
              {metric.format 
                ? metric.format(metric.value)
                : metric.value.toString()}
            </StatNumber>
            <StatHelpText display="flex" alignItems="center" gap={1}>
              {metric.change !== undefined && (
                <>
                  <StatArrow type={metric.change >= 0 ? 'increase' : 'decrease'} />
                  {Math.abs(metric.change).toFixed(1)}%
                </>
              )}
              <Text as="span" color={textColor}>{metric.helpText}</Text>
            </StatHelpText>
          </Stat>
        ))}
      </SimpleGrid>
    </Box>
  );
}
