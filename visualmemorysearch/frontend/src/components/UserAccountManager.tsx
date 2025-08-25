'use client';

import React, { useState, useEffect } from 'react';
import { User, Link, Unlink, RefreshCw, AlertCircle, CheckCircle, Trash, Trash2, UserX } from 'lucide-react';

interface UserAccountManagerProps {
  userProfile?: any; // Make userProfile optional
}

export default function UserAccountManager({ userProfile }: UserAccountManagerProps) {
  const [userAccounts, setUserAccounts] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [mergeEmail, setMergeEmail] = useState('');
  const [isMerging, setIsMerging] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'info'; text: string } | null>(null);
  const [isDeletingAllData, setIsDeletingAllData] = useState(false);
  const [isDeletingAccount, setIsDeletingAccount] = useState(false);

  useEffect(() => {
    loadUserAccounts();
  }, []);

  const getAuthToken = () => {
    return localStorage.getItem('access_token') || localStorage.getItem('auth_token');
  };

  const loadUserAccounts = async () => {
    try {
      setIsLoading(true);
      const token = getAuthToken();
      if (!token) return;

      const response = await fetch('/api/auth/user-accounts', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setUserAccounts(data);
      } else {
        console.error('Failed to load user accounts');
      }
    } catch (error) {
      console.error('Error loading user accounts:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMergeUsers = async () => {
    if (!mergeEmail.trim()) {
      setMessage({ type: 'error', text: 'Please enter an email address' });
      return;
    }

    try {
      setIsMerging(true);
      const token = getAuthToken();
      if (!token) return;

      const response = await fetch('/api/auth/merge-users', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: mergeEmail.trim() }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage({ type: 'success', text: data.message });
        setMergeEmail('');
        // Reload user accounts and profile
        await loadUserAccounts();
        // Trigger a page reload to update the user profile
        window.location.reload();
      } else {
        setMessage({ type: 'error', text: data.detail || 'Failed to merge users' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Network error occurred' });
    } finally {
      setIsMerging(false);
    }
  };

  const handleUnlinkOAuth = async (provider: string) => {
    try {
      const token = getAuthToken();
      if (!token) return;

      const response = await fetch(`/api/auth/unlink-oauth/${provider}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setMessage({ type: 'success', text: `Successfully unlinked ${provider} account` });
        await loadUserAccounts();
      } else {
        const data = await response.json();
        setMessage({ type: 'error', text: data.detail || `Failed to unlink ${provider} account` });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Network error occurred' });
    }
  };

  const deleteAllUserData = async () => {
    if (!confirm('⚠️ WARNING: This will permanently delete all your data. This action cannot be undone. Are you sure?')) return;
    if (!confirm('🔴 FINAL WARNING: Type "DELETE ALL" to confirm:')) return;

    try {
      setIsDeletingAllData(true);
      const token = getAuthToken();
      if (!token) {
        alert('No authentication token found. Please log in again.');
        return;
      }

      const response = await fetch('/api/admin/delete-all-user-data', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const result = await response.json();
        alert(`✅ All your data has been permanently deleted: ${result.message}`);
        window.location.reload();
      } else {
        throw new Error(`Failed to delete all data: ${response.status}`);
      }
    } catch (error) {
      console.error('Failed to delete all data:', error);
      alert('Failed to delete all data. Check console for details.');
    } finally {
      setIsDeletingAllData(false);
    }
  };

  const deleteUserAccount = async () => {
    if (!confirm('⚠️ WARNING: This will permanently delete your account. This action cannot be undone. Are you sure?')) return;
    if (!confirm('🔴 FINAL WARNING: Type "DELETE ACCOUNT" to confirm:')) return;

    try {
      setIsDeletingAccount(true);
      const token = getAuthToken();
      if (!token) {
        alert('No authentication token found. Please log in again.');
        return;
      }

      const response = await fetch('/api/admin/delete-user-account', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const result = await response.json();
        alert(`✅ Your account has been permanently deleted: ${result.message}`);
        localStorage.clear();
        sessionStorage.clear();
        window.location.href = '/auth/login';
      } else {
        throw new Error(`Failed to delete account: ${response.status}`);
      }
    } catch (error) {
      console.error('Failed to delete account:', error);
      alert('Failed to delete account. Check console for details.');
    } finally {
      setIsDeletingAccount(false);
    }
  };

  // Don't render if no user profile
  if (!userProfile) {
    return null;
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 mb-8">
      <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6 flex items-center">
        <User className="w-6 h-6 mr-3 text-blue-500" />
        Account Management
      </h2>

      {/* User Profile Information */}
      <div className="mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <h3 className="font-medium text-gray-900 dark:text-white mb-3">Profile Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
            <p className="text-sm text-gray-900 dark:text-white">{userProfile.email}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Username</label>
            <p className="text-sm text-gray-900 dark:text-white">{userProfile.username || 'Not set'}</p>
          </div>
          {/* SAFELY check for avatar_url before using it */}
          {userProfile && userProfile.avatar_url && (
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Avatar</label>
              <img 
                src={userProfile.avatar_url} 
                alt="User avatar" 
                className="w-16 h-16 rounded-full border-2 border-gray-300 dark:border-gray-600"
              />
            </div>
          )}
        </div>
      </div>

      {/* OAuth Accounts */}
      {userAccounts && (
        <div className="mb-6">
          <h3 className="font-medium text-gray-900 dark:text-white mb-3">Connected Accounts</h3>
          <div className="space-y-3">
            {userAccounts.oauth_accounts?.map((account: any) => (
              <div key={account.provider} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center mr-3">
                    <span className="text-white text-sm font-medium">{account.provider.charAt(0).toUpperCase()}</span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">{account.provider}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{account.email}</p>
                  </div>
                </div>
                <button
                  onClick={() => handleUnlinkOAuth(account.provider)}
                  className="px-3 py-1 text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center"
                >
                  <Unlink className="w-4 h-4 mr-1" />
                  Unlink
                </button>
              </div>
            ))}
            {(!userAccounts.oauth_accounts || userAccounts.oauth_accounts.length === 0) && (
              <p className="text-gray-600 dark:text-gray-400 text-sm">No OAuth accounts connected</p>
            )}
          </div>
        </div>
      )}

      {/* Merge Users */}
      <div className="mb-6">
        <h3 className="font-medium text-gray-900 dark:text-white mb-3">Merge User Accounts</h3>
        <div className="flex gap-2">
          <input
            type="email"
            placeholder="Enter email to merge"
            value={mergeEmail}
            onChange={(e) => setMergeEmail(e.target.value)}
            className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
          <button
            onClick={handleMergeUsers}
            disabled={isMerging || !mergeEmail.trim()}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg transition-colors disabled:cursor-not-allowed flex items-center"
          >
            {isMerging ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Merging...
              </>
            ) : (
              <>
                <Link className="w-4 h-4 mr-2" />
                Merge
              </>
            )}
          </button>
        </div>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
          Merge another user account with your current account to combine their data.
        </p>
      </div>

      {/* Data Management Section */}
      <div className="mb-6">
        <h3 className="font-medium text-gray-900 dark:text-white mb-6 flex items-center">
          <Trash className="w-5 h-5 mr-2 text-red-400" />
          Data Management
        </h3>

        <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-6">
          <div className="flex items-start space-x-4">
            <AlertCircle className="w-6 h-6 text-red-400 mt-1 flex-shrink-0" />
            <div className="flex-1">
              <h5 className="text-lg font-semibold text-red-300 mb-2">Danger Zone</h5>
              <p className="text-sm text-gray-300 mb-4">
                These actions are irreversible and will permanently delete your data. Use with extreme caution.
              </p>

              <div className="space-y-4">
                {/* Delete All Data */}
                <div className="flex items-center justify-between p-4 bg-red-900/50 rounded-lg border border-red-700/50">
                  <div>
                    <h6 className="font-medium text-red-200">Delete All My Data</h6>
                    <p className="text-xs text-gray-400">Permanently delete everything: screenshots, search index, user profile, and all settings</p>
                  </div>
                  <button
                    onClick={deleteAllUserData}
                    disabled={isDeletingAllData}
                    className="px-4 py-2 bg-red-700 hover:bg-red-800 disabled:bg-red-800/50 text-white rounded-lg transition-colors text-sm disabled:cursor-not-allowed flex items-center"
                  >
                    {isDeletingAllData ? (
                      <>
                        <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-2"></div>
                        Deleting...
                      </>
                    ) : (
                      <>
                        <Trash2 className="w-3 h-3 mr-2" />
                        Delete All Data
                      </>
                    )}
                  </button>
                </div>

                {/* Delete Account */}
                <div className="flex items-center justify-between p-4 bg-black/50 rounded-lg border border-red-800/50">
                  <div>
                    <h6 className="font-medium text-red-100">Delete My Account</h6>
                    <p className="text-xs text-gray-400">Permanently delete your entire account from the system. This will remove you completely.</p>
                  </div>
                  <button
                    onClick={deleteUserAccount}
                    disabled={isDeletingAccount}
                    className="px-4 py-2 bg-black hover:bg-gray-900 disabled:bg-gray-800 text-white rounded-lg transition-colors text-sm disabled:cursor-not-allowed flex items-center border border-red-800"
                  >
                    {isDeletingAccount ? (
                      <>
                        <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-2"></div>
                        Deleting...
                      </>
                    ) : (
                      <>
                        <UserX className="w-3 h-3 mr-2" />
                        Delete Account
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Message Display */}
      {message && (
        <div className={`p-3 rounded-lg ${
          message.type === 'success' 
            ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200' 
            : message.type === 'error'
            ? 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-200'
            : 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200'
        }`}>
          <div className="flex items-center">
            {message.type === 'success' ? (
              <CheckCircle className="w-4 h-4 mr-2" />
            ) : message.type === 'error' ? (
              <AlertCircle className="w-4 h-4 mr-2" />
            ) : (
              <AlertCircle className="w-4 h-4 mr-2" />
            )}
            {message.text}
          </div>
        </div>
      )}
    </div>
  );
}
