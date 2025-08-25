'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/components/Auth/AuthProvider';
import { useRouter } from 'next/navigation';
import { 
  BarChart3, 
  PieChart, 
  TrendingUp, 
  FileImage, 
  Brain, 
  DollarSign,
  Calendar,
  Clock,
  HardDrive,
  Search,
  Activity,
  Zap
} from 'lucide-react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

// Disable static generation for this page
export const dynamic = 'force-dynamic';

interface AnalyticsData {
  user_stats: {
    total_screenshots: number;
    total_size_mb: number;
    avg_file_size_kb: number;
    file_types: Record<string, number>;
    upload_timeline: Array<{ date: string; count: number }>;
  };
  openai_stats: {
    total_requests: number;
    total_tokens: number;
    avg_tokens_per_request: number;
    cost_estimate: number;
    usage_timeline: Array<{ date: string; requests: number; tokens: number }>;
  };
  search_stats: {
    total_searches: number;
    avg_results: number;
    popular_queries: Array<{ query: string; count: number }>;
  };
}

interface OpenAIUsageData {
  daily_usage: Array<{ date: string; requests: number; tokens: number; cost: number }>;
  model_usage: Array<{ model: string; requests: number; tokens: number; cost: number }>;
  request_types: Array<{ type: string; count: number; avg_tokens: number }>;
  cost_breakdown: {
    total_cost: number;
    daily_average: number;
    monthly_estimate: number;
    cost_per_request: number;
  };
}

interface ImageAnalyticsData {
  image_stats: {
    total_images: number;
    total_size_mb: number;
    avg_dimensions: { width: number; height: number };
    file_types: Record<string, number>;
    size_distribution: Array<{ range: string; count: number }>;
  };
  upload_patterns: {
    hourly_distribution: Array<{ hour: number; count: number }>;
    daily_distribution: Array<{ day: string; count: number }>;
    monthly_trend: Array<{ month: string; count: number }>;
  };
  image_analysis: {
    text_extraction_success: number;
    avg_text_length: number;
    common_words: Array<{ word: string; count: number }>;
    ocr_confidence: number;
  };
}

