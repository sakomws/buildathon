# Visual Memory Search - Documentation

Welcome to the Visual Memory Search project documentation. This folder contains comprehensive documentation for the entire system.

## 📚 Documentation Index

### 🚀 Getting Started
- **[STARTUP_GUIDE.md](./STARTUP_GUIDE.md)** - Complete setup and installation guide
- **[README_FASTAPI.md](./README_FASTAPI.md)** - FastAPI backend documentation

### 🔌 API Documentation
- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API reference and usage examples
- **[API_TEST_REPORT.md](./API_TEST_REPORT.md)** - API testing results and validation

### 🌐 Deployment & Infrastructure
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Deployment guides and configuration
- **[PUBLIC_URL.md](./PUBLIC_URL.md)** - Public deployment and URL management

## 🏗️ Project Structure

```
p1/
├── app/                    # FastAPI backend application
│   ├── config/            # Configuration management
│   ├── models/            # Data models and schemas
│   ├── services/          # Business logic services
│   └── utils/             # Utility functions
├── frontend/              # Next.js frontend application
│   ├── src/               # Source code
│   │   ├── app/           # Next.js app router
│   │   ├── lib/           # Utility libraries
│   │   └── types/         # TypeScript type definitions
│   └── tests/             # Frontend tests
├── docs/                  # Documentation (this folder)
├── tests/                 # Backend tests
└── test_screenshots/      # Test data and screenshots
```

## 🧪 Testing

### Backend Testing
- Run API tests: `python test_api_endpoints.py`
- Run FastAPI tests: `python test_fastapi.py`
- Run search tests: `python test_search.py`

### Frontend Testing
- Unit tests: `npm test`
- E2E tests: `npm run test:e2e`
- Coverage: `npm run test:coverage`

## 🚀 Quick Start

1. **Backend**: `python run_fastapi.py`
2. **Frontend**: `cd frontend && npm run dev`
3. **Access**: http://localhost:3000

## 📖 Additional Resources

- **API Docs**: http://localhost:8000/docs (when backend is running)
- **Test Results**: Check `api_test_results.json` for detailed test data
- **Logs**: Check `app.log` for application logs

## 🤝 Contributing

When adding new documentation:
1. Place it in the appropriate section
2. Update this README.md index
3. Follow the existing documentation format
4. Include examples and code snippets where relevant

## 📝 Documentation Standards

- Use clear, concise language
- Include code examples
- Provide step-by-step instructions
- Keep documentation up-to-date with code changes
- Use consistent formatting and structure
