import React, { createContext, useContext, useState, useEffect } from 'react';
import { message } from 'antd';
import { axiosInstance } from '../services/api';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // 检查本地存储中的token
    const token = localStorage.getItem('token');
    if (token) {
      // 验证token并获取用户信息
      checkAuth();
    }
  }, []);

  const checkAuth = async () => {
    try {
      const response = await axiosInstance.get('/api/auth/me');
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      localStorage.removeItem('token');
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const formData = new FormData();
      formData.append('username', email);  // OAuth2 expects 'username' field
      formData.append('password', password);

      const response = await axiosInstance.post('/api/auth/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      setUser(user);
      setIsAuthenticated(true);
      message.success('登录成功');
    } catch (error) {
      message.error('登录失败，请检查邮箱和密码');
      throw error;
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      const response = await axiosInstance.post('/api/auth/register', { email, password, name });
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      setUser(user);
      setIsAuthenticated(true);
      message.success('注册成功');
    } catch (error) {
      message.error('注册失败，请稍后重试');
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setIsAuthenticated(false);
    message.success('已退出登录');
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 