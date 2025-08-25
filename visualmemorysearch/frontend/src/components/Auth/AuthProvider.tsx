'use client';

import React, { useState, useEffect, createContext, useContext } from 'react';
import { authApi } from '@/lib/authApi';

// Extend Window interface to include Google
declare global {
  interface Window {
    google?: {
      auth2: {
        getAuthInstance(): {
          isSignedIn: {
            get(): boolean;
          };
          signIn(): Promise<void>;
          signOut(): Promise<void>;
          currentUser: {
            get(): {
              getAuthResponse(): {
                id_token: string;
              };
            };
          };
        };
      };
    };
  }
}

export interface User {
  id: string;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  created_at: string;
  last_login?: string;
  avatar_url?: string;
  oauth_providers?: string[];
  is_admin?: boolean;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  signIn: () => Promise<void>;
  signOut: () => Promise<void>;
  refreshUser: () => Promise<void>;
  login: (token: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export function useAuthContext() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already authenticated
    checkAuthStatus();
    
    // Check if we have a token in URL (from OAuth callback)
    checkUrlForToken();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('accessToken') || localStorage.getItem('auth_token') || localStorage.getItem('access_token');
      if (token) {
        console.log('Token found, verifying with backend...');
        const userData = await authApi.getCurrentUserWithPermissions();
        setUser(userData);
        console.log('User authenticated:', userData);
      } else {
        console.log('No token found');
      }
    } catch (error) {
      console.error('Failed to check auth status:', error);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('auth_token');
      localStorage.removeItem('access_token');
    } finally {
      // Add a small delay to ensure token verification completes
      setTimeout(() => {
        setIsLoading(false);
      }, 100);
    }
  };

  const checkUrlForToken = () => {
    // Check if we have a token in localStorage from OAuth
    const token = localStorage.getItem('auth_token') || localStorage.getItem('access_token');
    if (token) {
      console.log('Token found in localStorage, verifying...');
      // Token exists, verify it with backend
      verifyToken(token);
    } else {
      console.log('No token found in localStorage');
    }
  };

  const verifyToken = async (token: string) => {
    try {
      console.log('Verifying token with backend...');
      // Store the token
      localStorage.setItem('auth_token', token);
      localStorage.setItem('access_token', token);
      
      // Verify token with backend
      const userData = await authApi.getCurrentUser();
      setUser(userData);
      console.log('Token verified successfully, user:', userData);
    } catch (error) {
      console.error('Failed to verify token:', error);
      localStorage.removeItem('auth_token');
      localStorage.removeItem('access_token');
    }
  };

  const signIn = async () => {
    try {
      // Initialize Google Sign-In
      if (typeof window !== 'undefined' && window.google) {
        const auth2 = window.google.auth2.getAuthInstance();
        if (!auth2.isSignedIn.get()) {
          await auth2.signIn();
        }

        const googleUser = auth2.currentUser.get();
        const idToken = googleUser.getAuthResponse().id_token;

        // Send token to backend for verification
        const response = await authApi.verifyGoogleToken(idToken);

        // Store token and user data
        localStorage.setItem('auth_token', response.access_token);
        setUser(response.user);

        // Set up token refresh
        setupTokenRefresh();
      } else {
        throw new Error('Google Sign-In not available');
      }
    } catch (error) {
      console.error('Sign in failed:', error);
      throw error;
    }
  };

  const signOut = async () => {
    try {
      // Sign out from Google
      if (typeof window !== 'undefined' && window.google) {
        const auth2 = window.google.auth2.getAuthInstance();
        await auth2.signOut();
      }
      // Sign out from backend
      await authApi.signOut();

      // Clear local state
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
    } catch (error) {
      console.error('Sign out failed:', error);
      // Still clear local state even if backend call fails
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
    }
  };

  const refreshUser = async () => {
    await checkAuthStatus();
  };

  const login = async (token: string) => {
    try {
      console.log('Login method called with token');
      // Store the token with the correct name
      localStorage.setItem('accessToken', token);
      localStorage.setItem('auth_token', token);
      localStorage.setItem('access_token', token);
      
      // Verify token with backend
      const userData = await authApi.getCurrentUser();
      setUser(userData);
      console.log('Login successful, user:', userData);
    } catch (error) {
      console.error('Login failed:', error);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('auth_token');
      localStorage.removeItem('access_token');
      throw error;
    }
  };

  const setupTokenRefresh = () => {
    // Implement token refresh logic here
    // For example, set a timer to refresh token before it expires
  };

  const value: AuthContextType = {
    user,
    isLoading,
    signIn,
    signOut,
    refreshUser,
    login,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
