import { useState, useCallback } from 'react';
import axios from 'axios';

interface UseApiOptions<T> {
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
}

interface UseApiResult<T, R> {
  data: T | null;
  isLoading: boolean;
  error: Error | null;
  execute: (request: R) => Promise<T | null>;
}

export function useApi<T, R>(
  apiFunction: (request: R) => Promise<T>,
  options: UseApiOptions<T> = {}
): UseApiResult<T, R> {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const execute = useCallback(
    async (request: R) => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await apiFunction(request);
        setData(result);
        options.onSuccess?.(result);
        return result;
      } catch (err) {
        let error: Error;
        if (axios.isAxiosError(err)) {
          error = new Error(err.response?.data?.detail || err.message);
        } else {
          error = err instanceof Error ? err : new Error('未知错误');
        }
        setError(error);
        options.onError?.(error);
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    [apiFunction, options]
  );

  return {
    data,
    isLoading,
    error,
    execute,
  };
} 