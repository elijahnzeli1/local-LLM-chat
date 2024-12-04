import { ChartData } from 'chart.js';
import BaseChart from './BaseChart';
import { ChartPreferences } from '../../../types/preferences';

interface TagData {
  tag: string;
  count: number;
  percentage: number;
}

interface Props {
  data: TagData[];
  preferences: ChartPreferences;
  maxTags?: number;
}

export default function TagDistributionChart({ data, preferences, maxTags = 10 }: Props) {
  const formatData = (): ChartData<'radar' | 'bar'> => {
    // Sort by count and take top N tags
    const topTags = [...data]
      .sort((a, b) => b.count - a.count)
      .slice(0, maxTags);

    return {
      labels: topTags.map(d => d.tag),
      datasets: [
        {
          label: 'Tag Usage',
          data: topTags.map(d => d.count),
          backgroundColor: preferences.colorScheme[0] + '40',
          borderColor: preferences.colorScheme[0],
          borderWidth: 2,
          pointBackgroundColor: preferences.colorScheme[0],
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: preferences.colorScheme[0],
        },
      ],
    };
  };

  const options = {
    scales: {
      r: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const dataPoint = data[context.dataIndex];
            return `${dataPoint.tag}: ${dataPoint.count} (${dataPoint.percentage.toFixed(1)}%)`;
          },
        },
      },
    },
  };

  return (
    <BaseChart
      data={formatData()}
      preferences={{
        ...preferences,
        chartType: preferences.chartType === 'pie' ? 'radar' : preferences.chartType,
      }}
      title="Tag Distribution"
      options={options}
    />
  );
}
