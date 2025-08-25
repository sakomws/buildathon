'use client';

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { 
  Search, 
  Upload, 
  Download, 
  Trash, 
  FolderOpen, 
  Filter, 
  RefreshCw, 
  CheckCircle, 
  ArrowUp, 
  ArrowDown, 
  ChevronLeft, 
  ChevronRight,
  Eye,
  X,
  Database,
  FileText,
  Folder,
  File,
  EyeOff,
  Trash2,
  Building2,
  Shield,
  Users
} from 'lucide-react';
import { SearchQuery, SearchResult, ScreenshotInfo } from '@/types/api';
import { searchScreenshots, getScreenshots } from '@/lib/api';
import { Settings, Zap, AlertCircle, Key } from 'lucide-react';
import { useAuth } from '@/components/Auth/AuthProvider';

export default function Dashboard() {
  const { user, login } = useAuth();
  
  // State variables
  const [screenshots, setScreenshots] = useState<ScreenshotInfo[]>([]);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState<'text' | 'visual' | 'combined'>('combined');
  const [maxResults, setMaxResults] = useState(50);
  const [currentPage, setCurrentPage] = useState(1);
  const [screenshotsPerPage] = useState(12);
  const [totalPages, setTotalPages] = useState(1);
  const [isSelectMode, setIsSelectMode] = useState(false);
  const [selectedScreenshots, setSelectedScreenshots] = useState<Set<string>>(new Set());
  const [showAdminPanel, setShowAdminPanel] = useState(false);
  const [systemStatus, setSystemStatus] = useState<any>(null);
  const [isGeneratingTestData, setIsGeneratingTestData] = useState(false);
  const [isRebuildingIndex, setIsRebuildingIndex] = useState(false);
  const [isDeletingAllData, setIsDeletingAllData] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [openAIKey, setOpenAIKey] = useState('');
  const [showOpenAIKey, setShowOpenAIKey] = useState(false);
  const [isEditingOpenAIKey, setIsEditingOpenAIKey] = useState(false);
  const [isDownloadingZip, setIsDownloadingZip] = useState(false);
  const [sortBy, setSortBy] = useState<'name' | 'date' | 'size' | 'extension'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [filterExtension, setFilterExtension] = useState<string>('all');
  const [filterDateRange, setFilterDateRange] = useState<string>('all');
  const [filterSizeRange, setFilterSizeRange] = useState<string>('all');
  const [searchFilter, setSearchFilter] = useState<string>('');
  const [showFilters, setShowFilters] = useState(false);
  
  // View modal state
  const [viewModalOpen, setViewModalOpen] = useState(false);
  const [selectedScreenshot, setSelectedScreenshot] = useState<ScreenshotInfo | null>(null);
  
  // Organization management state
  const [showOrgManagement, setShowOrgManagement] = useState(false);
  const [newOrgName, setNewOrgName] = useState('');
  const [newOrgDescription, setNewOrgDescription] = useState('');
  const [newUserEmail, setNewUserEmail] = useState('');
  const [newUserRole, setNewUserRole] = useState('user');
  
  // Login form state
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  
  // Refs
  const fileInputRef = useRef<HTMLInputElement>(null);
  const folderInputRef = useRef<HTMLInputElement>(null);
  
  // Load initial data
  useEffect(() => {
    loadScreenshots();
    loadSystemStatus();
    loadOpenAIKey();
  }, []);

  // Load screenshots
  const loadScreenshots = async () => {
    try {
      setIsLoading(true);
      const data = await getScreenshots();
      // Handle both array and object responses
      if (Array.isArray(data)) {
        setScreenshots(data);
        setTotalPages(1);
      } else if (data && typeof data === 'object') {
        setScreenshots(data.screenshots || data);
        setTotalPages(Math.ceil((data.total || data.length || 0) / screenshotsPerPage));
      } else {
        setScreenshots([]);
        setTotalPages(1);
      }
    } catch (error) {
      console.error('Failed to load screenshots:', error);
      setScreenshots([]);
      setTotalPages(1);
    } finally {
      setIsLoading(false);
    }
  };

  // Load system status
  const loadSystemStatus = async () => {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) return;

      const response = await fetch('/api/admin/status', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const status = await response.json();
        setSystemStatus(status);
      }
    } catch (error) {
      console.error('Failed to load system status:', error);
    }
  };

  // Search functionality
  const handleSearch = async (query: string) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    try {
      setIsLoading(true);
      const results = await searchScreenshots({ 
        query, 
        search_type: 'combined', 
        max_results: 50 
      });
      setSearchResults(Array.isArray(results) ? results : []);
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  // Upload functionality
  const handleFileUpload = async (files: FileList | File[]) => {
    if (!files.length) return;

    setIsUploading(true);
    setUploadProgress(0);

    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) {
        alert('No authentication token found. Please log in again.');
        return;
      }

      // Upload files one by one since the backend expects single file uploads
      const uploadPromises = Array.from(files).map(async (file, index) => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/upload', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        });

        if (response.ok) {
          // Update progress
          setUploadProgress(((index + 1) / files.length) * 100);
          return { success: true, filename: file.name };
        } else {
          const error = await response.text();
          return { success: false, filename: file.name, error };
        }
      });

      const results = await Promise.all(uploadPromises);
      const successful = results.filter(r => r.success);
      const failed = results.filter(r => !r.success);

      if (successful.length > 0) {
        alert(`${successful.length} file(s) uploaded successfully!`);
        loadScreenshots();
      }
      
      if (failed.length > 0) {
        alert(`${failed.length} file(s) failed to upload. Check console for details.`);
        console.error('Failed uploads:', failed);
      }

      setSelectedFiles([]);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  // Drag and drop handlers
  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files);
    }
  };

  // File input handlers
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      handleFileUpload(e.target.files);
    }
  };

  const handleFolderSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      handleFileUpload(e.target.files);
    }
  };

  // Delete screenshot
  const handleDeleteScreenshot = async (filename: string) => {
    if (!confirm('Are you sure you want to delete this screenshot?')) return;
    
    try {
      const response = await fetch(`/api/screenshots/${filename}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      if (response.ok) {
        alert('Screenshot deleted successfully!');
        loadScreenshots();
      } else {
        alert('Error deleting screenshot. Please try again.');
      }
    } catch (error) {
      console.error('Error deleting screenshot:', error);
      alert('Error deleting screenshot. Please try again.');
    }
  };

  const viewScreenshot = (screenshot: ScreenshotInfo) => {
    setSelectedScreenshot(screenshot);
    setViewModalOpen(true);
  };

  const closeViewModal = () => {
    setViewModalOpen(false);
    setSelectedScreenshot(null);
  };

  // Admin functions
  const generateTestData = async () => {
    try {
      setIsGeneratingTestData(true);
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) {
        alert('No authentication token found. Please log in again.');
        return;
      }

      const response = await fetch('/api/generate-test-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ count: 10 })
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Test data generated: ${result.message}`);
        loadScreenshots();
        loadSystemStatus();
      } else {
        const errorText = await response.text();
        console.error('Failed to generate test data:', response.status, response.statusText, errorText);
        alert('Failed to generate test data. Check console for details.');
      }
    } catch (error) {
      console.error('Generate test data error:', error);
      alert('Failed to generate test data. Please try again.');
    } finally {
      setIsGeneratingTestData(false);
    }
  };

  const rebuildIndex = async () => {
    try {
      setIsRebuildingIndex(true);
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) {
        alert('No authentication token found. Please log in again.');
        return;
      }

      console.log('Rebuilding index...');
      const response = await fetch('/api/rebuild-index', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      console.log('Rebuild index response:', response.status, response.statusText);

      if (response.ok) {
        const result = await response.json();
        console.log('Rebuild index success:', result);
        alert('Search index rebuilt successfully!');
        loadSystemStatus();
      } else {
        const errorText = await response.text();
        console.error('Failed to rebuild index:', response.status, response.statusText, errorText);
        alert(`Failed to rebuild index (${response.status}): ${errorText}`);
      }
    } catch (error) {
      console.error('Rebuild index error:', error);
      alert('Failed to rebuild index. Please try again.');
    } finally {
      setIsRebuildingIndex(false);
    }
  };

  const deleteAllData = async () => {
    if (!confirm('Are you sure you want to delete ALL your data? This action cannot be undone!')) return;

    try {
      setIsDeletingAllData(true);
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) {
        alert('No authentication token found. Please log in again.');
        return;
      }

      console.log('Deleting all user data...');
      const response = await fetch('/api/admin/delete-all-user-data', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      console.log('Delete all data response:', response.status, response.statusText);

      if (response.ok) {
        const result = await response.json();
        console.log('Delete all data success:', result);
        alert('All data deleted successfully!');
        loadScreenshots();
        loadSystemStatus();
      } else {
        const errorText = await response.text();
        console.error('Failed to delete all data:', response.status, response.statusText, errorText);
        alert(`Failed to delete all data (${response.status}): ${errorText}`);
      }
    } catch (error) {
      console.error('Delete all data error:', error);
      alert('Failed to delete all data. Please try again.');
    } finally {
      setIsDeletingAllData(false);
    }
  };

  // OpenAI Key Management
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
      if (!token) {
        alert('No authentication token found. Please log in again.');
        return;
      }

      const response = await fetch('/api/admin/update-openai-key', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ api_key: openAIKey })
      });

      if (response.ok) {
        setIsEditingOpenAIKey(false);
        alert('OpenAI key saved successfully!');
      } else {
        alert('Failed to save OpenAI key');
      }
    } catch (error) {
      console.error('Failed to save OpenAI key:', error);
      alert('Failed to save OpenAI key');
    }
  };

  // Multi-select functions
  const toggleSelectMode = () => {
    setIsSelectMode(!isSelectMode);
    if (isSelectMode) {
      setSelectedScreenshots(new Set());
    }
  };

  const toggleScreenshotSelection = (filename: string) => {
    const newSelected = new Set(selectedScreenshots);
    if (newSelected.has(filename)) {
      newSelected.delete(filename);
    } else {
      newSelected.add(filename);
    }
    setSelectedScreenshots(newSelected);
  };

  const selectAllScreenshots = () => {
    const allFilenames = screenshots.map(s => s.filename);
    setSelectedScreenshots(new Set(allFilenames));
  };

  const clearSelection = () => {
    setSelectedScreenshots(new Set());
  };

  const downloadSingleImage = async (filename: string) => {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) {
        alert('No authentication token found. Please log in again.');
        return;
      }

      const response = await fetch(`/api/screenshots/${filename}/download`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        alert(`Downloaded ${filename}`);
      } else {
        const errorText = await response.text();
        console.error('Failed to download image:', response.status, response.statusText, errorText);
        alert('Failed to download image');
      }
    } catch (error) {
      console.error('Download error:', error);
      alert('Failed to download image');
    }
  };

  const downloadSelectedAsZip = async () => {
    if (selectedScreenshots.size === 0) {
      alert('Please select screenshots to download');
      return;
    }

    try {
      setIsDownloadingZip(true);
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) {
        alert('No authentication token found. Please log in again.');
        return;
      }

      const response = await fetch('/api/screenshots/download-zip', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filenames: Array.from(selectedScreenshots) })
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `screenshots-${new Date().toISOString().split('T')[0]}.zip`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        alert(`Downloaded ${selectedScreenshots.size} screenshots as ZIP`);
      } else {
        const errorText = await response.text();
        console.error('Failed to download ZIP:', response.status, response.statusText, errorText);
        alert('Failed to download ZIP. Check console for details.');
      }
    } catch (error) {
      console.error('Download ZIP error:', error);
      alert('Failed to download ZIP. Please try again.');
    } finally {
      setIsDownloadingZip(false);
    }
  };

  const deleteSelectedScreenshots = async () => {
    if (selectedScreenshots.size === 0) {
      alert('Please select screenshots to delete');
      return;
    }

    if (!confirm(`Are you sure you want to delete ${selectedScreenshots.size} selected screenshot(s)?`)) {
      return;
    }

    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('auth_token');
      if (!token) {
        alert('No authentication token found. Please log in again.');
        return;
      }

      const deletePromises = Array.from(selectedScreenshots).map(async (filename) => {
        const response = await fetch(`/api/screenshots/${filename}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        return { filename, success: response.ok };
      });

      const results = await Promise.all(deletePromises);
      const successful = results.filter(r => r.success);
      const failed = results.filter(r => !r.success);

      if (successful.length > 0) {
        alert(`Successfully deleted ${successful.length} screenshot(s)`);
        setSelectedScreenshots(new Set());
        loadScreenshots();
      }
      
      if (failed.length > 0) {
        alert(`${failed.length} screenshot(s) failed to delete. Check console for details.`);
        console.error('Failed deletions:', failed);
      }
    } catch (error) {
      console.error('Delete selected error:', error);
      alert('Failed to delete selected screenshots. Please try again.');
    }
  };

  // Filtering and Sorting Functions
  const getFileExtension = (filename: string): string => {
    return filename.split('.').pop()?.toLowerCase() || '';
  };

  const getFileSize = (screenshot: ScreenshotInfo): number => {
    return screenshot.metadata?.file_size || 0;
  };

  const getFileDate = (screenshot: ScreenshotInfo): Date => {
    return new Date(screenshot.metadata?.created_at || screenshot.timestamp || 0);
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFilteredAndSortedScreenshots = () => {
    let filtered = [...screenshots];

    // Apply search filter
    if (searchFilter) {
      filtered = filtered.filter(screenshot => 
        screenshot.filename.toLowerCase().includes(searchFilter.toLowerCase()) ||
        screenshot.text_content?.toLowerCase().includes(searchFilter.toLowerCase())
      );
    }

    // Apply extension filter
    if (filterExtension !== 'all') {
      filtered = filtered.filter(screenshot => 
        getFileExtension(screenshot.filename) === filterExtension
      );
    }

    // Apply date range filter
    if (filterDateRange !== 'all') {
      const now = new Date();
      const fileDate = getFileDate(filtered[0]);
      const daysDiff = Math.floor((now.getTime() - fileDate.getTime()) / (1000 * 60 * 60 * 24));
      
      switch (filterDateRange) {
        case 'today':
          filtered = filtered.filter(screenshot => {
            const date = getFileDate(screenshot);
            return date.toDateString() === now.toDateString();
          });
          break;
        case 'week':
          filtered = filtered.filter(screenshot => {
            const date = getFileDate(screenshot);
            return daysDiff <= 7;
          });
          break;
        case 'month':
          filtered = filtered.filter(screenshot => {
            const date = getFileDate(screenshot);
            return daysDiff <= 30;
          });
          break;
        case 'year':
          filtered = filtered.filter(screenshot => {
            const date = getFileDate(screenshot);
            return daysDiff <= 365;
          });
          break;
      }
    }

    // Apply size range filter
    if (filterSizeRange !== 'all') {
      const sizeInBytes = (size: string) => {
        const num = parseInt(size);
        if (size.includes('MB')) return num * 1024 * 1024;
        if (size.includes('KB')) return num * 1024;
        return num;
      };

      filtered = filtered.filter(screenshot => {
        const fileSize = getFileSize(screenshot);
        switch (filterSizeRange) {
          case 'small':
            return fileSize < 1024 * 1024; // < 1MB
          case 'medium':
            return fileSize >= 1024 * 1024 && fileSize < 5 * 1024 * 1024; // 1MB - 5MB
          case 'large':
            return fileSize >= 5 * 1024 * 1024; // > 5MB
          default:
            return true;
        }
      });
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aValue: any, bValue: any;
      
      switch (sortBy) {
        case 'name':
          aValue = a.filename.toLowerCase();
          bValue = b.filename.toLowerCase();
          break;
        case 'date':
          aValue = getFileDate(a);
          bValue = getFileDate(b);
          break;
        case 'size':
          aValue = getFileSize(a);
          bValue = getFileSize(b);
          break;
        case 'extension':
          aValue = getFileExtension(a.filename);
          bValue = getFileExtension(b.filename);
          break;
        default:
          return 0;
      }

      if (sortOrder === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
      }
    });

    return filtered;
  };

  const clearAllFilters = () => {
    setSearchFilter('');
    setFilterExtension('all');
    setFilterDateRange('all');
    setFilterSizeRange('all');
    setSortBy('date');
    setSortOrder('desc');
  };

  const getUniqueExtensions = () => {
    const extensions = screenshots.map(s => getFileExtension(s.filename));
    return ['all', ...Array.from(new Set(extensions)).filter(ext => ext)];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Visual Memory Search Dashboard
            </h1>
            <p className="text-gray-600 mt-2">Search and manage your visual content</p>
          </div>
          <button
            onClick={() => setShowAdminPanel(!showAdminPanel)}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg hover:from-blue-600 hover:to-purple-600 transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            <Settings className="w-5 h-5" />
            {showAdminPanel ? 'Hide Admin Panel' : 'Show Admin Panel'}
          </button>
        </div>

        {/* Simple Login Form */}
        {!user && (
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-blue-800 mb-2">🔐 Quick Login (No OAuth Required)</h3>
            <div className="space-y-3">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <input
                  type="text"
                  placeholder="Username (default: admin)"
                  className="px-3 py-2 border border-blue-200 rounded-md text-gray-900 bg-white"
                  value={loginUsername}
                  onChange={(e) => setLoginUsername(e.target.value)}
                />
                <input
                  type="password"
                  placeholder="Password (default: admin123)"
                  className="px-3 py-2 border border-blue-200 rounded-md text-gray-900 bg-white"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                />
              </div>
              <button
                onClick={async () => {
                  try {
                    const response = await fetch('/api/dev/simple-login', {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json'
                      },
                      body: JSON.stringify({
                        username: loginUsername || 'admin',
                        password: loginPassword || 'admin123'
                      })
                    });
                    
                    if (response.ok) {
                      const result = await response.json();
                      console.log('Login successful:', result);
                      
                      // Use the AuthProvider's login method
                      await login(result.access_token);
                      
                      alert('Login successful! You should now have admin access.');
                      // No need to reload - the AuthProvider will handle the state
                    } else {
                      const error = await response.text();
                      alert(`Login failed: ${error}`);
                    }
                  } catch (error) {
                    alert(`Error: ${error}`);
                  }
                }}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium"
              >
                🚀 Quick Login
              </button>
              <p className="text-xs text-blue-600">
                This creates a test account if none exists. First user automatically becomes admin!
              </p>
            </div>
          </div>
        )}

        {/* Debug Info - Temporary */}
        {user && (
          <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <h3 className="font-semibold text-yellow-800 mb-2">🔍 Debug Info</h3>
            <div className="text-sm text-yellow-700 space-y-1">
              <p><strong>User ID:</strong> {user.id}</p>
              <p><strong>Username:</strong> {user.username}</p>
              <p><strong>Is Admin:</strong> {user.is_admin ? '✅ Yes' : '❌ No'}</p>
              <p><strong>Admin Panel Visible:</strong> {showAdminPanel && user?.is_admin ? '✅ Yes' : '❌ No'}</p>
              <p><strong>Show Admin Panel State:</strong> {showAdminPanel ? '✅ Yes' : '❌ No'}</p>
            </div>
            <div className="mt-3 p-3 bg-yellow-100 rounded-md">
              <p className="font-medium text-yellow-800">Quick Admin Access:</p>
              <div className="mt-2 space-y-2">
                <button
                  onClick={async () => {
                    try {
                      const token = localStorage.getItem('accessToken');
                      if (!token) {
                        alert('No access token found. Please login again.');
                        return;
                      }
                      
                      console.log('Making user admin...');
                      const response = await fetch('/api/dev/make-admin', {
                        method: 'POST',
                        headers: {
                          'Authorization': `Bearer ${token}`,
                          'Content-Type': 'application/json'
                        }
                      });
                      
                      console.log('Response status:', response.status);
                      
                      if (response.ok) {
                        const result = await response.json();
                        console.log('Admin access granted:', result);
                        alert('Admin access granted! Refreshing page...');
                        window.location.reload();
                      } else {
                        const error = await response.text();
                        console.error('Failed to get admin access:', error);
                        alert(`Failed to get admin access: ${error}`);
                      }
                    } catch (error) {
                      console.error('Error making user admin:', error);
                      alert(`Error: ${error}`);
                    }
                  }}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors text-sm font-medium"
                >
                  🚀 Make Me Admin (Click Here)
                </button>
                
                <button
                  onClick={async () => {
                    try {
                      const token = localStorage.getItem('accessToken');
                      if (!token) {
                        alert('No access token found. Please login again.');
                        return;
                      }
                      
                      console.log('Promoting first user to admin...');
                      const response = await fetch('/api/dev/promote-first-user', {
                        method: 'POST',
                        headers: {
                          'Authorization': `Bearer ${token}`,
                          'Content-Type': 'application/json'
                        }
                      });
                      
                      console.log('Response status:', response.status);
                      
                      if (response.ok) {
                        const result = await response.json();
                        console.log('First user promoted:', result);
                        alert('First user promoted to admin! Refreshing page...');
                        window.location.reload();
                      } else {
                        const error = await response.text();
                        console.error('Failed to promote first user:', error);
                        alert(`Failed to promote first user: ${error}`);
                      }
                    } catch (error) {
                      console.error('Error promoting first user:', error);
                      alert(`Error: ${error}`);
                    }
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  👑 Promote First User to Admin
                </button>
                
                <p className="text-xs text-yellow-600">
                  Try the blue button first if you're the first user, then the green button
                </p>
              </div>
            </div>
          </div>
        )}



        {/* Admin Panel */}
        {showAdminPanel && user?.is_admin && (
          <div className="mb-8 p-6 bg-white rounded-xl shadow-lg border border-gray-200">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <Zap className="w-6 h-6 text-blue-500" />
              Admin Panel
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* System Status */}
              <div className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
                <h3 className="font-semibold text-blue-800 mb-3 flex items-center gap-2">
                  <Database className="w-5 h-5" />
                  System Status
                </h3>
                {systemStatus ? (
                  <div className="space-y-3">
                    <div className="flex justify-between items-center p-2 bg-white/50 rounded-md">
                      <span className="text-blue-700 font-medium">Total Screenshots:</span>
                      <span className="font-bold text-blue-800 text-lg">{systemStatus.total_screenshots || 0}</span>
                    </div>
                    <div className="flex justify-between items-center p-2 bg-white/50 rounded-md">
                      <span className="text-blue-700 font-medium">Index Status:</span>
                      <span className={`font-bold px-2 py-1 rounded-full text-sm ${
                        systemStatus.index_status === 'ready' 
                          ? 'bg-green-100 text-green-800' 
                          : systemStatus.index_status === 'building'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {systemStatus.index_status || 'Unknown'}
                      </span>
                    </div>
                    {systemStatus.index_size && (
                      <div className="flex justify-between items-center p-2 bg-white/50 rounded-md">
                        <span className="text-blue-700 font-medium">Index Size:</span>
                        <span className="font-bold text-blue-800">{(systemStatus.index_size / 1024 / 1024).toFixed(2)} MB</span>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="text-center py-4">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500 mx-auto mb-2"></div>
                    <p className="text-blue-600 text-sm">Loading status...</p>
                  </div>
                )}
              </div>

              {/* Generate Test Data */}
              <div className="p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg border border-green-200">
                <h3 className="font-semibold text-green-800 mb-2 flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Generate Test Data
                </h3>
                <button
                  onClick={generateTestData}
                  disabled={isGeneratingTestData}
                  className="w-full px-3 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isGeneratingTestData ? 'Generating...' : 'Generate 10 Test Screenshots'}
                </button>
              </div>

              {/* Rebuild Index */}
              <div className="p-4 bg-gradient-to-br from-purple-50 to-violet-50 rounded-lg border border-purple-200">
                <h3 className="font-semibold text-purple-800 mb-2 flex items-center gap-2">
                  <RefreshCw className="w-5 h-5" />
                  Rebuild Search Index
                </h3>
                <button
                  onClick={rebuildIndex}
                  disabled={isRebuildingIndex}
                  className="w-full px-3 py-2 bg-purple-500 text-white rounded-md hover:bg-purple-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isRebuildingIndex ? 'Rebuilding...' : 'Rebuild Index'}
                </button>
              </div>

              {/* Delete All Data */}
              <div className="p-4 bg-gradient-to-br from-red-50 to-pink-50 rounded-lg border border-red-200">
                <h3 className="font-semibold text-red-800 mb-2 flex items-center gap-2">
                  <Trash2 className="w-5 h-5" />
                  Delete All Data
                </h3>
                <button
                  onClick={deleteAllData}
                  disabled={isDeletingAllData}
                  className="w-full px-3 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isDeletingAllData ? 'Deleting...' : 'Delete All Data'}
                </button>
              </div>

              {/* OpenAI Configuration */}
              <div className="p-4 bg-gradient-to-br from-indigo-50 to-blue-50 rounded-lg border border-indigo-200">
                <h3 className="font-semibold text-indigo-800 mb-3 flex items-center gap-2">
                  <Key className="w-5 h-5" />
                  OpenAI API Key
                </h3>
                <div className="space-y-3">
                  {/* Key Status */}
                  <div className="flex justify-between items-center p-2 bg-white/50 rounded-md">
                    <span className="text-indigo-700 font-medium">Status:</span>
                    <span className={`font-bold px-2 py-1 rounded-full text-sm ${
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
                           placeholder={isEditingOpenAIKey ? "sk-..." : "Click 'Edit Key' to configure"}
                           className={`w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent pr-20 text-sm text-gray-900 bg-white placeholder-gray-500 ${
                             !isEditingOpenAIKey ? 'bg-gray-100 cursor-not-allowed' : ''
                           }`}
                           disabled={!isEditingOpenAIKey}
                         />
                    <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex gap-1">
                      <button
                        onClick={() => setShowOpenAIKey(!showOpenAIKey)}
                        className="p-1 text-gray-500 hover:text-gray-700 rounded"
                        title={showOpenAIKey ? 'Hide key' : 'Show key'}
                      >
                        {showOpenAIKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                      {!isEditingOpenAIKey && openAIKey && (
                        <button
                          onClick={() => {
                            if (confirm('Are you sure you want to delete your OpenAI API key?')) {
                              setOpenAIKey('');
                              saveOpenAIKey();
                            }
                          }}
                          className="p-1 text-red-500 hover:text-red-700 rounded"
                          title="Delete key"
                        >
                          <Trash className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>
                  
                  {/* Action Buttons */}
                  <div className="flex gap-2">
                    {isEditingOpenAIKey ? (
                      <>
                        <button
                          onClick={saveOpenAIKey}
                          className="flex-1 px-3 py-2 bg-indigo-500 text-white rounded-md hover:bg-indigo-600 transition-colors text-sm font-medium"
                        >
                          Save Key
                        </button>
                        <button
                          onClick={() => {
                            setIsEditingOpenAIKey(false);
                            loadOpenAIKey(); // Reset to original value
                          }}
                          className="flex-1 px-3 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors text-sm font-medium"
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <button
                        onClick={() => setIsEditingOpenAIKey(true)}
                        className="w-full px-3 py-2 bg-indigo-500 text-white rounded-md hover:bg-indigo-600 transition-colors text-sm font-medium"
                      >
                        {openAIKey ? 'Edit Key' : 'Add Key'}
                      </button>
                    )}
                  </div>
                  
                  {/* Key Info */}
                  {openAIKey && (
                    <div className="text-xs text-indigo-600 bg-indigo-50 p-2 rounded-md">
                      <p className="font-medium">Key Info:</p>
                      <p>• User-specific key (only you can see this)</p>
                      <p>• Used for enhanced search capabilities</p>
                      <p>• Stored securely on the server</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Organization & Permission Management */}
              <div className="p-4 bg-gradient-to-br from-orange-50 to-amber-50 rounded-lg border border-orange-200">
                <h3 className="font-semibold text-orange-800 mb-3 flex items-center gap-2">
                  <Settings className="w-5 h-5" />
                  Organization & Permissions
                </h3>
                <div className="space-y-3">
                  <button
                    onClick={() => setShowOrgManagement(true)}
                    className="w-full px-3 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 transition-colors text-sm font-medium"
                  >
                    Manage Organizations & Roles
                  </button>
                  <div className="text-xs text-orange-600 bg-orange-50 p-2 rounded-md">
                    <p className="font-medium">Features:</p>
                    <p>• Create and manage organizations</p>
                    <p>• Define custom roles and permissions</p>
                    <p>• Assign users to organizations</p>
                    <p>• Manage user access levels</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}



        {/* Upload Section */}
        <div className="mb-8 p-6 bg-white rounded-xl shadow-lg border border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Upload className="w-6 h-6 text-blue-500" />
            Upload Screenshots
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* File Upload */}
            <div className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border-2 border-dashed border-blue-300 hover:border-blue-400 transition-colors">
              <div className="text-center">
                <File className="w-12 h-12 text-blue-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-blue-800 mb-2">Upload Files</h3>
                <p className="text-blue-600 mb-4">Select individual screenshot files</p>
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isUploading}
                  className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50 transition-colors"
                >
                  {isUploading ? 'Uploading...' : 'Select Files'}
                </button>
              </div>
            </div>

            {/* Folder Upload */}
            <div className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg border-2 border-dashed border-green-300 hover:border-green-400 transition-colors">
              <div className="text-center">
                <Folder className="w-12 h-12 text-green-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-green-800 mb-2">Upload Folder</h3>
                <p className="text-green-600 mb-4">Select a folder with screenshots</p>
                <input
                  ref={folderInputRef}
                  type="file"
                  webkitdirectory=""
                  multiple
                  accept="image/*"
                  onChange={handleFolderSelect}
                  className="hidden"
                />
                <button
                  onClick={() => folderInputRef.current?.click()}
                  disabled={isUploading}
                  className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:opacity-50 transition-colors"
                >
                  {isUploading ? 'Uploading...' : 'Select Folder'}
                </button>
              </div>
            </div>
          </div>

          {/* Drag & Drop Zone */}
          <div
            className={`mt-6 p-8 border-2 border-dashed rounded-lg text-center transition-colors ${
              dragActive
                ? 'border-blue-400 bg-blue-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-lg font-medium text-gray-600 mb-2">
              Drag and drop screenshots here
            </p>
            <p className="text-gray-500">or use the upload buttons above</p>
          </div>

          {/* Upload Progress */}
          {isUploading && (
            <div className="mt-4">
              <div className="flex justify-between text-sm text-gray-600 mb-2">
                <span>Uploading...</span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
            </div>
          )}
        </div>

        {/* Search Section */}
        <div className="mb-8 p-6 bg-white rounded-xl shadow-lg border border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Search className="w-6 h-6 text-blue-500" />
            Search Screenshots
          </h2>
          
          <div className="flex gap-4 mb-6">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search by text content, description, or filename..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white placeholder-gray-500"
              />
            </div>
            <button
              onClick={() => handleSearch(searchQuery)}
              disabled={!searchQuery.trim() || isLoading}
              className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? 'Searching...' : 'Search'}
            </button>
          </div>

          {/* Search Results */}
          {searchResults.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Search Results ({searchResults.length})</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {searchResults.map((result, index) => (
                  <div key={index} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <div className="relative">
                                          <img
                      src={`/api/images/${result.screenshot.filename}`}
                      alt={result.screenshot.filename}
                      className="w-full h-32 object-cover rounded-md mb-3"
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjNmNGY2Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNiIgZmlsbD0iIzljYTNhZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIE5vdCBBdmFpbGFibGU8L3RleHQ+PC9zdmc+';
                      }}
                    />
                      {/* View button overlay */}
                      <button
                        onClick={() => viewScreenshot(result.screenshot)}
                        className="absolute top-2 right-2 p-2 bg-green-500 text-white rounded-full hover:bg-green-600 transition-colors shadow-lg"
                        title="View screenshot"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    </div>
                    <h4 className="font-medium text-gray-800 mb-1">{result.screenshot.filename}</h4>
                    <p className="text-sm text-gray-600 mb-2">Score: {result.score?.toFixed(3)}</p>
                    {result.screenshot.text_content && (
                      <p className="text-xs text-gray-500 line-clamp-2">{result.screenshot.text_content}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Screenshots Section */}
        <div className="p-6 bg-white rounded-xl shadow-lg border border-gray-200">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold text-gray-800 flex items-center gap-2">
              <FolderOpen className="w-6 h-6 text-blue-500" />
              My Screenshots ({getFilteredAndSortedScreenshots().length} of {screenshots.length})
            </h2>
            <div className="flex items-center gap-3">
              <button
                onClick={toggleSelectMode}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  isSelectMode 
                    ? 'bg-blue-500 text-white hover:bg-blue-600' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <CheckCircle className="w-4 h-4" />
                {isSelectMode ? 'Exit Select' : 'Select'}
              </button>
              <button
                onClick={() => setShowFilters(!showFilters)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  showFilters 
                    ? 'bg-purple-500 text-white hover:bg-purple-600' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Filter className="w-4 h-4" />
                Filters
              </button>
              <button
                onClick={loadScreenshots}
                disabled={isLoading}
                className="flex items-center gap-2 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 disabled:opacity-50 transition-colors"
              >
                <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
                Refresh
              </button>
            </div>
          </div>

          {/* Filters and Sorting Panel */}
          {showFilters && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Search Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
                  <input
                    type="text"
                    placeholder="Search by filename or content..."
                    value={searchFilter}
                    onChange={(e) => setSearchFilter(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white placeholder-gray-500"
                  />
                </div>

                {/* Extension Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">File Type</label>
                  <select
                    value={filterExtension}
                    onChange={(e) => setFilterExtension(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white"
                  >
                    {getUniqueExtensions().map(ext => (
                      <option key={ext} value={ext}>
                        {ext === 'all' ? 'All Types' : ext.toUpperCase()}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Date Range Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Date Range</label>
                  <select
                    value={filterDateRange}
                    onChange={(e) => setFilterDateRange(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white"
                  >
                    <option value="all">All Time</option>
                    <option value="today">Today</option>
                    <option value="week">Last 7 Days</option>
                    <option value="month">Last 30 Days</option>
                    <option value="year">Last Year</option>
                  </select>
                </div>

                {/* Size Range Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">File Size</label>
                  <select
                    value={filterSizeRange}
                    onChange={(e) => setFilterSizeRange(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white"
                  >
                    <option value="all">All Sizes</option>
                    <option value="small">Small (&lt; 1MB)</option>
                    <option value="medium">Medium (1MB - 5MB)</option>
                    <option value="large">Large (&gt; 5MB)</option>
                  </select>
                </div>
              </div>

              {/* Sorting Controls */}
              <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <label className="text-sm font-medium text-gray-700">Sort by:</label>
                    <select
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value as any)}
                      className="px-3 py-1 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white"
                    >
                      <option value="date">Date</option>
                      <option value="name">Name</option>
                      <option value="size">Size</option>
                      <option value="extension">Type</option>
                    </select>
                  </div>
                  <button
                    onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                    className="flex items-center gap-1 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
                  >
                    {sortOrder === 'asc' ? <ArrowUp className="w-4 h-4" /> : <ArrowDown className="w-4 h-4" />}
                    {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
                  </button>
                </div>
                <button
                  onClick={clearAllFilters}
                  className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 transition-colors"
                >
                  Clear All Filters
                </button>
              </div>
            </div>
          )}

          {/* Multi-select Actions */}
          {isSelectMode && (
            <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <span className="text-sm font-medium text-blue-800">
                    {selectedScreenshots.size} screenshot(s) selected
                  </span>
                  <div className="flex gap-2">
                    <button
                      onClick={selectAllScreenshots}
                      className="px-3 py-1 text-sm bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
                    >
                      Select All
                    </button>
                    <button
                      onClick={clearSelection}
                      className="px-3 py-1 text-sm bg-gray-500 text-white rounded-md hover:bg-gray-600 transition-colors"
                    >
                      Clear Selection
                    </button>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={downloadSelectedAsZip}
                    disabled={selectedScreenshots.size === 0 || isDownloadingZip}
                    className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:opacity-50 transition-colors"
                  >
                    <Download className="w-4 h-4" />
                    {isDownloadingZip ? 'Downloading...' : 'Download ZIP'}
                  </button>
                  <button
                    onClick={deleteSelectedScreenshots}
                    disabled={selectedScreenshots.size === 0}
                    className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 disabled:opacity-50 transition-colors"
                  >
                    <Trash className="w-4 h-4" />
                    Delete Selected
                  </button>
                </div>
              </div>
            </div>
          )}

          {isLoading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading screenshots...</p>
            </div>
          ) : getFilteredAndSortedScreenshots().length === 0 ? (
            <div className="text-center py-12">
              <FolderOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-600 mb-2">
                {screenshots.length === 0 ? 'No screenshots found' : 'No screenshots match your filters'}
              </h3>
              <p className="text-gray-500">
                {screenshots.length === 0 ? 'Upload some screenshots to get started' : 'Try adjusting your filters or search terms'}
              </p>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {getFilteredAndSortedScreenshots().map((screenshot) => (
                  <div key={screenshot.filename} className="bg-gray-50 rounded-lg overflow-hidden border border-gray-200 hover:shadow-lg transition-shadow">
                    <div className="relative">
                      {/* Multi-select checkbox */}
                      {isSelectMode && (
                        <div className="absolute top-2 left-2 z-10">
                          <input
                            type="checkbox"
                            checked={selectedScreenshots.has(screenshot.filename)}
                            onChange={() => toggleScreenshotSelection(screenshot.filename)}
                            className="w-5 h-5 text-blue-600 bg-white border-2 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
                          />
                        </div>
                      )}
                      
                      <img
                        src={`/api/images/${screenshot.filename}`}
                        alt={screenshot.filename}
                        className="w-full h-48 object-cover"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement;
                          target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjNmNGY2Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNiIgZmlsbD0iIzljYTNhZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIE5vdCBBdmFpbGFibGU8L3RleHQ+PC9zdmc+';
                        }}
                      />
                      
                      {/* Action buttons overlay */}
                      <div className="absolute top-2 right-2 flex gap-1">
                        {!isSelectMode && (
                          <>
                            <button
                              onClick={() => viewScreenshot(screenshot)}
                              className="p-2 bg-green-500 text-white rounded-full hover:bg-green-600 transition-colors shadow-lg"
                              title="View screenshot"
                            >
                              <Eye className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => downloadSingleImage(screenshot.filename)}
                              className="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors shadow-lg"
                              title="Download screenshot"
                            >
                              <Download className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => handleDeleteScreenshot(screenshot.filename)}
                              className="p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors shadow-lg"
                              title="Delete screenshot"
                            >
                              <Trash className="w-4 h-4" />
                            </button>
                          </>
                        )}
                      </div>
                      
                      {/* File type badge */}
                      <div className="absolute bottom-2 left-2">
                        <span className="px-2 py-1 bg-black bg-opacity-50 text-white text-xs rounded">
                          {getFileExtension(screenshot.filename).toUpperCase()}
                        </span>
                      </div>
                    </div>
                    <div className="p-4">
                      <h3 className="font-medium text-gray-800 mb-2 truncate" title={screenshot.filename}>
                        {screenshot.filename}
                      </h3>
                      <div className="space-y-1 text-sm text-gray-600">
                        <div className="flex justify-between items-center">
                          <span>Date:</span>
                          <span>{getFileDate(screenshot).toLocaleDateString()}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span>Size:</span>
                          <span>{formatFileSize(getFileSize(screenshot))}</span>
                        </div>
                        {screenshot.metadata?.dimensions && (
                          <div className="flex justify-between items-center">
                            <span>Dimensions:</span>
                            <span>{screenshot.metadata.dimensions.width}×{screenshot.metadata.dimensions.height}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex justify-center items-center gap-2 mt-8">
                  <button
                    onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                    disabled={currentPage === 1}
                    className="p-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <ChevronLeft className="w-5 h-5" />
                  </button>
                  
                  <span className="px-4 py-2 text-gray-700">
                    Page {currentPage} of {totalPages}
                  </span>
                  
                  <button
                    onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                    disabled={currentPage === totalPages}
                    className="p-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <ChevronRight className="w-5 h-5" />
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* View Screenshot Modal */}
      {viewModalOpen && selectedScreenshot && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl max-h-[90vh] overflow-hidden">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-800 truncate">
                {selectedScreenshot.filename}
              </h3>
              <button
                onClick={closeViewModal}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>
            
            {/* Modal Content */}
            <div className="p-4">
              {/* Screenshot Image */}
              <div className="flex justify-center mb-4">
                <img
                  src={`/api/images/${selectedScreenshot.filename}`}
                  alt={selectedScreenshot.filename}
                  className="max-w-full max-h-[60vh] object-contain rounded-lg shadow-lg"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjNmNGY2Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNiIgZmlsbD0iIzljYTNhZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIE5vdCBBdmFpbGFibGU8L3RleHQ+PC9zdmc+';
                  }}
                />
              </div>
              
              {/* Screenshot Details */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <h4 className="font-medium text-gray-800 mb-2">File Information</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Filename:</span>
                      <span className="font-medium">{selectedScreenshot.filename}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Size:</span>
                      <span className="font-medium">{formatFileSize(getFileSize(selectedScreenshot))}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Date:</span>
                      <span className="font-medium">{getFileDate(selectedScreenshot).toLocaleDateString()}</span>
                    </div>
                    {selectedScreenshot.metadata?.dimensions && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Dimensions:</span>
                        <span className="font-medium">
                          {selectedScreenshot.metadata.dimensions.width} × {selectedScreenshot.metadata.dimensions.height}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-800 mb-2">Content</h4>
                  {selectedScreenshot.text_content ? (
                    <div className="bg-gray-50 p-3 rounded-md">
                      <p className="text-gray-700 text-sm leading-relaxed">
                        {selectedScreenshot.text_content}
                      </p>
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">No text content extracted</p>
                  )}
                </div>
              </div>
              
              {/* Action Buttons */}
              <div className="flex justify-center gap-3 mt-6 pt-4 border-t border-gray-200">
                <button
                  onClick={() => downloadSingleImage(selectedScreenshot.filename)}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download
                </button>
                <button
                  onClick={() => {
                    handleDeleteScreenshot(selectedScreenshot.filename);
                    closeViewModal();
                  }}
                  className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                >
                  <Trash className="w-4 h-4" />
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Organization Management Modal */}
      {showOrgManagement && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Organization & Permission Management
              </h2>
              <button
                onClick={() => setShowOrgManagement(false)}
                className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Organizations Section */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                  <Building2 className="w-5 h-5" />
                  Organizations
                </h3>
                
                <div className="space-y-3">
                  <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700">
                    <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">Create Organization</h4>
                    <div className="space-y-2">
                      <input
                        type="text"
                        placeholder="Organization Name"
                        className="w-full px-3 py-2 border border-blue-200 dark:border-blue-700 rounded-md text-gray-900 bg-white dark:bg-gray-700 dark:text-white"
                        value={newOrgName}
                        onChange={(e) => setNewOrgName(e.target.value)}
                      />
                      <textarea
                        placeholder="Description (optional)"
                        className="w-full px-3 py-2 border border-blue-200 dark:border-blue-700 rounded-md text-gray-900 bg-white dark:bg-gray-700 dark:text-white"
                        value={newOrgDescription}
                        onChange={(e) => setNewOrgDescription(e.target.value)}
                        rows={2}
                      />
                      <button
                        onClick={async () => {
                          try {
                            const response = await fetch('/api/admin/organizations', {
                              method: 'POST',
                              headers: {
                                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                                'Content-Type': 'application/json'
                              },
                              body: JSON.stringify({
                                name: newOrgName,
                                description: newOrgDescription
                              })
                            });
                            
                            if (response.ok) {
                              alert('Organization created successfully!');
                              setNewOrgName('');
                              setNewOrgDescription('');
                            } else {
                              const error = await response.text();
                              alert(`Failed to create organization: ${error}`);
                            }
                          } catch (error) {
                            alert(`Error: ${error}`);
                          }
                        }}
                        className="w-full px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm font-medium"
                      >
                        Create Organization
                      </button>
                    </div>
                  </div>
                  
                  <div className="text-xs text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 p-2 rounded-md">
                    <p className="font-medium">Default Organization:</p>
                    <p>• System-wide access</p>
                    <p>• All users are members</p>
                    <p>• Admin roles can manage</p>
                  </div>
                </div>
              </div>

              {/* Roles & Permissions Section */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                  <Shield className="w-5 h-5" />
                  Roles & Permissions
                </h3>
                
                <div className="space-y-3">
                  <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700">
                    <h4 className="font-medium text-green-800 dark:text-green-200 mb-2">Available Roles</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between items-center">
                        <span className="font-medium">Admin</span>
                        <span className="text-green-600 dark:text-green-400">Full Access</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-medium">User</span>
                        <span className="text-green-600 dark:text-green-400">Standard Access</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="font-medium">Viewer</span>
                        <span className="text-green-600 dark:text-green-400">Read Only</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="text-xs text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 p-2 rounded-md">
                    <p className="font-medium">Role Capabilities:</p>
                    <p>• Admin: Full system access</p>
                    <p>• User: Upload, search, manage own data</p>
                    <p>• Viewer: Search and view only</p>
                  </div>
                </div>
              </div>

              {/* User Management Section */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  User Management
                </h3>
                
                <div className="space-y-3">
                  <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-700">
                    <h4 className="font-medium text-purple-800 dark:text-purple-200 mb-2">Assign Role</h4>
                    <div className="space-y-2">
                      <input
                        type="text"
                        placeholder="User ID or Email"
                        className="w-full px-3 py-2 border border-purple-200 dark:border-purple-700 rounded-md text-gray-900 bg-white dark:bg-gray-700 dark:text-white"
                        value={newUserEmail}
                        onChange={(e) => setNewUserEmail(e.target.value)}
                      />
                      <select
                        className="w-full px-3 py-2 border border-purple-200 dark:border-purple-700 rounded-md text-gray-900 bg-white dark:bg-gray-700 dark:text-white"
                        value={newUserRole}
                        onChange={(e) => setNewUserRole(e.target.value)}
                      >
                        <option value="user">User</option>
                        <option value="admin">Admin</option>
                        <option value="viewer">Viewer</option>
                      </select>
                      <button
                        onClick={async () => {
                          try {
                            const response = await fetch('/api/admin/assign-role', {
                              method: 'POST',
                              headers: {
                                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
                                'Content-Type': 'application/json'
                              },
                              body: JSON.stringify({
                                user_email: newUserEmail,
                                role: newUserRole
                              })
                            });
                            
                            if (response.ok) {
                              alert('Role assigned successfully!');
                              setNewUserEmail('');
                              setNewUserRole('user');
                            } else {
                              const error = await response.text();
                              alert(`Failed to assign role: ${error}`);
                            }
                          } catch (error) {
                            alert(`Error: ${error}`);
                          }
                        }}
                        className="w-full px-3 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors text-sm font-medium"
                      >
                        Assign Role
                      </button>
                    </div>
                  </div>
                  
                  <div className="text-xs text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-900/20 p-2 rounded-md">
                    <p className="font-medium">Quick Actions:</p>
                    <p>• Enter user email to assign role</p>
                    <p>• Choose appropriate permission level</p>
                    <p>• Changes apply immediately</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
