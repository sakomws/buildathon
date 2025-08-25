'use client';

import React from 'react';
import { FileText, Github, ExternalLink, Mail, Shield, Zap, Database } from 'lucide-react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <FileText className="h-8 w-8 text-blue-600 dark:text-blue-400" />
              <span className="text-xl font-bold text-gray-900 dark:text-white">Visual Memory Search</span>
            </div>
            <p className="text-gray-600 dark:text-gray-400 mb-4 max-w-md">
              Enterprise-grade AI-powered screenshot search and management system. 
              Find, organize, and analyze your visual content with advanced machine learning.
            </p>
            <div className="flex space-x-4">
              <a
                href="https://github.com/sakomws/buildathon"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="mailto:support@visualmemorysearch.com"
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
              >
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Product Features */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 dark:text-white tracking-wider uppercase mb-4">
              Features
            </h3>
            <ul className="space-y-2">
              <li className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                <Zap className="h-4 w-4 mr-2 text-green-500" />
                AI-Powered Search
              </li>
              <li className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                <Database className="h-4 w-4 mr-2 text-blue-500" />
                Smart Indexing
              </li>
              <li className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                <Shield className="h-4 w-4 mr-2 text-purple-500" />
                Enterprise Security
              </li>
              <li className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                <FileText className="h-4 w-4 mr-2 text-orange-500" />
                OCR & Text Extraction
              </li>
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 dark:text-white tracking-wider uppercase mb-4">
              Resources
            </h3>
            <ul className="space-y-2">
              <li>
                <a
                  href="/docs"
                  className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors flex items-center"
                >
                  <ExternalLink className="h-3 w-3 mr-2" />
                  Documentation
                </a>
              </li>
              <li>
                <a
                  href="/api"
                  className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors flex items-center"
                >
                  <ExternalLink className="h-3 w-3 mr-2" />
                  API Reference
                </a>
              </li>
              <li>
                <a
                  href="/support"
                  className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors flex items-center"
                >
                  <ExternalLink className="h-3 w-3 mr-2" />
                  Support
                </a>
              </li>
              <li>
                <a
                  href="/pricing"
                  className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors flex items-center"
                >
                  <ExternalLink className="h-3 w-3 mr-2" />
                  Pricing
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              © {currentYear} Visual Memory Search. All rights reserved.
            </div>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a
                href="/privacy"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                Privacy Policy
              </a>
              <a
                href="/terms"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                Terms of Service
              </a>
              <a
                href="/cookies"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                Cookie Policy
              </a>
            </div>
          </div>
        </div>

        {/* Enterprise Badge */}
        <div className="mt-6 text-center">
          <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-medium rounded-full">
            <Shield className="h-4 w-4 mr-2" />
            Enterprise Ready
          </div>
        </div>
      </div>
    </footer>
  );
}
