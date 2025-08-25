import { NextRequest, NextResponse } from 'next/server';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  try {
    const resolvedParams = await params;
    const filename = resolvedParams.path.join('/');
    const response = await fetch(`${API_BASE_URL}/api/screenshots/${filename}`);

    if (!response.ok) {
      return new NextResponse('Screenshot not found', { status: 404 });
    }

    const buffer = await response.arrayBuffer();
    const headers = new Headers();

    // Set appropriate content type based on file extension
    if (filename.endsWith('.png')) {
      headers.set('Content-Type', 'image/png');
    } else if (filename.endsWith('.jpg') || filename.endsWith('.jpeg')) {
      headers.set('Content-Type', 'image/jpeg');
    } else if (filename.endsWith('.gif')) {
      headers.set('Content-Type', 'image/gif');
    } else if (filename.endsWith('.bmp')) {
      headers.set('Content-Type', 'image/bmp');
    } else {
      headers.set('Content-Type', 'application/octet-stream');
    }

    // Cache the image for 1 hour
    headers.set('Cache-Control', 'public, max-age=3600');

    return new NextResponse(buffer, {
      status: 200,
      headers,
    });
  } catch (error) {
    console.error('Error fetching screenshot:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
