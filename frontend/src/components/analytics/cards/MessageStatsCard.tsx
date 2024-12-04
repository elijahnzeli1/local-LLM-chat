import {
  Box,
  Stat,
  StatLabel,
  StatNumber,
  StatGroup,
  Text,
  useColorModeValue,
} from '@chakra-ui/react';
import { MessageStats } from '../../../types/analytics';

interface Props {
  stats: MessageStats;
}

export default function MessageStatsCard({ stats }: Props) {
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  return (
    <Box
      p={5}
      bg={bgColor}
      borderRadius="lg"
      borderWidth="1px"
      borderColor={borderColor}
      shadow="sm"
    >
      <Text fontSize="lg" fontWeight="bold" mb={4}>
        Message Statistics
      </Text>
      <StatGroup>
        <Stat>
          <StatLabel>Total Messages</StatLabel>
          <StatNumber>{stats.totalMessages}</StatNumber>
        </Stat>
        <Stat>
          <StatLabel>User Messages</StatLabel>
          <StatNumber>{stats.userMessages}</StatNumber>
        </Stat>
        <Stat>
          <StatLabel>Assistant Messages</StatLabel>
          <StatNumber>{stats.assistantMessages}</StatNumber>
        </Stat>
      </StatGroup>
      <StatGroup mt={4}>
        <Stat>
          <StatLabel>Avg. User Length</StatLabel>
          <StatNumber>{Math.round(stats.avgUserLength)}</StatNumber>
          <Text fontSize="sm" color="gray.500">characters</Text>
        </Stat>
        <Stat>
          <StatLabel>Avg. Assistant Length</StatLabel>
          <StatNumber>{Math.round(stats.avgAssistantLength)}</StatNumber>
          <Text fontSize="sm" color="gray.500">characters</Text>
        </Stat>
      </StatGroup>
    </Box>
  );
}
