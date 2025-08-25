'use client';

import React from 'react';
import { SearchResult } from '@/types/api';
import { FileImage, Star, Brain, Zap, TrendingUp } from 'lucide-react';

interface SearchResultsProps {
  results: SearchResult[];
  isLoading: boolean;
  query: string;
}

export default function SearchResults({ results, isLoading, query }: SearchResultsProps) {
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">Searching...</span>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="text-center py-12">
        <FileImage className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">No results found</h3>
        <p className="mt-1 text-sm text-gray-500">
          No screenshots match "{query}". Try different keywords or search type.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">
          Search Results ({results.length})
        </h3>
        <div className="text-sm text-gray-500">
          Query: "{query}"
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.map((result, index) => (
          <SearchResultCard key={index} result={result} rank={index + 1} />
        ))}
      </div>
    </div>
  );
}

interface SearchResultCardProps {
  result: SearchResult;
  rank: number;
}

function SearchResultCard({ result, rank }: SearchResultCardProps) {
  const { screenshot, score, match_type, highlights } = result;
  
  // Extract scores from the result
  const baseScore = result.base_score || 0;
  const openaiScore = result.openai_score || 0;
  const finalScore = score || 0;

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-100';
    if (score >= 0.6) return 'text-blue-600 bg-blue-100';
    if (score >= 0.4) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 0.8) return <Star className="w-4 h-4" />;
    if (score >= 0.6) return <TrendingUp className="w-4 h-4" />;
    if (score >= 0.4) return <Zap className="w-4 h-4" />;
    return <Brain className="w-4 h-4" />;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
      {/* Rank Badge */}
      <div className="absolute top-2 left-2 z-10">
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white text-xs font-bold px-2 py-1 rounded-full">
          #{rank}
        </div>
      </div>

      {/* Match Type Badge */}
      <div className="absolute top-2 right-2 z-10">
        <div className="bg-gray-800 text-white text-xs px-2 py-1 rounded-full capitalize">
          {match_type}
        </div>
      </div>

      {/* Screenshot Image */}
      <div className="relative">
        <img
                          src={`/api/images/${screenshot.filename}`}
          alt={screenshot.filename}
          className="w-full h-48 object-cover"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = '/placeholder-image.png';
          }}
        />
        
        {/* Score Overlay */}
        <div className="absolute bottom-2 left-2 right-2">
          <div className="bg-black bg-opacity-75 text-white text-xs p-2 rounded">
            <div className="flex items-center justify-between">
              <span>Final Score:</span>
              <span className="font-bold">{finalScore.toFixed(3)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h4 className="font-medium text-gray-900 truncate mb-2">
          {screenshot.filename}
        </h4>
        
        {screenshot.text_content && (
          <p className="text-sm text-gray-600 mb-3 line-clamp-2">
            {screenshot.text_content}
          </p>
        )}

        {/* Confidence Scores */}
        <div className="space-y-2 mb-3">
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center space-x-1">
              <Brain className="w-3 h-3 text-blue-500" />
              <span className="text-gray-600">Base Score:</span>
            </div>
            <span className={`px-2 py-1 rounded ${getScoreColor(baseScore)}`}>
              {baseScore.toFixed(3)}
            </span>
          </div>
          
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center space-x-1">
              <Zap className="w-3 h-3 text-purple-500" />
              <span className="text-gray-600">OpenAI Score:</span>
            </div>
            <span className={`px-2 py-1 rounded ${getScoreColor(openaiScore)}`}>
              {openaiScore.toFixed(3)}
            </span>
          </div>
          
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center space-x-1">
              <Star className="w-3 h-3 text-yellow-500" />
              <span className="text-gray-600">Final Score:</span>
            </div>
            <span className={`px-2 py-1 rounded ${getScoreColor(finalScore)}`}>
              {finalScore.toFixed(3)}
            </span>
          </div>
        </div>

        {/* Highlights */}
        {highlights && highlights.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {highlights.map((highlight, index) => (
              <span
                key={index}
                className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
              >
                {highlight}
              </span>
            ))}
          </div>
        )}

        {/* Metadata */}
        {screenshot.metadata && (
          <div className="mt-3 pt-3 border-t border-gray-100 text-xs text-gray-500">
            {screenshot.metadata.file_size && (
              <div>Size: {(screenshot.metadata.file_size / 1024).toFixed(1)} KB</div>
            )}
            {screenshot.metadata.dimensions && (
              <div>
                Dimensions: {screenshot.metadata.dimensions.width} × {screenshot.metadata.dimensions.height}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
