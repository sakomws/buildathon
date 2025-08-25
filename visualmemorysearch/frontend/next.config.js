/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['localhost'],
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/api/screenshots/**',
      },
    ],
  },
  async rewrites() {
    return [
      {
        source: '/api/screenshots/:path*',
        destination: 'http://localhost:8000/api/screenshots/:path*',
      },
      {
        source: '/api/admin/:path*',
        destination: 'http://localhost:8000/api/admin/:path*',
      },
      {
        source: '/api/upload',
        destination: 'http://localhost:8000/api/upload',
      },
      {
        source: '/api/search',
        destination: 'http://localhost:8000/api/search',
      },
      {
        source: '/api/screenshots',
        destination: 'http://localhost:8000/api/screenshots',
      },
      // Proxy OAuth callback endpoints to backend
      {
        source: '/auth/google/callback',
        destination: 'http://localhost:8000/auth/google/callback',
      },
      {
        source: '/auth/github/callback',
        destination: 'http://localhost:8000/auth/github/callback',
      },
      // Proxy OAuth start endpoints to backend
      {
        source: '/auth/google',
        destination: 'http://localhost:8000/auth/google',
      },
      {
        source: '/auth/github',
        destination: 'http://localhost:8000/auth/github',
      },
      // Keep login and register pages on frontend
      {
        source: '/auth/login',
        destination: '/auth/login',
      },
      {
        source: '/auth/register',
        destination: '/auth/register',
      },
      // Proxy all other auth routes to backend
      {
        source: '/auth/:path*',
        destination: 'http://localhost:8000/auth/:path*',
      },
      // Proxy analytics routes to backend
      {
        source: '/api/analytics/:path*',
        destination: 'http://localhost:8000/api/analytics/:path*',
      },
      // User endpoints
      {
        source: '/api/user/:path*',
        destination: 'http://localhost:8000/api/user/:path*',
      },
      // User-specific rebuild and generate endpoints
      {
        source: '/api/rebuild-index',
        destination: 'http://localhost:8000/api/rebuild-index',
      },
      {
        source: '/api/generate-test-data',
        destination: 'http://localhost:8000/api/generate-test-data',
      },
      // Public image endpoint
      {
        source: '/api/images/:path*',
        destination: 'http://localhost:8000/api/images/:path*',
      },
      // Auth endpoints
      {
        source: '/api/auth/:path*',
        destination: 'http://localhost:8000/api/auth/:path*',
      },
      // Admin endpoints
      {
        source: '/api/admin/:path*',
        destination: 'http://localhost:8000/api/admin/:path*',
      },
      // Organization and permission management endpoints
      {
        source: '/api/admin/organizations',
        destination: 'http://localhost:8000/api/admin/organizations',
      },
      {
        source: '/api/admin/roles',
        destination: 'http://localhost:8000/api/admin/roles',
      },
      {
        source: '/api/admin/users',
        destination: 'http://localhost:8000/api/admin/users',
      },
      {
        source: '/api/admin/assign-role',
        destination: 'http://localhost:8000/api/admin/assign-role',
      },
    ];
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
};

module.exports = nextConfig;
