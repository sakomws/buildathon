

import React from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { FileText, Shield, AlertTriangle, CheckCircle, Users, Globe, Scale } from 'lucide-react';

// Disable static generation for this page
export const dynamic = 'force-dynamic';

export default function TermsOfService() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <Scale className="h-16 w-16 text-blue-600 dark:text-blue-400" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Terms of Service
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Last updated: {new Date().toLocaleDateString()}
            </p>
          </div>

          {/* Content */}
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <FileText className="h-6 w-6 mr-2 text-blue-600" />
                Acceptance of Terms
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>
                  By accessing and using Visual Memory Search ("the Service"), you accept and agree to be bound by the terms and provision of this agreement.
                </p>
                <p>
                  If you do not agree to abide by the above, please do not use this service. These terms apply to all visitors, users, and others who access or use the Service.
                </p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Users className="h-6 w-6 mr-2 text-green-600" />
                Use License
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>Permission is granted to temporarily use the Service for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Modify or copy the materials</li>
                  <li>Use the materials for any commercial purpose or for any public display</li>
                  <li>Attempt to reverse engineer any software contained in the Service</li>
                  <li>Remove any copyright or other proprietary notations from the materials</li>
                  <li>Transfer the materials to another person or "mirror" the materials on any other server</li>
                </ul>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Shield className="h-6 w-6 mr-2 text-purple-600" />
                User Responsibilities
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>As a user of the Service, you agree to:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Provide accurate and complete information when creating your account</li>
                  <li>Maintain the security of your account credentials</li>
                  <li>Not upload content that violates intellectual property rights</li>
                  <li>Not use the Service for any illegal or unauthorized purpose</li>
                  <li>Not interfere with or disrupt the Service or servers</li>
                  <li>Comply with all applicable laws and regulations</li>
                </ul>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <AlertTriangle className="h-6 w-6 mr-2 text-orange-600" />
                Prohibited Uses
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>You may not use the Service to:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Upload malicious software, viruses, or harmful code</li>
                  <li>Harass, abuse, or harm other users</li>
                  <li>Violate any applicable laws or regulations</li>
                  <li>Infringe on intellectual property rights</li>
                  <li>Attempt to gain unauthorized access to the Service</li>
                  <li>Use automated systems to access the Service</li>
                </ul>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Globe className="h-6 w-6 mr-2 text-indigo-600" />
                Service Availability
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>
                  We strive to maintain high availability of the Service, but we do not guarantee that the Service will be available at all times. The Service may be temporarily unavailable due to:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Scheduled maintenance and updates</li>
                  <li>Technical issues or system failures</li>
                  <li>Network connectivity problems</li>
                  <li>Force majeure events beyond our control</li>
                </ul>
                <p>
                  We will make reasonable efforts to notify users of planned maintenance and to minimize service disruptions.
                </p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <CheckCircle className="h-6 w-6 mr-2 text-green-600" />
                Intellectual Property
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>
                  The Service and its original content, features, and functionality are and will remain the exclusive property of Visual Memory Search and its licensors. The Service is protected by copyright, trademark, and other laws.
                </p>
                <p>
                  You retain ownership of content you upload to the Service, but you grant us a license to use, store, and process that content to provide the Service.
                </p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Limitation of Liability
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>
                  In no event shall Visual Memory Search, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your use of the Service.
                </p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Changes to Terms
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>
                  We reserve the right to modify or replace these Terms at any time. If a revision is material, we will try to provide at least 30 days notice prior to any new terms taking effect.
                </p>
                <p>
                  Your continued use of the Service after any changes constitutes acceptance of the new Terms.
                </p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Contact Information
              </h2>
              <div className="text-gray-700 dark:text-gray-300">
                <p>
                  If you have any questions about these Terms of Service, please contact us at:
                </p>
                <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="font-medium">Visual Memory Search</p>
                  <p>Email: legal@visualmemorysearch.com</p>
                  <p>Address: [Your Company Address]</p>
                </div>
              </div>
            </section>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
