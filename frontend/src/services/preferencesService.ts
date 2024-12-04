import { AnalyticsPreferences, defaultPreferences } from '../types/preferences';

const STORAGE_KEY = 'analytics_preferences';

export class PreferencesService {
  private static instance: PreferencesService;
  private preferences: AnalyticsPreferences;
  private listeners: Set<(prefs: AnalyticsPreferences) => void>;

  private constructor() {
    this.preferences = this.loadPreferences();
    this.listeners = new Set();
  }

  static getInstance(): PreferencesService {
    if (!PreferencesService.instance) {
      PreferencesService.instance = new PreferencesService();
    }
    return PreferencesService.instance;
  }

  private loadPreferences(): AnalyticsPreferences {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        return { ...defaultPreferences, ...JSON.parse(stored) };
      } catch (error) {
        console.error('Error loading preferences:', error);
      }
    }
    return defaultPreferences;
  }

  private savePreferences() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.preferences));
      this.notifyListeners();
    } catch (error) {
      console.error('Error saving preferences:', error);
    }
  }

  private notifyListeners() {
    this.listeners.forEach(listener => listener(this.preferences));
  }

  getPreferences(): AnalyticsPreferences {
    return { ...this.preferences };
  }

  updatePreferences(update: Partial<AnalyticsPreferences>) {
    this.preferences = {
      ...this.preferences,
      ...update,
    };
    this.savePreferences();
  }

  subscribe(listener: (prefs: AnalyticsPreferences) => void) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  resetToDefaults() {
    this.preferences = { ...defaultPreferences };
    this.savePreferences();
  }
}

export const preferencesService = PreferencesService.getInstance();
