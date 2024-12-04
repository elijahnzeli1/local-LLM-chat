import {
  Box,
  Icon,
} from '@chakra-ui/react';
import { useColorMode } from '@chakra-ui/color-mode';
import {
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
} from '@chakra-ui/stat';
import type { IconType } from 'react-icons';

interface Props {
  label: string;
  value: number | string;
  helpText?: string;
  icon?: IconType;
  change?: number;
  format?: (value: number) => string;
}

export default function MetricsCard({
  label,
  value,
  helpText,
  icon,
  change,
  format = (val) => val.toString(),
}: Props) {
  const { colorMode } = useColorMode();
  const bgColor = colorMode === 'light' ? 'white' : 'gray.800';
  const borderColor = colorMode === 'light' ? 'gray.200' : 'gray.700';

  return (
    <Box
      p={4}
      bg={bgColor}
      borderRadius="lg"
      borderWidth="1px"
      borderColor={borderColor}
      boxShadow="sm"
    >
      <Stat>
        <StatLabel display="flex" alignItems="center" gap={2}>
          {icon && <Icon as={icon} />}
          {label}
        </StatLabel>
        <StatNumber fontSize="2xl">
          {typeof value === 'number' ? format(value) : value}
        </StatNumber>
        {(helpText || change !== undefined) && (
          <StatHelpText>
            {change !== undefined && (
              <StatArrow type={change >= 0 ? 'increase' : 'decrease'} />
            )}
            {helpText || `${Math.abs(change || 0)}% vs last period`}
          </StatHelpText>
        )}
      </Stat>
    </Box>
  );
}
