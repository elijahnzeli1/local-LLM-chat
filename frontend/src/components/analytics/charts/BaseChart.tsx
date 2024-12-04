import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
  ChartData,
} from 'chart.js';
import { Line, Bar, Pie, Radar } from 'react-chartjs-2';
import { Box } from '@chakra-ui/react';
import { useColorMode } from '@chakra-ui/color-mode';
import { ChartPreferences } from '../../../types/preferences';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend
);

interface Props {
  data: ChartData<any>;
  preferences: ChartPreferences;
  height?: number;
  title?: string;
  options?: ChartOptions<any>;
}

export default function BaseChart({ data, preferences, height = 300, title, options = {} }: Props) {
  const { colorMode } = useColorMode();
  const bgColor = colorMode === 'light' ? 'white' : 'gray.800';
  const textColor = colorMode === 'light' ? 'gray.800' : 'white';

  const baseOptions: ChartOptions<any> = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: preferences.enableAnimation ? 750 : 0,
    },
    plugins: {
      legend: {
        display: preferences.showLegend,
        position: 'top' as const,
        labels: {
          color: textColor,
        },
      },
      title: {
        display: !!title,
        text: title || '',
        color: textColor,
      },
    },
    scales: {
      x: {
        ticks: {
          color: textColor,
        },
        grid: {
          color: colorMode === 'light' ? 'rgba(0,0,0,0.1)' : 'rgba(255,255,255,0.1)',
        },
      },
      y: {
        ticks: {
          color: textColor,
        },
        grid: {
          color: colorMode === 'light' ? 'rgba(0,0,0,0.1)' : 'rgba(255,255,255,0.1)',
        },
      },
    },
    ...options,
  };

  const renderChart = () => {
    const chartProps = {
      data,
      options: baseOptions,
      height,
    };

    switch (preferences.chartType) {
      case 'line':
        return <Line {...chartProps} />;
      case 'bar':
        return <Bar {...chartProps} />;
      case 'pie':
        return <Pie {...chartProps} />;
      case 'radar':
        return <Radar {...chartProps} />;
      default:
        return <Bar {...chartProps} />;
    }
  };

  return (
    <Box
      bg={bgColor}
      p={4}
      borderRadius="lg"
      boxShadow="sm"
      height={height}
      position="relative"
    >
      {renderChart()}
    </Box>
  );
}
