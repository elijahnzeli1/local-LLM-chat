import {
  Box,
  Button,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverBody,
  SimpleGrid,
  useColorModeValue,
} from '@chakra-ui/react';

interface Props {
  colors: string[];
  onChange: (colors: string[]) => void;
}

const PRESET_COLORS = [
  '#3182CE', '#63B3ED', '#4FD1C5', '#38B2AC', // Blues & Teals
  '#9F7AEA', '#B794F4', '#D6BCFA', '#E9D8FD', // Purples
  '#F6AD55', '#ED8936', '#DD6B20', '#C05621', // Oranges
  '#48BB78', '#68D391', '#9AE6B4', '#C6F6D5', // Greens
  '#FC8181', '#F56565', '#E53E3E', '#C53030', // Reds
  '#B7791F', '#D69E2E', '#ECC94B', '#F6E05E', // Yellows
];

export const ColorPicker = ({ colors, onChange }: Props) => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  const handleColorClick = (color: string, index: number) => {
    const newColors = [...colors];
    newColors[index] = color;
    onChange(newColors);
  };

  return (
    <SimpleGrid columns={colors.length} spacing={2}>
      {colors.map((color, index) => (
        <Popover key={index} placement="bottom">
          <PopoverTrigger>
            <Button
              w="100%"
              h="40px"
              p={0}
              bg={color}
              _hover={{ opacity: 0.8 }}
              aria-label={`Color ${index + 1}`}
            />
          </PopoverTrigger>
          <PopoverContent w="200px" bg={bgColor} borderColor={borderColor}>
            <PopoverBody>
              <SimpleGrid columns={4} spacing={2}>
                {PRESET_COLORS.map((presetColor) => (
                  <Box
                    key={presetColor}
                    w="30px"
                    h="30px"
                    bg={presetColor}
                    borderRadius="md"
                    cursor="pointer"
                    onClick={() => handleColorClick(presetColor, index)}
                    _hover={{ opacity: 0.8 }}
                  />
                ))}
              </SimpleGrid>
            </PopoverBody>
          </PopoverContent>
        </Popover>
      ))}
    </SimpleGrid>
  );
}
