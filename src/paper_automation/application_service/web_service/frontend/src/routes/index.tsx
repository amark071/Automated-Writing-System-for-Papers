import { createBrowserRouter, Navigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import Home from '../features/home/Home';
import WritingList from '../features/writing/pages/WritingList';
import WritingTemplate from '../features/writing/pages/WritingTemplate';
import WritingEditor from '../features/writing/pages/WritingEditor';
import Topic from '../features/topic/Topic';
import Learning from '../features/learning/Learning';
import Community from '../features/community/Community';
import Profile from '../features/profile/Profile';
import Login from '../features/auth/Login';
import Register from '../features/auth/Register';
import NotFound from '../features/error/NotFound';
import { useAuth } from '../contexts/AuthContext';

// 受保护的路由组件
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        path: '',
        element: <Home />,
      },
      {
        path: 'writing',
        children: [
          {
            path: '',
            element: <ProtectedRoute><WritingList /></ProtectedRoute>,
          },
          {
            path: 'new',
            element: <ProtectedRoute><WritingTemplate /></ProtectedRoute>,
          },
          {
            path: 'editor/:id',
            element: <ProtectedRoute><WritingEditor /></ProtectedRoute>,
          },
        ],
      },
      {
        path: 'topic',
        element: <ProtectedRoute><Topic /></ProtectedRoute>,
      },
      {
        path: 'learning',
        element: <ProtectedRoute><Learning /></ProtectedRoute>,
      },
      {
        path: 'community',
        element: <ProtectedRoute><Community /></ProtectedRoute>,
      },
      {
        path: 'profile',
        element: <ProtectedRoute><Profile /></ProtectedRoute>,
      },
    ],
  },
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/register',
    element: <Register />,
  },
  {
    path: '*',
    element: <NotFound />,
  },
]); 