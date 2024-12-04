import { ChartData } from 'chart.js';
import BaseChart from './BaseChart';
import { ChartPreferences } from '../../../types/preferences';

interface CategoryData {
  category: string;
  count: number;
  percentage: number;
}

interface Props {
  data: CategoryData[];
  preferences: ChartPreferences;
}

export default function CategoryDistributionChart({ data, preferences }: Props) {
  const formatData = (): ChartData<'pie' | 'bar'> => {
    return {
      labels: data.map(d => d.category),
      datasets: [
        {
          data: data.map(d => d.count),
          backgroundColor: preferences.colorScheme,
          borderColor: preferences.colorScheme.map(color => color + '80'),
          borderWidth: 1,
        },
      ],
    };
  };

  const options = {
    plugins: {
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const dataPoint = data[context.dataIndex];
            return `${dataPoint.category}: ${dataPoint.count} (${dataPoint.percentage.toFixed(1)}%)`;
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
        chartType: preferences.chartType === 'line' ? 'bar' : preferences.chartType,
      }}
      title="Conversation Categories"
      options={options}
    />
  );
}
