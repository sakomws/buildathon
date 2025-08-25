/** TypeScript interfaces for API communication. */

// Search and Query Types
export interface SearchQuery {
  query: string;
  search_type: 'text' | 'visual' | 'combined';
  max_results: number;
}

// Screenshot Metadata
export interface ScreenshotMetadata {
  file_size?: number;
  dimensions?: {
    width: number;
    height: number;
  };
  mime_type?: string;
  created_at?: string;
  modified_at?: string;
  [key: string]: unknown;
}

// Screenshot Information
export interface ScreenshotInfo {
  filename: string;
  filepath: string;
  timestamp?: string;
  text_content?: string;
  visual_features?: number[];
  metadata?: ScreenshotMetadata;
}

// Search Results with Confidence Scores
export interface SearchResult {
  screenshot: ScreenshotInfo;
  score: number; // Final combined score
  base_score?: number; // Base algorithm confidence score
  openai_score?: number; // OpenAI enhanced score
  match_type: 'text' | 'visual' | 'combined';
  highlights?: string[];
  confidence_breakdown?: {
    text_similarity?: number;
    visual_similarity?: number;
    openai_enhancement?: number;
    final_weighted?: number;
  };
}

// Upload Responses
export interface UploadResponse {
  message: string;
  filename: string;
  indexed: boolean;
  file_size?: number;
  processing_time?: number;
}

export interface BulkUploadResponse {
  total_files: number;
  successful_uploads: number;
  failed_uploads: number;
  results: UploadResponse[];
  processing_time: number;
}

// Health and Status
export interface HealthResponse {
  status: 'healthy' | 'unhealthy';
  service: string;
  version: string;
  timestamp: string;
  uptime?: number;
}

export interface AdminStatusResponse {
  total_screenshots: number;
  index_size: number;
  embeddings_loaded: boolean;
  models_ready: boolean;
  storage_usage?: Record<string, unknown>;
  system_info?: Record<string, unknown>;
}

// Admin Operations
export interface RebuildIndexResponse {
  message: string;
  screenshots_processed: number;
  processing_time: number;
  index_size: number;
}

export interface OpenAIKeyTestResponse {
  valid: boolean;
  message: string;
  model_available?: string;
  rate_limit_info?: Record<string, unknown>;
}

// Error Response
export interface ErrorResponse {
  error: string;
  detail?: string;
  error_code?: string;
  timestamp: string;
  request_id?: string;
}

// API Response Wrapper
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

// Pagination
export interface PaginationParams {
  page: number;
  limit: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
  };
}

// Filter Options
export interface ScreenshotFilters {
  date_from?: string;
  date_to?: string;
  min_size?: number;
  max_size?: number;
  has_text?: boolean;
  file_types?: string[];
}

// Sort Options
export interface SortOptions {
  field: 'filename' | 'timestamp' | 'file_size' | 'created_at';
  direction: 'asc' | 'desc';
}

// Authentication Types
export interface AuthUser {
  id: string;
  email: string;
  name: string;
  picture?: string;
  given_name?: string;
  family_name?: string;
  locale?: string;
  verified_email?: boolean;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: AuthUser;
  expires_in: number;
}

export interface TokenRefreshResponse {
  access_token: string;
  expires_in: number;
}

// Cookie Preferences
export interface CookiePreferences {
  essential: boolean;
  functional: boolean;
  analytics: boolean;
  marketing: boolean;
}
