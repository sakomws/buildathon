import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@/components/Auth/AuthProvider'

const inter = Inter({ subsets: ['latin'] })

// Disable static generation globally
export const dynamic = 'force-dynamic';

export const metadata: Metadata = {
  title: 'Visual Memory Search',
  description: 'AI-powered screenshot search and management system',
  keywords: ['screenshot', 'search', 'AI', 'visual', 'memory', 'management'],
  authors: [{ name: 'Visual Memory Search Team' }],
  creator: 'Visual Memory Search',
  publisher: 'Visual Memory Search',
  robots: 'index, follow',
  openGraph: {
    title: 'Visual Memory Search',
    description: 'AI-powered screenshot search and management system',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Visual Memory Search',
    description: 'AI-powered screenshot search and management system',
  },
  icons: {
    icon: [
      { url: '/favicon.svg', type: 'image/svg+xml' },
      { url: '/favicon.ico', sizes: 'any' }
    ],
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        {/* No inline scripts - let React handle dark mode */}
      </head>
      <body className={inter.className}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
