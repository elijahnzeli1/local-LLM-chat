import {
  Box,
  Text,
  useColorModeValue,
  Wrap,
  WrapItem,
  Tag as ChakraTag,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
} from '@chakra-ui/react';
import { TagStats } from '../../../types/analytics';

interface Props {
  stats: TagStats;
}

export default function TagStatsCard({ stats }: Props) {
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  const sortedTags = Object.entries(stats.tagDistribution)
    .sort((a, b) => b[1] - a[1]);

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
        Tag Usage
      </Text>
      
      <Text fontSize="md" mb={2}>Most Used Tags</Text>
      <Wrap mb={4}>
        {stats.mostUsedTags.map((tag) => (
          <WrapItem key={tag}>
            <ChakraTag
              size="md"
              variant="solid"
              colorScheme="blue"
            >
              {tag}
            </ChakraTag>
          </WrapItem>
        ))}
      </Wrap>

      <Box overflowY="auto" maxHeight="200px">
        <Table variant="simple" size="sm">
          <Thead>
            <Tr>
              <Th>Tag</Th>
              <Th isNumeric>Usage Count</Th>
            </Tr>
          </Thead>
          <Tbody>
            {sortedTags.map(([tag, count]) => (
              <Tr key={tag}>
                <Td>{tag}</Td>
                <Td isNumeric>{count}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    </Box>
  );
}
