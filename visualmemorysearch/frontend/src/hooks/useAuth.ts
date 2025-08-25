import { useCallback } from 'react';

export const useAuth = () => {
  const getAuthToken = useCallback(() => {
    return localStorage.getItem('access_token') || localStorage.getItem('auth_token');
  }, []);

  const clearAuth = useCallback(() => {
    localStorage.clear();
    sessionStorage.clear();
  }, []);

  return {
    getAuthToken,
    clearAuth
  };
};
