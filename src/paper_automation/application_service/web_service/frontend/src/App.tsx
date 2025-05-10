import React from 'react';
import { ConfigProvider } from 'antd';
import { antdConfig } from './config/antd.config';
import { RouterProvider } from 'react-router-dom';
import { router } from './routes';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { theme } from './theme';
import { AuthProvider } from './contexts/AuthContext';
import { WritingProvider } from './contexts/WritingContext';
import Layout from './components/layout/Layout';
import Login from './features/auth/Login';
import Home from './features/home/Home';
import WritingList from './features/writing/pages/WritingList';
import WritingTemplate from './features/writing/pages/WritingTemplate';
import WritingEditor from './features/writing/pages/WritingEditor';
import Topic from './features/topic/Topic';
import Learning from './features/learning/Learning';
import Community from './features/community/Community';
import Profile from './features/profile/Profile';

const App: React.FC = () => {
  return (
    <ConfigProvider {...antdConfig}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AuthProvider>
          <WritingProvider>
            <RouterProvider router={router} />
          </WritingProvider>
        </AuthProvider>
      </ThemeProvider>
    </ConfigProvider>
  );
};

export default App;
