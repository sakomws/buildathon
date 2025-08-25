import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  const { baseURL } = config.projects[0].use;
  
  console.log('🚀 Starting global setup...');
  
  // Check if backend is running
  try {
    const response = await fetch('http://localhost:8000/api/health');
    if (response.ok) {
      console.log('✅ Backend is running and healthy');
    } else {
      console.log('⚠️ Backend is running but not healthy');
    }
  } catch (error) {
    console.log('❌ Backend is not running. Please start the backend first.');
    console.log('   Run: python run_fastapi.py');
    process.exit(1);
  }

  // Check if frontend is accessible
  try {
    const response = await fetch(baseURL || 'http://localhost:3000');
    if (response.ok) {
      console.log('✅ Frontend is accessible');
    } else {
      console.log('⚠️ Frontend is accessible but returned status:', response.status);
    }
  } catch (error) {
    console.log('❌ Frontend is not accessible. Please start the frontend first.');
    console.log('   Run: cd frontend && npm run dev');
    process.exit(1);
  }

  // Create test data if needed
  console.log('📝 Setting up test data...');
  
  // You can add test data setup here if needed
  // For example, creating test screenshots, etc.
  
  console.log('✅ Global setup completed successfully');
}

export default globalSetup;
