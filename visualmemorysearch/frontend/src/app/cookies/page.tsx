'use client';
import React, { useEffect, useState } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { Cookie, Settings, Info, Shield, Database, Eye, CheckCircle } from 'lucide-react';
import { getCookiePreferences, setCookiePreferences } from '@/lib/api';
import type { CookiePreferences } from '@/types/api';

// Disable static generation for this page
export const dynamic = 'force-dynamic';

export default function CookiePolicy() {
  const [prefs, setPrefs] = useState<CookiePreferences>({ essential: true, functional: false, analytics: false, marketing: false });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await getCookiePreferences();
        setPrefs({
          essential: true,
          functional: !!data.functional,
          analytics: !!data.analytics,
          marketing: !!data.marketing,
        });
      } catch (e) {
        // default stays
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const acceptAll = async () => {
    await savePrefs({ essential: true, functional: true, analytics: true, marketing: true });
  };
  const rejectNonEssential = async () => {
    await savePrefs({ essential: true, functional: false, analytics: false, marketing: false });
  };
  const savePrefs = async (next: CookiePreferences) => {
    try {
      setSaving(true);
      const res = await setCookiePreferences(next);
      setPrefs(res.preferences);
      setMessage('Preferences saved');
      setTimeout(() => setMessage(null), 2000);
    } catch (e) {
      setMessage('Failed to save preferences');
      setTimeout(() => setMessage(null), 3000);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <Cookie className="h-16 w-16 text-blue-600 dark:text-blue-400" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Cookie Policy
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Last updated: {new Date().toLocaleDateString()}
            </p>
          </div>

          {/* Content */}
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Info className="h-6 w-6 mr-2 text-blue-600" />
                What Are Cookies?
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>
                  Cookies are small text files that are placed on your device when you visit our website. 
                  They help us provide you with a better experience by remembering your preferences and 
                  analyzing how you use our service.
                </p>
                <p>
                  Cookies can be "session cookies" (which are deleted when you close your browser) or 
                  "persistent cookies" (which remain on your device for a set period of time).
                </p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Settings className="h-6 w-6 mr-2 text-green-600" />
                How We Use Cookies
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>We use cookies for the following purposes:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li><strong>Essential Cookies:</strong> Required for the website to function properly</li>
                  <li><strong>Authentication Cookies:</strong> To keep you signed in and secure</li>
                  <li><strong>Preference Cookies:</strong> To remember your settings and preferences</li>
                  <li><strong>Analytics Cookies:</strong> To understand how visitors use our service</li>
                  <li><strong>Performance Cookies:</strong> To optimize website performance</li>
                </ul>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Database className="h-6 w-6 mr-2 text-purple-600" />
                Types of Cookies We Use
              </h2>
              <div className="space-y-6 text-gray-700 dark:text-gray-300">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Essential Cookies</h3>
                  <p>
                    These cookies are necessary for the website to function and cannot be switched off. 
                    They are usually only set in response to actions made by you, such as setting your 
                    privacy preferences, logging in, or filling in forms.
                  </p>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Functional Cookies</h3>
                  <p>
                    These cookies enable the website to provide enhanced functionality and personalization. 
                    They may be set by us or by third-party providers whose services we have added to our pages.
                  </p>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Analytics Cookies</h3>
                  <p>
                    These cookies allow us to count visits and traffic sources so we can measure and 
                    improve the performance of our site. They help us know which pages are the most and 
                    least popular and see how visitors move around the site.
                  </p>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Marketing Cookies</h3>
                  <p>
                    These cookies may be set through our site by our advertising partners. They may be 
                    used by those companies to build a profile of your interests and show you relevant 
                    advertisements on other sites.
                  </p>
                </div>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Eye className="h-6 w-6 mr-2 text-orange-600" />
                Third-Party Cookies
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>
                  In addition to our own cookies, we may also use various third-party cookies to report 
                  usage statistics of the service, deliver advertisements on and through the service, and so on.
                </p>
                <p>Third-party services we use include:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li><strong>Google Analytics:</strong> For website analytics and performance monitoring</li>
                  <li><strong>Google OAuth:</strong> For user authentication and sign-in services</li>
                  <li><strong>GitHub OAuth:</strong> For user authentication and sign-in services</li>
                  <li><strong>Cloudflare:</strong> For content delivery and security services</li>
                </ul>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Shield className="h-6 w-6 mr-2 text-indigo-600" />
                Managing Your Cookie Preferences
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>You have several options for managing cookies:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li><strong>Browser Settings:</strong> Most browsers allow you to control cookies through their settings</li>
                  <li><strong>Cookie Consent:</strong> Use our cookie consent banner to manage preferences</li>
                  <li><strong>Third-Party Opt-Out:</strong> Opt out of specific third-party services</li>
                  <li><strong>Delete Cookies:</strong> Remove existing cookies from your device</li>
                </ul>
                <p>
                  Please note that disabling certain cookies may affect the functionality of our website.
                </p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <CheckCircle className="h-6 w-6 mr-2 text-green-600" />
                Your Rights and Choices
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>Under applicable data protection laws, you have the right to:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Access information about cookies we use</li>
                  <li>Opt out of non-essential cookies</li>
                  <li>Request deletion of your data</li>
                  <li>Withdraw consent for cookie usage</li>
                  <li>Lodge a complaint with supervisory authorities</li>
                </ul>
                <p>
                  To exercise these rights, please contact us using the information provided below.
                </p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Updates to This Policy
              </h2>
              <div className="space-y-4 text-gray-700 dark:text-gray-300">
                <p>
                  We may update this Cookie Policy from time to time to reflect changes in our practices 
                  or for other operational, legal, or regulatory reasons.
                </p>
                <p>
                  We will notify you of any material changes by posting the new Cookie Policy on this page 
                  and updating the "Last updated" date at the top of this policy.
                </p>
              </div>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Contact Us
              </h2>
              <div className="text-gray-700 dark:text-gray-300">
                <p>
                  If you have any questions about our use of cookies or this Cookie Policy, 
                  please contact us at:
                </p>
                <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="font-medium">Visual Memory Search</p>
                  <p>Email: privacy@visualmemorysearch.com</p>
                  <p>Address: [Your Company Address]</p>
                </div>
              </div>
            </section>

            {/* Cookie Consent Management */}
            <section className="mt-12 p-6 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700">
              <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
                Cookie Consent Management
              </h3>
              <p className="text-blue-800 dark:text-blue-200 mb-4">
                You can manage your cookie preferences at any time using the settings below:
              </p>
              {message && (
                <div className="mb-3 text-sm text-green-800 dark:text-green-200">{message}</div>
              )}
              <div className="flex flex-wrap gap-3 items-center">
                <button onClick={acceptAll} disabled={saving} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg transition-colors">
                  Accept All Cookies
                </button>
                <button onClick={rejectNonEssential} disabled={saving} className="px-4 py-2 bg-gray-600 hover:bg-gray-700 disabled:opacity-50 text-white rounded-lg transition-colors">
                  Reject Non-Essential
                </button>
              </div>

              {/* Customize */}
              <div className="mt-6 grid sm:grid-cols-2 gap-4">
                <label className="flex items-center justify-between p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                  <span className="text-gray-800 dark:text-gray-200">Essential (required)</span>
                  <input type="checkbox" checked readOnly className="h-5 w-5" />
                </label>
                <label className="flex items-center justify-between p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                  <span className="text-gray-800 dark:text-gray-200">Functional</span>
                  <input
                    type="checkbox"
                    checked={prefs.functional}
                    onChange={(e) => setPrefs({ ...prefs, functional: e.target.checked })}
                    className="h-5 w-5"
                  />
                </label>
                <label className="flex items-center justify-between p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                  <span className="text-gray-800 dark:text-gray-200">Analytics</span>
                  <input
                    type="checkbox"
                    checked={prefs.analytics}
                    onChange={(e) => setPrefs({ ...prefs, analytics: e.target.checked })}
                    className="h-5 w-5"
                  />
                </label>
                <label className="flex items-center justify-between p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                  <span className="text-gray-800 dark:text-gray-200">Marketing</span>
                  <input
                    type="checkbox"
                    checked={prefs.marketing}
                    onChange={(e) => setPrefs({ ...prefs, marketing: e.target.checked })}
                    className="h-5 w-5"
                  />
                </label>
              </div>
              <div className="mt-4">
                <button onClick={() => savePrefs(prefs)} disabled={saving} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg transition-colors">
                  {saving ? 'Saving...' : 'Save Preferences'}
                </button>
              </div>
            </section>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
