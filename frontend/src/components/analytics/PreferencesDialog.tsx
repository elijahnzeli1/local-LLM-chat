import { useState } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  VStack,
  FormControl,
  FormLabel,
  Select,
  Switch,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
  Grid,
  GridItem,
} from '@chakra-ui/react';
import { preferencesService } from '../../services/preferencesService';
import { AnalyticsPreferences, ChartPreferences } from '../../types/preferences';
import { ColorPicker } from './ColorPicker';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function PreferencesDialog({ isOpen, onClose }: Props) {
  const [preferences, setPreferences] = useState<AnalyticsPreferences>(
    preferencesService.getPreferences()
  );

  const handleSave = () => {
    preferencesService.updatePreferences(preferences);
    onClose();
  };

  const handleReset = () => {
    preferencesService.resetToDefaults();
    setPreferences(preferencesService.getPreferences());
  };

  const updateChartPreferences = (
    chartKey: keyof AnalyticsPreferences['charts'],
    update: Partial<ChartPreferences>
  ) => {
    setPreferences(prev => ({
      ...prev,
      charts: {
        ...prev.charts,
        [chartKey]: {
          ...prev.charts[chartKey],
          ...update,
        },
      },
    }));
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="xl">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Analytics Preferences</ModalHeader>
        <ModalBody>
          <Tabs>
            <TabList>
              <Tab>General</Tab>
              <Tab>Charts</Tab>
              <Tab>Layout</Tab>
              <Tab>Notifications</Tab>
            </TabList>

            <TabPanels>
              <TabPanel>
                <VStack spacing={4} align="stretch">
                  <FormControl>
                    <FormLabel>Refresh Interval (seconds)</FormLabel>
                    <NumberInput
                      value={preferences.refreshInterval}
                      min={5}
                      max={300}
                      onChange={(_, value) =>
                        setPreferences(prev => ({
                          ...prev,
                          refreshInterval: value,
                        }))
                      }
                    >
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  </FormControl>

                  <FormControl>
                    <FormLabel>Default Time Range</FormLabel>
                    <Select
                      value={preferences.defaultTimeRange}
                      onChange={e =>
                        setPreferences(prev => ({
                          ...prev,
                          defaultTimeRange: e.target.value as any,
                        }))
                      }
                    >
                      <option value="7d">Last 7 Days</option>
                      <option value="30d">Last 30 Days</option>
                      <option value="90d">Last 90 Days</option>
                    </Select>
                  </FormControl>
                </VStack>
              </TabPanel>

              <TabPanel>
                <VStack spacing={6} align="stretch">
                  {Object.entries(preferences.charts).map(([key, chart]) => (
                    <FormControl key={key}>
                      <FormLabel>{key} Chart</FormLabel>
                      <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                        <GridItem>
                          <Select
                            value={chart.chartType}
                            onChange={e =>
                              updateChartPreferences(key as any, {
                                chartType: e.target.value as any,
                              })
                            }
                          >
                            <option value="bar">Bar Chart</option>
                            <option value="line">Line Chart</option>
                            <option value="pie">Pie Chart</option>
                            <option value="radar">Radar Chart</option>
                          </Select>
                        </GridItem>
                        <GridItem>
                          <FormControl display="flex" alignItems="center">
                            <FormLabel mb="0">Show Legend</FormLabel>
                            <Switch
                              isChecked={chart.showLegend}
                              onChange={e =>
                                updateChartPreferences(key as any, {
                                  showLegend: e.target.checked,
                                })
                              }
                            />
                          </FormControl>
                        </GridItem>
                        <GridItem colSpan={2}>
                          <ColorPicker
                            colors={chart.colorScheme}
                            onChange={colors =>
                              updateChartPreferences(key as any, {
                                colorScheme: colors,
                              })
                            }
                          />
                        </GridItem>
                      </Grid>
                    </FormControl>
                  ))}
                </VStack>
              </TabPanel>

              <TabPanel>
                <VStack spacing={4} align="stretch">
                  {Object.entries(preferences.dashboardLayout).map(([key, layout]) => (
                    <FormControl key={key}>
                      <FormLabel>{key} Position</FormLabel>
                      <Grid templateColumns="repeat(4, 1fr)" gap={2}>
                        <GridItem>
                          <NumberInput
                            value={layout.x}
                            min={0}
                            max={11}
                            onChange={(_, value) =>
                              setPreferences(prev => ({
                                ...prev,
                                dashboardLayout: {
                                  ...prev.dashboardLayout,
                                  [key]: { ...layout, x: value },
                                },
                              }))
                            }
                          >
                            <NumberInputField />
                            <NumberInputStepper>
                              <NumberIncrementStepper />
                              <NumberDecrementStepper />
                            </NumberInputStepper>
                          </NumberInput>
                        </GridItem>
                        <GridItem>
                          <NumberInput
                            value={layout.y}
                            min={0}
                            onChange={(_, value) =>
                              setPreferences(prev => ({
                                ...prev,
                                dashboardLayout: {
                                  ...prev.dashboardLayout,
                                  [key]: { ...layout, y: value },
                                },
                              }))
                            }
                          >
                            <NumberInputField />
                            <NumberInputStepper>
                              <NumberIncrementStepper />
                              <NumberDecrementStepper />
                            </NumberInputStepper>
                          </NumberInput>
                        </GridItem>
                        <GridItem>
                          <NumberInput
                            value={layout.w}
                            min={1}
                            max={12}
                            onChange={(_, value) =>
                              setPreferences(prev => ({
                                ...prev,
                                dashboardLayout: {
                                  ...prev.dashboardLayout,
                                  [key]: { ...layout, w: value },
                                },
                              }))
                            }
                          >
                            <NumberInputField />
                            <NumberInputStepper>
                              <NumberIncrementStepper />
                              <NumberDecrementStepper />
                            </NumberInputStepper>
                          </NumberInput>
                        </GridItem>
                        <GridItem>
                          <NumberInput
                            value={layout.h}
                            min={1}
                            onChange={(_, value) =>
                              setPreferences(prev => ({
                                ...prev,
                                dashboardLayout: {
                                  ...prev.dashboardLayout,
                                  [key]: { ...layout, h: value },
                                },
                              }))
                            }
                          >
                            <NumberInputField />
                            <NumberInputStepper>
                              <NumberIncrementStepper />
                              <NumberDecrementStepper />
                            </NumberInputStepper>
                          </NumberInput>
                        </GridItem>
                      </Grid>
                    </FormControl>
                  ))}
                </VStack>
              </TabPanel>

              <TabPanel>
                <VStack spacing={4} align="stretch">
                  <FormControl display="flex" alignItems="center">
                    <FormLabel mb="0">Enable Real-time Updates</FormLabel>
                    <Switch
                      isChecked={preferences.notifications.enableRealTime}
                      onChange={e =>
                        setPreferences(prev => ({
                          ...prev,
                          notifications: {
                            ...prev.notifications,
                            enableRealTime: e.target.checked,
                          },
                        }))
                      }
                    />
                  </FormControl>

                  <FormControl display="flex" alignItems="center">
                    <FormLabel mb="0">Notify on Thresholds</FormLabel>
                    <Switch
                      isChecked={preferences.notifications.notifyOnThreshold}
                      onChange={e =>
                        setPreferences(prev => ({
                          ...prev,
                          notifications: {
                            ...prev.notifications,
                            notifyOnThreshold: e.target.checked,
                          },
                        }))
                      }
                    />
                  </FormControl>

                  <FormControl>
                    <FormLabel>Active Conversations Threshold</FormLabel>
                    <NumberInput
                      value={preferences.notifications.thresholds.activeConversations}
                      min={1}
                      onChange={(_, value) =>
                        setPreferences(prev => ({
                          ...prev,
                          notifications: {
                            ...prev.notifications,
                            thresholds: {
                              ...prev.notifications.thresholds,
                              activeConversations: value,
                            },
                          },
                        }))
                      }
                    >
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  </FormControl>
                </VStack>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </ModalBody>

        <ModalFooter>
          <Button variant="ghost" mr={3} onClick={handleReset}>
            Reset to Defaults
          </Button>
          <Button colorScheme="blue" mr={3} onClick={handleSave}>
            Save
          </Button>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}
