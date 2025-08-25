'use client';

import React, { useEffect } from 'react';
import { useAuth } from '@/components/Auth/AuthProvider';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import Dashboard from '@/components/Dashboard';
import Footer from '@/components/Footer';

// Disable static generation for this page
export const dynamic = 'force-dynamic';

export default function Home() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    console.log('Home page - Auth state:', { user, isLoading });
    console.log('localStorage tokens:', {
      auth_token: localStorage.getItem('auth_token'),
      access_token: localStorage.getItem('access_token')
    });
    
    if (!isLoading && !user) {
      console.log('No user found, redirecting to landing page...');
      router.push('/landing');
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // Will redirect to login
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
      <Header />
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Welcome to Visual Memory Search
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            AI-powered screenshot search and management system
          </p>
        </div>
        
        <Dashboard />
      </main>
      <Footer />
    </div>
  );
}
