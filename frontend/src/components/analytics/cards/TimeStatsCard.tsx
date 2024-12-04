import {
  Box,
  Text,
  useColorModeValue,
  Flex,
} from '@chakra-ui/react';
import { TimeStats } from '../../../types/analytics';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface Props {
  stats: TimeStats;
}

export default function TimeStatsCard({ stats }: Props) {
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  const chartColor = useColorModeValue('rgba(49, 130, 206, 0.6)', 'rgba(99, 179, 237, 0.6)');

  const hourLabels = Array.from({ length: 24 }, (_, i) => 
    i.toString().padStart(2, '0') + ':00'
  );

  const dayLabels = [
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
  ];

  const hourData = {
    labels: hourLabels,
    datasets: [
      {
        label: 'Messages per Hour',
        data: hourLabels.map(
          (_, i) => stats.hourDistribution[i] || 0
        ),
        backgroundColor: chartColor,
      },
    ],
  };

  const dayData = {
    labels: dayLabels,
    datasets: [
      {
        label: 'Messages per Day',
        data: dayLabels.map(
          (_, i) => stats.dayDistribution[i] || 0
        ),
        backgroundColor: chartColor,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

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
        Time Distribution
      </Text>
      <Flex direction="column" gap={6}>
        <Box>
          <Text fontSize="md" mb={2}>Hourly Activity</Text>
          <Box height="200px">
            <Bar data={hourData} options={options} />
          </Box>
        </Box>
        <Box>
          <Text fontSize="md" mb={2}>Daily Activity</Text>
          <Box height="200px">
            <Bar data={dayData} options={options} />
          </Box>
        </Box>
        <Text fontSize="sm" color="gray.500">
          Average Response Time: {Math.round(stats.avgResponseTime)} seconds
        </Text>
      </Flex>
    </Box>
  );
}
