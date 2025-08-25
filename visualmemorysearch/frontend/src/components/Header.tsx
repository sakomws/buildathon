'use client';

import React, { useState, useRef, useEffect } from 'react';
import { FileText, User, Settings, LogOut, ChevronDown, ChevronUp, BarChart3 } from 'lucide-react';
import { useAuth } from '@/components/Auth/AuthProvider';
import UserAccountManager from './UserAccountManager';

export default function Header() {
  const { user, signOut } = useAuth();
  const [showProfileDropdown, setShowProfileDropdown] = useState(false);
  const [showAccountManager, setShowAccountManager] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowProfileDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSignOut = async () => {
    try {
      await signOut();
      setShowProfileDropdown(false);
    } catch (error) {
      console.error('Sign out failed:', error);
    }
  };

  const toggleProfileDropdown = () => {
    setShowProfileDropdown(!showProfileDropdown);
  };

  const handleAccountManager = () => {
    setShowAccountManager(!showAccountManager);
    setShowProfileDropdown(false);
  };

  return (
    <>
      <header className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 border-b border-gray-700/50 backdrop-blur-sm transition-all duration-300 shadow-2xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-emerald-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg">
                  <FileText className="w-6 h-6 text-white" />
                </div>
                <span className="text-white font-bold text-xl bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent">Visual Memory Search</span>
              </div>
              
              {/* Navigation Links */}
              {user && (
                <div className="hidden md:flex items-center space-x-4 ml-8">
                  <a
                    href="/"
                    className="text-gray-300 hover:text-emerald-400 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-gray-800/50"
                  >
                    Dashboard
                  </a>
                  <a
                    href="/analytics"
                    className="text-gray-300 hover:text-emerald-400 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-gray-800/50 flex items-center"
                  >
                    <BarChart3 className="w-4 h-4 mr-2" />
                    Analytics
                  </a>
                </div>
              )}
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Dark mode toggle removed */}

              {user ? (
                <div className="relative" ref={dropdownRef}>
                  <button
                    onClick={toggleProfileDropdown}
                    className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-gray-800/50 rounded-lg transition-all duration-200 border border-gray-600/50 hover:border-emerald-400/50"
                  >
                    {user.avatar_url ? (
                      <img
                        src={user.avatar_url}
                        alt={user.full_name || user.username}
                        className="w-6 h-6 rounded-full object-cover border border-gray-200 dark:border-gray-600"
                        onError={(e) => {
                          // Fallback to default avatar if image fails to load
                          const target = e.target as HTMLImageElement;
                          target.style.display = 'none';
                          target.nextElementSibling?.classList.remove('hidden');
                        }}
                      />
                    ) : null}
                    <User className={`w-4 h-4 ${user.avatar_url ? 'hidden' : ''}`} />
                    <span>{user.full_name || user.username || user.email}</span>
                    {showProfileDropdown ? (
                      <ChevronUp className="w-4 h-4" />
                    ) : (
                      <ChevronDown className="w-4 h-4" />
                    )}
                  </button>

                  {/* Profile Dropdown Menu */}
                  {showProfileDropdown && (
                    <div className="absolute right-0 mt-2 w-64 bg-gray-800/95 backdrop-blur-xl rounded-xl shadow-2xl border border-gray-700/50 z-50">
                      <div className="p-4 border-b border-gray-700/50">
                        <div className="flex items-center space-x-3">
                          {user.avatar_url ? (
                            <img
                              src={user.avatar_url}
                              alt={user.full_name || user.username}
                              className="w-10 h-10 rounded-full object-cover border-2 border-emerald-400/50"
                              onError={(e) => {
                                // Fallback to default avatar if image fails to load
                                const target = e.target as HTMLImageElement;
                                target.style.display = 'none';
                                target.nextElementSibling?.classList.remove('hidden');
                              }}
                            />
                          ) : null}
                          <div className={`w-10 h-10 bg-gradient-to-br from-emerald-400 to-blue-500 rounded-full flex items-center justify-center ${user.avatar_url ? 'hidden' : ''}`}>
                            <User className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <p className="font-medium text-white">
                              {user.full_name || user.username}
                            </p>
                            <p className="text-sm text-gray-300">
                              {user.email}
                            </p>
                            {user.oauth_providers && user.oauth_providers.length > 0 && (
                              <div className="flex items-center space-x-1 mt-1">
                                {user.oauth_providers.map((provider) => (
                                  <span
                                    key={provider}
                                    className="px-2 py-1 text-xs bg-emerald-500/20 text-emerald-300 rounded-full capitalize border border-emerald-500/30"
                                  >
                                    {provider}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className="p-2">
                        <a
                          href="/analytics"
                          className="w-full flex items-center px-3 py-2 text-sm text-gray-300 hover:text-emerald-400 hover:bg-gray-700/50 rounded-lg transition-all duration-200"
                        >
                          <BarChart3 className="w-4 h-4 mr-3" />
                          Analytics
                        </a>
                        <button
                          onClick={handleAccountManager}
                          className="w-full flex items-center px-3 py-2 text-sm text-gray-300 hover:text-emerald-400 hover:bg-gray-700/50 rounded-lg transition-all duration-200"
                        >
                          <Settings className="w-4 h-4 mr-3" />
                          Account Settings
                        </button>
                        <button
                          onClick={handleSignOut}
                          className="w-full flex items-center px-3 py-2 text-sm text-red-400 hover:text-red-300 hover:bg-red-500/20 rounded-lg transition-all duration-200"
                        >
                          <LogOut className="w-4 h-4 mr-3" />
                          Sign Out
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <a
                  href="/auth/login"
                  className="px-6 py-2 text-sm font-medium text-white bg-gradient-to-r from-emerald-500 to-blue-500 hover:from-emerald-600 hover:to-blue-600 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  Sign In
                </a>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Account Manager Modal */}
      {showAccountManager && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800/95 backdrop-blur-xl rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-700/50">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-white">
                  Account Settings
                </h2>
                <button
                  onClick={handleAccountManager}
                  className="text-gray-400 hover:text-emerald-400 transition-colors duration-200"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              {user && <UserAccountManager userProfile={user} />}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
