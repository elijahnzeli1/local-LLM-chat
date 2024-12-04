import axios from 'axios';
import { UserAnalytics } from '../types/analytics';

const BASE_URL = 'http://localhost:8000/api';

export class AnalyticsService {
  static async getUserAnalytics(
    startDate?: Date,
    endDate?: Date
  ): Promise<UserAnalytics> {
    const params = new URLSearchParams();
    if (startDate) {
      params.append('start_date', startDate.toISOString());
    }
    if (endDate) {
      params.append('end_date', endDate.toISOString());
    }

    const response = await axios.get(`${BASE_URL}/analytics/user`, {
      params,
      withCredentials: true,
    });
    return response.data;
  }

  static async exportAnalytics(
    startDate: Date,
    endDate: Date,
    format: 'csv' | 'json' = 'csv'
  ): Promise<Blob> {
    const response = await axios.get(
      `${BASE_URL}/analytics/export`,
      {
        params: {
          start_date: startDate.toISOString(),
          end_date: endDate.toISOString(),
          format,
        },
        responseType: 'blob',
        withCredentials: true,
      }
    );
    return response.data;
  }
}
