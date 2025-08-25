

import React from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { DollarSign, CheckCircle, Star, Zap, Shield, Users, Database, Globe, Lock, Eye, BarChart3, Settings, HelpCircle, Info } from 'lucide-react';

// Disable static generation for this page
export const dynamic = 'force-dynamic';

export default function Pricing() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Simple, Transparent Pricing
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Choose the plan that fits your needs. All plans include our core AI-powered 
            search features with no hidden fees.
          </p>
        </div>

        {/* Pricing Toggle */}
        <div className="flex justify-center mb-12">
          <div className="bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
            <div className="flex">
              <button className="px-6 py-2 text-sm font-medium text-gray-900 dark:text-white bg-white dark:bg-gray-600 rounded-md shadow-sm">
                Monthly
              </button>
              <button className="px-6 py-2 text-sm font-medium text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white">
                Annual
                <span className="ml-2 text-xs bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200 px-2 py-1 rounded-full">
                  Save 20%
                </span>
              </button>
            </div>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {/* Free Plan */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 relative">
            <div className="text-center">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Free</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900 dark:text-white">$0</span>
                <span className="text-gray-500 dark:text-gray-400">/month</span>
              </div>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Perfect for individuals getting started with visual search
              </p>
              <button className="w-full py-3 px-6 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                Get Started Free
              </button>
            </div>

            <div className="mt-8 space-y-4">
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">What's included:</h4>
              <div className="space-y-3">
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">100 screenshots</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Basic AI search</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">OCR text extraction</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Email support</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Basic API access</span>
                </div>
              </div>
            </div>
          </div>

          {/* Pro Plan */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border-2 border-blue-500 p-8 relative">
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <span className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-medium">
                Most Popular
              </span>
            </div>
            
            <div className="text-center">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Pro</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900 dark:text-white">$29</span>
                <span className="text-gray-500 dark:text-gray-400">/month</span>
              </div>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Ideal for professionals and small teams
              </p>
              <button className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
                Start Pro Trial
              </button>
            </div>

            <div className="mt-8 space-y-4">
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Everything in Free, plus:</h4>
              <div className="space-y-3">
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">10,000 screenshots</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Advanced AI search</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Visual similarity search</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Priority support</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Full API access</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Team collaboration</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Advanced analytics</span>
                </div>
              </div>
            </div>
          </div>

          {/* Enterprise Plan */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 relative">
            <div className="text-center">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Enterprise</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900 dark:text-white">Custom</span>
              </div>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                For large organizations with custom needs
              </p>
              <button className="w-full py-3 px-6 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                Contact Sales
              </button>
            </div>

            <div className="mt-8 space-y-4">
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Everything in Pro, plus:</h4>
              <div className="space-y-3">
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Unlimited screenshots</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Custom AI models</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Dedicated support</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">SLA guarantees</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Custom integrations</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">On-premise options</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700 dark:text-gray-300">Compliance features</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Feature Comparison */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 mb-16">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
            Feature Comparison
          </h2>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="text-left py-4 px-6 font-semibold text-gray-900 dark:text-white">Feature</th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900 dark:text-white">Free</th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900 dark:text-white">Pro</th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900 dark:text-white">Enterprise</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                <tr>
                  <td className="py-4 px-6 text-gray-700 dark:text-gray-300">Screenshots</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">100</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">10,000</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Unlimited</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 text-gray-700 dark:text-gray-300">AI Search</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Basic</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Advanced</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Custom</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 text-gray-700 dark:text-gray-300">API Access</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Basic</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Full</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Full + Custom</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 text-gray-700 dark:text-gray-300">Support</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Email</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Priority</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Dedicated</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 text-gray-700 dark:text-gray-300">Team Size</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">1 user</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Up to 10</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Unlimited</td>
                </tr>
                <tr>
                  <td className="py-4 px-6 text-gray-700 dark:text-gray-300">Storage</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">5 GB</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">100 GB</td>
                  <td className="py-4 px-6 text-center text-gray-700 dark:text-gray-300">Custom</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 mb-16">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
            Frequently Asked Questions
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Can I change plans anytime?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Yes! You can upgrade or downgrade your plan at any time. Changes take effect 
                  immediately, and we'll prorate any billing adjustments.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Is there a free trial?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Pro plans come with a 14-day free trial. No credit card required to start 
                  exploring advanced features.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  What payment methods do you accept?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  We accept all major credit cards, PayPal, and bank transfers for enterprise plans.
                </p>
              </div>
            </div>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Do you offer refunds?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  We offer a 30-day money-back guarantee. If you're not satisfied, we'll 
                  refund your payment, no questions asked.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Can I cancel anytime?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Absolutely. You can cancel your subscription at any time from your account 
                  settings. No long-term contracts or cancellation fees.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  What about data retention?
                </h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Your data is retained according to your plan. Free users get 30 days, 
                  Pro users get 1 year, and Enterprise users get custom retention policies.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-white">
            <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
            <p className="text-xl mb-8 max-w-2xl mx-auto">
              Join thousands of users who are already using Visual Memory Search to 
              organize and find their visual content faster than ever.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-8 py-4 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors">
                <DollarSign className="w-5 h-5 inline mr-2" />
                Start Free Trial
              </button>
              <button className="px-8 py-4 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-blue-600 transition-colors">
                <Info className="w-5 h-5 inline mr-2" />
                Schedule Demo
              </button>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

