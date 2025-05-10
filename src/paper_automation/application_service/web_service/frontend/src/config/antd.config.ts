import type { ThemeConfig } from 'antd';
import { ConfigProvider } from 'antd';

export const antdConfig: ThemeConfig = {
  token: {
    colorPrimary: '#1976d2',
    colorSuccess: '#2e7d32',
    colorWarning: '#ed6c02',
    colorError: '#d32f2f',
    colorInfo: '#0288d1',
    borderRadius: 8,
  },
  components: {
    Button: {
      borderRadius: 8,
    },
    Card: {
      borderRadius: 12,
    },
    Input: {
      borderRadius: 8,
    },
  },
};

export const initAntd = () => {
  ConfigProvider.config({
    ...antdConfig,
  });
}; 