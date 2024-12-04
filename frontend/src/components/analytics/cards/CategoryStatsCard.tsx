import {
  Box,
  Text,
} from '@chakra-ui/react';
import { useColorMode } from '@chakra-ui/color-mode';
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
} from '@chakra-ui/table';
import { CategoryStats } from '../../../types/analytics';

interface Props {
  stats: CategoryStats;
  totalConversations?: number;
}

const tableStyles = {
  table: {
    fontVariantNumeric: 'lining-nums tabular-nums',
    borderCollapse: 'collapse',
  },
  th: {
    fontFamily: 'heading',
    fontWeight: 'bold',
    textTransform: 'uppercase',
    letterSpacing: 'wider',
    textAlign: 'start',
  },
  td: {
    textAlign: 'start',
  },
};

export default function CategoryStatsCard({ stats, totalConversations = 0 }: Props) {
  const { colorMode } = useColorMode();
  const bgColor = colorMode === 'light' ? 'white' : 'gray.800';
  const borderColor = colorMode === 'light' ? 'gray.200' : 'gray.700';

  const sortedCategories = Object.entries(stats.categoryDistribution)
    .sort((a, b) => b[1] - a[1])
    .map(([name, count]) => ({
      name,
      count,
      percentage: totalConversations > 0 ? (count / totalConversations) * 100 : 0,
    }));

  return (
    <Box
      p={4}
      bg={bgColor}
      borderRadius="lg"
      borderWidth="1px"
      borderColor={borderColor}
      boxShadow="sm"
    >
      <Text fontSize="lg" fontWeight="bold" mb={4}>
        Category Distribution
      </Text>
      {sortedCategories.length === 0 ? (
        <Text color="gray.500">
          No categories found
        </Text>
      ) : (
        <TableContainer>
          <Table variant="simple" size="sm" sx={tableStyles}>
            <Thead>
              <Tr>
                <Th>Category</Th>
                <Th isNumeric>Count</Th>
                <Th isNumeric>Percentage</Th>
              </Tr>
            </Thead>
            <Tbody>
              {sortedCategories.map((category) => (
                <Tr key={category.name}>
                  <Td>{category.name}</Td>
                  <Td isNumeric>{category.count}</Td>
                  <Td isNumeric>{category.percentage.toFixed(1)}%</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
}
