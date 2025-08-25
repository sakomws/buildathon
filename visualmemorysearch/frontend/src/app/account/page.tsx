'use client';

import React, { useState, useEffect } from 'react';
import { User, Link, Unlink, RefreshCw, AlertCircle, CheckCircle, Trash, Trash2, UserX, Settings, Shield, Key, Database, Bell, Download, Eye, EyeOff, Save, Edit, X } from 'lucide-react';
import UserAccountManager from '@/components/UserAccountManager';

export default function AccountSettingsPage() {
  const [userProfile, setUserProfile] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('profile');
  const [showOpenAIKey, setShowOpenAIKey] = useState(false);
  const [openAIKey, setOpenAIKey] = useState('');
  const [isEditingKey, setIsEditingKey] = useState(false);

  useEffect(() => {
    loadUserProfile();
    loadOpenAIKey();
  }, []);

  const loadUserProfile = async () => {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) {
        window.location.href = '/auth/login';
        return;
      }

      const response = await fetch('/api/auth/profile', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const profile = await response.json();
        setUserProfile(profile);
      } else {
        console.error('Failed to load user profile');
      }
    } catch (error) {
      console.error('Failed to load user profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadOpenAIKey = async () => {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) return;

      const response = await fetch('/api/admin/get-openai-key', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setOpenAIKey(data.openai_key || '');
      }
    } catch (error) {
      console.error('Failed to load OpenAI key:', error);
    }
  };

  const saveOpenAIKey = async () => {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) return;

      const response = await fetch('/api/admin/update-openai-key', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ api_key: openAIKey })
      });

      if (response.ok) {
        setIsEditingKey(false);
        alert('OpenAI key saved successfully!');
      } else {
        alert('Failed to save OpenAI key');
      }
    } catch (error) {
      console.error('Failed to save OpenAI key:', error);
      alert('Failed to save OpenAI key');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading account settings...</p>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'profile', name: 'Profile', icon: User },
    { id: 'security', name: 'Security', icon: Shield },
    { id: 'data', name: 'Data Management', icon: Database },
    { id: 'integrations', name: 'Integrations', icon: Key }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-xl border-b border-gray-200/50 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Account Settings
              </h1>
              <p className="text-gray-600 mt-1">Manage your account, security, and preferences</p>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => window.history.back()}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                ← Back
              </button>
              <button
                onClick={() => window.location.href = '/dashboard'}
                className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg hover:from-blue-600 hover:to-purple-600 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                Dashboard
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Tab Navigation */}
        <div className="mb-8">
          <div className="flex space-x-1 bg-white/60 backdrop-blur-sm rounded-xl p-1 border border-gray-200/50">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-white text-blue-600 shadow-lg'
                      : 'text-gray-600 hover:text-gray-800 hover:bg-white/50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.name}
                </button>
              );
            })}
          </div>
        </div>

        {/* Tab Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-3">
            {activeTab === 'profile' && (
              <div className="space-y-6">
                <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl border border-gray-200/50 p-8">
                  <div className="flex items-center justify-between mb-8">
                    <div>
                      <h2 className="text-2xl font-semibold text-gray-800 flex items-center gap-3">
                        <div className="p-3 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg">
                          <User className="w-6 h-6 text-white" />
                        </div>
                        Account Management
                      </h2>
                      <p className="text-gray-600 mt-2">Manage your profile information and account settings</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                        Active Account
                      </span>
                    </div>
                  </div>
                  
                  {/* Account Overview Card */}
                  <div className="mb-8 p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-200">
                    <div className="flex items-center gap-4">
                      <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
                        {userProfile?.avatar_url ? (
                          <img 
                            src={userProfile.avatar_url} 
                            alt="Profile" 
                            className="w-16 h-16 rounded-full object-cover"
                          />
                        ) : (
                          <User className="w-8 h-8 text-white" />
                        )}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-xl font-semibold text-gray-800">
                          {userProfile?.full_name || userProfile?.username || 'User'}
                        </h3>
                        <p className="text-gray-600">{userProfile?.email || 'No email provided'}</p>
                        <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                          <span>Member since {userProfile?.created_at ? new Date(userProfile.created_at).toLocaleDateString() : 'N/A'}</span>
                          <span>•</span>
                          <span>Last login {userProfile?.last_login ? new Date(userProfile.last_login).toLocaleDateString() : 'N/A'}</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-blue-600">Pro</div>
                        <div className="text-sm text-gray-500">Plan</div>
                      </div>
                    </div>
                  </div>
                  
                  <UserAccountManager userProfile={userProfile} />
                </div>
              </div>
            )}

            {activeTab === 'security' && (
              <div className="space-y-6">
                <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl border border-gray-200/50 p-8">
                  <div className="flex items-center justify-between mb-8">
                    <div>
                      <h2 className="text-2xl font-semibold text-gray-800 flex items-center gap-3">
                        <div className="p-3 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl shadow-lg">
                          <Shield className="w-6 h-6 text-white" />
                        </div>
                        Security & Privacy
                      </h2>
                      <p className="text-gray-600 mt-2">Protect your account with advanced security features</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                        Secure
                      </span>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl border border-green-200 hover:shadow-lg transition-all duration-200 group">
                      <div className="flex items-start justify-between mb-4">
                        <div className="p-3 bg-green-100 rounded-lg group-hover:bg-green-200 transition-colors">
                          <Key className="w-6 h-6 text-green-600" />
                        </div>
                        <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                          Recommended
                        </span>
                      </div>
                      <h3 className="font-semibold text-green-800 mb-3 text-lg">Two-Factor Authentication</h3>
                      <p className="text-green-700 text-sm mb-4 leading-relaxed">
                        Add an extra layer of security to your account with TOTP authentication. Protect your data even if your password is compromised.
                      </p>
                      <div className="flex items-center gap-2 mb-4">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-sm text-green-600">Currently disabled</span>
                      </div>
                      <button className="w-full px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors shadow-md hover:shadow-lg font-medium">
                        Enable 2FA
                      </button>
                    </div>

                    <div className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-200 hover:shadow-lg transition-all duration-200 group">
                      <div className="flex items-start justify-between mb-4">
                        <div className="p-3 bg-blue-100 rounded-lg group-hover:bg-blue-200 transition-colors">
                          <Bell className="w-6 h-6 text-blue-600" />
                        </div>
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                          Active
                        </span>
                      </div>
                      <h3 className="font-semibold text-blue-800 mb-3 text-lg">Notification Preferences</h3>
                      <p className="text-blue-700 text-sm mb-4 leading-relaxed">
                        Manage your email and push notification settings. Stay informed about important account activities and updates.
                      </p>
                      <div className="flex items-center gap-2 mb-4">
                        <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                        <span className="text-sm text-blue-600">Email notifications enabled</span>
                      </div>
                      <button className="w-full px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors shadow-md hover:shadow-lg font-medium">
                        Configure Notifications
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'data' && (
              <div className="space-y-6">
                <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl border border-gray-200/50 p-8">
                  <div className="flex items-center justify-between mb-8">
                    <div>
                      <h2 className="text-2xl font-semibold text-gray-800 flex items-center gap-3">
                        <div className="p-3 bg-gradient-to-br from-purple-500 to-violet-600 rounded-xl shadow-lg">
                          <Database className="w-6 h-6 text-white" />
                        </div>
                        Data Management
                      </h2>
                      <p className="text-gray-600 mt-2">Control your data with enterprise-grade management tools</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
                        GDPR Compliant
                      </span>
                    </div>
                  </div>
                  
                  {/* Data Overview */}
                  <div className="mb-8 p-6 bg-gradient-to-br from-purple-50 to-violet-50 rounded-xl border border-purple-200">
                    <h3 className="text-lg font-semibold text-purple-800 mb-4">Data Overview</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="text-center p-4 bg-white/50 rounded-lg">
                        <div className="text-2xl font-bold text-purple-600">1.2 GB</div>
                        <div className="text-sm text-purple-700">Total Storage Used</div>
                      </div>
                      <div className="text-center p-4 bg-white/50 rounded-lg">
                        <div className="text-2xl font-bold text-purple-600">247</div>
                        <div className="text-sm text-purple-700">Screenshots Stored</div>
                      </div>
                      <div className="text-center p-4 bg-white/50 rounded-lg">
                        <div className="text-2xl font-bold text-purple-600">30 days</div>
                        <div className="text-sm text-purple-700">Data Retention</div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="p-6 bg-gradient-to-br from-purple-50 to-violet-50 rounded-xl border border-purple-200 hover:shadow-lg transition-all duration-200 group">
                      <div className="flex items-start justify-between mb-4">
                        <div className="p-3 bg-purple-100 rounded-lg group-hover:bg-purple-200 transition-colors">
                          <Download className="w-6 h-6 text-purple-600" />
                        </div>
                        <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium">
                          Available
                        </span>
                      </div>
                      <h3 className="font-semibold text-purple-800 mb-3 text-lg">Export Data</h3>
                      <p className="text-purple-700 text-sm mb-4 leading-relaxed">
                        Download all your data in a portable format. Includes screenshots, metadata, and search indexes in a structured format.
                      </p>
                      <div className="flex items-center gap-2 mb-4">
                        <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                        <span className="text-sm text-purple-600">Last export: Never</span>
                      </div>
                      <button className="w-full px-4 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors shadow-md hover:shadow-lg font-medium">
                        Export All Data
                      </button>
                    </div>

                    <div className="p-6 bg-gradient-to-br from-red-50 to-pink-50 rounded-xl border border-red-200 hover:shadow-lg transition-all duration-200 group">
                      <div className="flex items-start justify-between mb-4">
                        <div className="p-3 bg-red-100 rounded-lg group-hover:bg-red-200 transition-colors">
                          <Trash2 className="w-6 h-6 text-red-600" />
                        </div>
                        <span className="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-medium">
                          Destructive
                        </span>
                      </div>
                      <h3 className="font-semibold text-red-800 mb-3 text-lg">Delete All Data</h3>
                      <p className="text-red-700 text-sm mb-4 leading-relaxed">
                        Permanently delete all your screenshots and data. This action cannot be undone and will remove all stored content.
                      </p>
                      <div className="flex items-center gap-2 mb-4">
                        <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                        <span className="text-sm text-red-600">247 items will be deleted</span>
                      </div>
                      <button className="w-full px-4 py-3 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors shadow-md hover:shadow-lg font-medium">
                        Delete All Data
                      </button>
                    </div>

                    <div className="p-6 bg-gradient-to-br from-orange-50 to-amber-50 rounded-xl border border-orange-200 hover:shadow-lg transition-all duration-200 group">
                      <div className="flex items-start justify-between mb-4">
                        <div className="p-3 bg-orange-100 rounded-lg group-hover:bg-orange-200 transition-colors">
                          <UserX className="w-6 h-6 text-orange-600" />
                        </div>
                        <span className="px-2 py-1 bg-orange-100 text-orange-800 rounded-full text-xs font-medium">
                          Permanent
                        </span>
                      </div>
                      <h3 className="font-semibold text-orange-800 mb-3 text-lg">Delete Account</h3>
                      <p className="text-orange-700 text-sm mb-4 leading-relaxed">
                        Permanently delete your account and all associated data. This will remove your profile, data, and access to the service.
                      </p>
                      <div className="flex items-center gap-2 mb-4">
                        <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                        <span className="text-sm text-orange-600">Account will be permanently removed</span>
                      </div>
                      <button className="w-full px-4 py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors shadow-md hover:shadow-lg font-medium">
                        Delete Account
                      </button>
                    </div>

                    <div className="p-6 bg-gradient-to-br from-indigo-50 to-blue-50 rounded-xl border border-indigo-200 hover:shadow-lg transition-all duration-200 group">
                      <div className="flex items-start justify-between mb-4">
                        <div className="p-3 bg-indigo-100 rounded-lg group-hover:bg-indigo-200 transition-colors">
                          <Settings className="w-6 h-6 text-indigo-600" />
                        </div>
                        <span className="px-2 py-1 bg-indigo-100 text-indigo-800 rounded-full text-xs font-medium">
                          Advanced
                        </span>
                      </div>
                      <h3 className="font-semibold text-indigo-800 mb-3 text-lg">Data Settings</h3>
                      <p className="text-indigo-700 text-sm mb-4 leading-relaxed">
                        Configure data retention policies, backup schedules, and privacy settings for your account.
                      </p>
                      <div className="flex items-center gap-2 mb-4">
                        <div className="w-2 h-2 bg-indigo-500 rounded-full"></div>
                        <span className="text-sm text-indigo-600">30-day retention policy</span>
                      </div>
                      <button className="w-full px-4 py-3 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors shadow-md hover:shadow-lg font-medium">
                        Configure Settings
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'integrations' && (
              <div className="space-y-6">
                <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl border border-gray-200/50 p-8">
                  <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center gap-3">
                    <div className="p-2 bg-indigo-100 rounded-lg">
                      <Key className="w-6 h-6 text-indigo-600" />
                    </div>
                    API Integrations
                  </h2>
                  
                                     {/* OpenAI Configuration */}
                   <div className="p-6 bg-gradient-to-br from-indigo-50 to-blue-50 rounded-xl border border-indigo-200">
                     <h3 className="font-semibold text-indigo-800 mb-4 flex items-center gap-2">
                       <Key className="w-5 h-5" />
                       OpenAI API Key
                     </h3>
                     <p className="text-indigo-700 text-sm mb-4">
                       Configure your OpenAI API key for enhanced search capabilities
                     </p>
                     
                     <div className="space-y-4">
                       {/* Key Status */}
                       <div className="flex justify-between items-center p-3 bg-white/50 rounded-lg">
                         <span className="text-indigo-700 font-medium">Status:</span>
                         <span className={`font-bold px-3 py-1 rounded-full text-sm ${
                           openAIKey ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                         }`}>
                           {openAIKey ? 'Configured' : 'Not Set'}
                         </span>
                       </div>
                       
                                                {/* Key Display/Edit */}
                         <div className="relative">
                           <input
                             type={showOpenAIKey ? 'text' : 'password'}
                             value={openAIKey}
                             onChange={(e) => setOpenAIKey(e.target.value)}
                             placeholder={isEditingKey ? "sk-..." : "Click 'Edit Key' to configure"}
                             className={`w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent pr-20 ${
                               !isEditingKey ? 'bg-gray-100 cursor-not-allowed' : ''
                             }`}
                             disabled={!isEditingKey}
                           />
                         <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex gap-2">
                           <button
                             onClick={() => setShowOpenAIKey(!showOpenAIKey)}
                             className="p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-100"
                             title={showOpenAIKey ? 'Hide key' : 'Show key'}
                           >
                             {showOpenAIKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                           </button>
                           {!isEditingKey && openAIKey && (
                             <button
                               onClick={() => {
                                 if (confirm('Are you sure you want to delete your OpenAI API key?')) {
                                   setOpenAIKey('');
                                   saveOpenAIKey();
                                 }
                               }}
                               className="p-2 text-red-500 hover:text-red-700 rounded-lg hover:bg-red-50"
                               title="Delete key"
                             >
                               <Trash className="w-4 h-4" />
                             </button>
                           )}
                         </div>
                       </div>
                       
                       {/* Action Buttons */}
                       <div className="flex gap-3">
                         {isEditingKey ? (
                           <>
                             <button
                               onClick={saveOpenAIKey}
                               className="px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors flex items-center gap-2"
                             >
                               <Save className="w-4 h-4" />
                               Save Key
                             </button>
                             <button
                               onClick={() => {
                                 setIsEditingKey(false);
                                 loadOpenAIKey(); // Reset to original value
                               }}
                               className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors flex items-center gap-2"
                             >
                               <X className="w-4 h-4" />
                               Cancel
                             </button>
                           </>
                         ) : (
                           <button
                             onClick={() => setIsEditingKey(true)}
                             className="px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors flex items-center gap-2"
                           >
                             <Edit className="w-4 h-4" />
                             {openAIKey ? 'Edit Key' : 'Add Key'}
                           </button>
                         )}
                       </div>
                       
                       {/* Key Info */}
                       {openAIKey && (
                         <div className="text-sm text-indigo-600 bg-indigo-50 p-4 rounded-lg">
                           <p className="font-medium mb-2">Key Information:</p>
                           <ul className="space-y-1">
                             <li>• User-specific key (only you can see this)</li>
                             <li>• Used for enhanced search capabilities</li>
                             <li>• Stored securely on the server</li>
                             <li>• Automatically used for AI-powered features</li>
                           </ul>
                         </div>
                       )}
                     </div>
                   </div>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Stats */}
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl border border-gray-200/50 p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <Settings className="w-5 h-5 text-blue-500" />
                Account Status
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Status:</span>
                  <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                    Active
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Member since:</span>
                  <span className="text-gray-800 font-medium">
                    {userProfile?.created_at ? new Date(userProfile.created_at).toLocaleDateString() : 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Last login:</span>
                  <span className="text-gray-800 font-medium">
                    {userProfile?.last_login ? new Date(userProfile.last_login).toLocaleDateString() : 'N/A'}
                  </span>
                </div>
              </div>
            </div>

            {/* Help & Support */}
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl border border-gray-200/50 p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Help & Support</h3>
              <div className="space-y-3">
                <a href="/docs" className="flex items-center gap-2 text-blue-600 hover:text-blue-800 transition-colors p-2 rounded-lg hover:bg-blue-50">
                  📚 Documentation
                </a>
                <a href="/faq" className="flex items-center gap-2 text-blue-600 hover:text-blue-800 transition-colors p-2 rounded-lg hover:bg-blue-50">
                  ❓ FAQ
                </a>
                <a href="/support" className="flex items-center gap-2 text-blue-600 hover:text-blue-800 transition-colors p-2 rounded-lg hover:bg-blue-50">
                  🆘 Contact Support
                </a>
                <a href="/feedback" className="flex items-center gap-2 text-blue-600 hover:text-blue-800 transition-colors p-2 rounded-lg hover:bg-blue-50">
                  💬 Send Feedback
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
