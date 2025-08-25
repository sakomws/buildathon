

import React from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { HelpCircle, Mail, MessageCircle, Phone, Clock, MapPin, Users, BookOpen, FileText, Video, CheckCircle, AlertCircle, Info, Shield } from 'lucide-react';

// Disable static generation for this page
export const dynamic = 'force-dynamic';

export default function Support() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="flex justify-center mb-4">
              <MessageCircle className="h-16 w-16 text-blue-600 dark:text-blue-400" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Support Center
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              We're here to help you get the most out of Visual Memory Search. 
              Find answers, get help, and connect with our team.
            </p>
          </div>

          {/* Quick Contact */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="p-6 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700 text-center">
              <Mail className="h-8 w-8 text-blue-600 dark:text-blue-400 mx-auto mb-3" />
              <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">Email Support</h3>
              <p className="text-blue-700 dark:text-blue-300 text-sm mb-3">Get help via email</p>
              <a
                href="mailto:support@visualmemorysearch.com"
                className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors"
              >
                Send Email
              </a>
            </div>

            <div className="p-6 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700 text-center">
              <Clock className="h-8 w-8 text-green-600 dark:text-green-400 mx-auto mb-3" />
              <h3 className="text-lg font-semibold text-green-900 dark:text-green-100 mb-2">Response Time</h3>
              <p className="text-green-700 dark:text-green-300 text-sm mb-3">Within 24 hours</p>
              <span className="inline-flex items-center px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200 text-sm rounded-full">
                Guaranteed
              </span>
            </div>

            <div className="p-6 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-700 text-center">
              <Users className="h-8 w-8 text-purple-600 dark:text-purple-400 mx-auto mb-3" />
              <h3 className="text-lg font-semibold text-purple-900 dark:text-purple-100 mb-2">Community</h3>
              <p className="text-purple-700 dark:text-purple-300 text-sm mb-3">Join our community</p>
              <a
                href="https://github.com/sakomws/buildathon"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm rounded-lg transition-colors"
              >
                GitHub
              </a>
            </div>
          </div>

          {/* FAQ Section */}
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center flex items-center justify-center">
              <HelpCircle className="h-8 w-8 mr-3 text-blue-600" />
              Frequently Asked Questions
            </h2>
            
            <div className="space-y-6">
              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  How do I get started with Visual Memory Search?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Getting started is easy! Simply sign in with your Google or GitHub account, 
                  or create a traditional email/password account. Once authenticated, you can 
                  start uploading screenshots and searching through them immediately.
                </p>
              </div>

              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  What file formats are supported?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  We support PNG, JPG, JPEG, GIF, and BMP files. PNG is recommended for 
                  screenshots with text as it provides the best OCR results. Maximum file 
                  size is 16MB.
                </p>
              </div>

              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  How does the AI search work?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Our AI-powered search combines text extraction (OCR), visual feature analysis, 
                  and natural language processing. You can search by text content, visual 
                  similarity, or use combined search for the best results.
                </p>
              </div>

              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  Is my data secure?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Absolutely! We use enterprise-grade security including OAuth 2.0, JWT tokens, 
                  data encryption, and secure cloud storage. Your data is never shared with 
                  third parties without your explicit consent.
                </p>
              </div>

              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  Can I export my data?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Yes! You can download your screenshots and metadata at any time. We also 
                  provide API access for programmatic data export. Your data belongs to you.
                </p>
              </div>

              <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  What if I need help with the API?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  We provide comprehensive API documentation with examples in JavaScript, 
                  Python, and cURL. Check our <a href="/api" className="text-blue-600 dark:text-blue-400 hover:underline">API Reference</a> page 
                  for detailed information and code samples.
                </p>
              </div>
            </div>
          </div>

          {/* Support Channels */}
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center flex items-center justify-center">
              <MessageCircle className="h-8 w-8 mr-3 text-green-600" />
              Support Channels
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="space-y-6">
                <div className="p-6 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center mb-4">
                    <Mail className="h-6 w-6 text-blue-600 mr-3" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Email Support</h3>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 mb-4">
                    Get detailed help and technical support via email. Our team typically 
                    responds within 24 hours.
                  </p>
                  <a
                    href="mailto:support@visualmemorysearch.com"
                    className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                  >
                    Contact Support
                  </a>
                </div>

                <div className="p-6 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center mb-4">
                    <FileText className="h-6 w-6 text-green-600 mr-3" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Documentation</h3>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 mb-4">
                    Comprehensive guides and tutorials to help you master all features.
                  </p>
                  <a
                    href="/docs"
                    className="inline-flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                  >
                    View Docs
                  </a>
                </div>
              </div>

              <div className="space-y-6">
                <div className="p-6 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center mb-4">
                    <Users className="h-6 w-6 text-purple-600 mr-3" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Community</h3>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 mb-4">
                    Connect with other users, share tips, and get community support.
                  </p>
                  <a
                    href="https://github.com/sakomws/buildathon"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
                  >
                    Join Community
                  </a>
                </div>

                <div className="p-6 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center mb-4">
                    <MessageCircle className="h-6 w-6 text-orange-600 mr-3" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Live Chat</h3>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300 mb-4">
                    Get instant help with our live chat support during business hours.
                  </p>
                  <button className="inline-flex items-center px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg transition-colors">
                    Start Chat
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Enterprise Support */}
          <div className="mb-12">
            <div className="p-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg text-white">
              <div className="text-center">
                <Shield className="h-12 w-12 mx-auto mb-4 text-white" />
                <h2 className="text-3xl font-bold mb-4">Enterprise Support</h2>
                <p className="text-xl mb-6 max-w-3xl mx-auto">
                  Need dedicated support for your organization? Our enterprise support team 
                  provides priority assistance, custom integrations, and dedicated account management.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <a
                    href="/pricing"
                    className="inline-flex items-center px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    View Plans
                  </a>
                  <a
                    href="mailto:enterprise@visualmemorysearch.com"
                    className="inline-flex items-center px-6 py-3 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-blue-600 transition-colors"
                  >
                    Contact Sales
                  </a>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center flex items-center justify-center">
              <MessageCircle className="h-8 w-8 mr-3 text-blue-600" />
              Still Need Help?
            </h2>
            
            <div className="max-w-2xl mx-auto">
              <form className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      First Name
                    </label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                      placeholder="Your first name"
                    />
                  </div>
                  <div>
                    <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Last Name
                    </label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                      placeholder="Your last name"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                    placeholder="your.email@example.com"
                  />
                </div>

                <div>
                  <label htmlFor="subject" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Subject
                  </label>
                  <select
                    id="subject"
                    name="subject"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                  >
                    <option value="">Select a topic</option>
                    <option value="technical">Technical Support</option>
                    <option value="billing">Billing & Account</option>
                    <option value="feature">Feature Request</option>
                    <option value="bug">Bug Report</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Message
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    rows={6}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                    placeholder="Describe your issue or question in detail..."
                  ></textarea>
                </div>

                <div className="text-center">
                  <button
                    type="submit"
                    className="inline-flex items-center px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
                  >
                    <Mail className="w-5 h-5 mr-2" />
                    Send Message
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
