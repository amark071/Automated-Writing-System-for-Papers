import api from '../api';

// 用户登录
export const login = (username: string, password: string) => {
  return api.post('/auth/login', { username, password });
};

// 用户注册
export const register = (username: string, password: string, email: string) => {
  return api.post('/auth/register', { username, password, email });
};

// 用户登出
export const logout = () => {
  localStorage.removeItem('token');
  window.location.href = '/login';
};

// 获取当前用户信息
export const getCurrentUser = () => {
  return api.get('/auth/me');
};

// 检查用户是否已登录
export const isAuthenticated = () => {
  return !!localStorage.getItem('token');
}; 