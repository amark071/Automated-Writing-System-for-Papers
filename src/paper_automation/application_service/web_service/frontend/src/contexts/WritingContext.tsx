import React, { createContext, useContext, useState } from 'react';
import { writingApi } from '../services/api';

interface Writing {
  id: string;
  title: string;
  content: string;
  status: string;
  created_at: string;
  updated_at: string;
}

interface WritingContextType {
  currentWriting: Writing | null;
  setCurrentWriting: (writing: Writing | null) => void;
  saveWriting: (writing: Writing) => Promise<void>;
  loadWriting: (id: string) => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

const WritingContext = createContext<WritingContextType | undefined>(undefined);

export const WritingProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentWriting, setCurrentWriting] = useState<Writing | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const saveWriting = async (writing: Writing) => {
    try {
      setIsLoading(true);
      setError(null);
      await writingApi.update(writing.id, writing);
      setCurrentWriting(writing);
    } catch (err) {
      setError('保存失败');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const loadWriting = async (id: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const writing = await writingApi.get(id);
      setCurrentWriting(writing);
    } catch (err) {
      setError('加载失败');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <WritingContext.Provider
      value={{
        currentWriting,
        setCurrentWriting,
        saveWriting,
        loadWriting,
        isLoading,
        error,
      }}
    >
      {children}
    </WritingContext.Provider>
  );
};

export const useWriting = () => {
  const context = useContext(WritingContext);
  if (context === undefined) {
    throw new Error('useWriting must be used within a WritingProvider');
  }
  return context;
}; 