export default function AnalyticsPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'overview' | 'openai' | 'images'>('overview');
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [openaiData, setOpenaiData] = useState<OpenAIUsageData | null>(null);
  const [imageData, setImageData] = useState<ImageAnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/auth/login');
      return;
    }

    if (user) {
      loadAnalyticsData();
    }
  }, [user, isLoading, router]);

  const loadAnalyticsData = async () => {
    try {
      setLoading(true);
      
      // Load overview data
      const overviewResponse = await fetch('/api/analytics/overview', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token') || localStorage.getItem('access_token')}`
        }
      });
      
      if (overviewResponse.ok) {
        const overviewData = await overviewResponse.json();
        setAnalyticsData(overviewData);
      }

      // Load OpenAI usage data
      const openaiResponse = await fetch('/api/analytics/openai-usage', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token') || localStorage.getItem('access_token')}`
        }
      });
      
      if (openaiResponse.ok) {
        const openaiUsageData = await openaiResponse.json();
        setOpenaiData(openaiUsageData);
      }

      // Load image analytics data
      const imageResponse = await fetch('/api/analytics/image-analytics', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token') || localStorage.getItem('access_token')}`
        }
      });
      
      if (imageResponse.ok) {
        const imageAnalyticsData = await imageResponse.json();
        setImageData(imageAnalyticsData);
      }
    } catch (error) {
      console.error('Failed to load analytics data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (isLoading || loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Header />
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-400">Loading analytics...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const StatCard = ({ title, value, subtitle, icon: Icon, color = "blue" }: {
    title: string;
    value: string | number;
    subtitle?: string;
    icon: React.ComponentType<any>;
    color?: string;
  }) => (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{value}</p>
          {subtitle && (
            <p className="text-sm text-gray-500 dark:text-gray-500 mt-1">{subtitle}</p>
          )}
        </div>
        <div className={`p-3 rounded-full bg-${color}-100 dark:bg-${color}-900/30`}>
          <Icon className={`w-6 h-6 text-${color}-600 dark:text-${color}-400`} />
        </div>
      </div>
    </div>
  );

  const renderOverviewTab = () => (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Screenshots"
          value={analyticsData?.user_stats.total_screenshots || 0}
          icon={FileImage}
          color="blue"
        />
        <StatCard
          title="OpenAI Requests"
          value={analyticsData?.openai_stats.total_requests || 0}
          icon={Brain}
          color="purple"
        />
        <StatCard
          title="Total Searches"
          value={analyticsData?.search_stats.total_searches || 0}
          icon={Search}
          color="green"
        />
        <StatCard
          title="Storage Used"
          value={`${analyticsData?.user_stats.total_size_mb || 0} MB`}
          icon={HardDrive}
          color="orange"
        />
      </div>

      {/* OpenAI Usage Summary */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <Brain className="w-5 h-5 mr-2 text-purple-600" />
          OpenAI Usage Summary
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Total Tokens</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {analyticsData?.openai_stats.total_tokens.toLocaleString() || 0}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Avg Tokens/Request</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {analyticsData?.openai_stats.avg_tokens_per_request || 0}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Estimated Cost</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              ${analyticsData?.openai_stats.cost_estimate || 0}
            </p>
          </div>
        </div>
      </div>

      {/* Popular Search Queries */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <Search className="w-5 h-5 mr-2 text-green-600" />
          Popular Search Queries
        </h3>
        <div className="space-y-3">
          {analyticsData?.search_stats.popular_queries.map((query, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <span className="text-gray-900 dark:text-white font-medium">{query.query}</span>
              <span className="text-sm text-gray-600 dark:text-gray-400">{query.count} searches</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderOpenAITab = () => (
    <div className="space-y-6">
      {openaiData && (
        <>
          {/* Cost Overview */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <StatCard
              title="Total Cost"
              value={`$${openaiData.cost_breakdown.total_cost}`}
              icon={DollarSign}
              color="green"
            />
            <StatCard
              title="Daily Average"
              value={`$${openaiData.cost_breakdown.daily_average}`}
              icon={Calendar}
              color="blue"
            />
            <StatCard
              title="Monthly Estimate"
              value={`$${openaiData.cost_breakdown.monthly_estimate}`}
              icon={TrendingUp}
              color="purple"
            />
            <StatCard
              title="Cost per Request"
              value={`$${openaiData.cost_breakdown.cost_per_request}`}
              icon={Activity}
              color="orange"
            />
          </div>

          {/* Model Usage */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <Brain className="w-5 h-5 mr-2 text-purple-600" />
              Model Usage
            </h3>
            <div className="space-y-4">
              {openaiData.model_usage.map((model, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">{model.model}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {model.requests} requests • {model.tokens.toLocaleString()} tokens
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-gray-900 dark:text-white">${model.cost}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Request Types */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <Zap className="w-5 h-5 mr-2 text-yellow-600" />
              Request Types
            </h3>
            <div className="space-y-4">
              {openaiData.request_types.map((type, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white capitalize">
                      {type.type.replace('_', ' ')}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {type.count} requests • {type.avg_tokens} avg tokens
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );

  const renderImagesTab = () => (
    <div className="space-y-6">
      {imageData && (
        <>
          {/* Image Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <StatCard
              title="Total Images"
              value={imageData.image_stats.total_images}
              icon={FileImage}
              color="blue"
            />
            <StatCard
              title="Total Size"
              value={`${imageData.image_stats.total_size_mb} MB`}
              icon={HardDrive}
              color="green"
            />
            <StatCard
              title="Avg Dimensions"
              value={`${imageData.image_stats.avg_dimensions.width}x${imageData.image_stats.avg_dimensions.height}`}
              icon={BarChart3}
              color="purple"
            />
            <StatCard
              title="OCR Success Rate"
              value={`${imageData.image_analysis.text_extraction_success}%`}
              icon={Activity}
              color="orange"
            />
          </div>

          {/* File Type Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <PieChart className="w-5 h-5 mr-2 text-blue-600" />
              File Type Distribution
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.entries(imageData.image_stats.file_types).map(([type, count]) => (
                <div key={type} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="font-medium text-gray-900 dark:text-white">{type.toUpperCase()}</p>
                  <p className="text-2xl font-bold text-blue-600">{count}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Size Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-green-600" />
              Size Distribution
            </h3>
            <div className="space-y-3">
              {imageData.image_stats.size_distribution.map((item, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <span className="text-gray-900 dark:text-white font-medium">{item.range}</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">{item.count} files</span>
                </div>
              ))}
            </div>
          </div>

          {/* Common Words */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <Search className="w-5 h-5 mr-2 text-purple-600" />
              Common Words in Images
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {imageData.image_analysis.common_words.map((word, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <span className="text-gray-900 dark:text-white font-medium">{word.word}</span>
                  <span className="text-sm text-gray-600 dark:text-gray-400">{word.count} occurrences</span>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Analytics Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Monitor your OpenAI usage and image analytics
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="border-b border-gray-200 dark:border-gray-700 mb-8">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'openai', label: 'OpenAI Usage', icon: Brain },
              { id: 'images', label: 'Image Analytics', icon: FileImage }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4 mr-2" />
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          {activeTab === 'overview' && renderOverviewTab()}
          {activeTab === 'openai' && renderOpenAITab()}
          {activeTab === 'images' && renderImagesTab()}
        </div>
      </main>

      <Footer />
    </div>
  );
}
