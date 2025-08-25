# Visual Memory Search - System Architecture

## Overview

Visual Memory Search is a full-stack web application that provides AI-powered screenshot organization and search capabilities. The system is built with a microservices architecture, featuring a FastAPI backend and a Next.js frontend.

## System Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   Services      │
│                 │    │                 │    │                 │
│ • React App     │    │ • REST API      │    │ • OpenAI API    │
│ • Tailwind CSS  │    │ • Auth Service  │    │ • Google OAuth  │
│ • TypeScript    │    │ • Search Engine │    │ • GitHub OAuth  │
└─────────────────┘    │ • File Storage  │    │ • reCAPTCHA     │
                       └─────────────────┘    └─────────────────┘
```

## Core Components

### 1. Frontend (Next.js)

**Technology Stack:**
- **Framework:** Next.js 14 with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS v4
- **State Management:** React Context API
- **HTTP Client:** Axios
- **Icons:** Lucide React
- **Build Tool:** Webpack with Next.js

**Key Features:**
- Responsive design with mobile-first approach
- Dark/light mode support (removed due to issues)
- OAuth authentication integration
- Real-time search and filtering
- Drag & drop file upload
- Image viewer with zoom capabilities
- Role-based access control (RBAC)

**Architecture Patterns:**
- Component-based architecture
- Custom hooks for business logic
- Context providers for global state
- Server-side rendering (SSR) and static generation
- API route proxying to backend

### 2. Backend (FastAPI)

**Technology Stack:**
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **ASGI Server:** Uvicorn
- **Data Validation:** Pydantic v2
- **Authentication:** JWT with python-jose
- **Password Hashing:** passlib with bcrypt
- **HTTP Client:** httpx
- **Image Processing:** OpenCV, Pillow
- **OCR:** pytesseract
- **ML/AI:** transformers, sentence-transformers, scikit-learn

**Key Services:**

#### Authentication Service
- OAuth 2.0 integration (Google, GitHub)
- JWT token management
- Password-based authentication
- User session management

#### RBAC Service
- Role-based access control
- Permission management
- User profile management
- Data isolation per user

#### Visual Search Service
- Image feature extraction
- Text extraction (OCR)
- Vector embeddings generation
- Similarity search algorithms
- Index management

#### File Management Service
- File upload handling
- Storage path management
- File validation and processing
- Bulk operations support

### 3. Data Layer

**Storage Structure:**
```
/app
├── screenshots/          # Global screenshot storage
├── user_data/           # User-specific data
│   └── user_{id}/      # Individual user storage
│       ├── screenshots/ # User screenshots
│       ├── indexes/     # Search indexes
│       └── embeddings/  # Feature vectors
└── logs/               # Application logs
```

**Data Models:**
- **User:** Authentication and profile information
- **UserProfile:** Extended user data and preferences
- **ScreenshotInfo:** Image metadata and features
- **SearchResult:** Search query results
- **CookiePreferences:** User cookie consent settings

### 4. External Integrations

#### OpenAI Integration
- API key management per user
- Text embedding generation
- AI-powered search enhancement
- Usage analytics tracking

#### OAuth Providers
- **Google OAuth 2.0:** User authentication and profile data
- **GitHub OAuth:** Developer-focused authentication
- **Email/Password:** Traditional authentication fallback

#### Security Services
- **reCAPTCHA v3:** Bot protection on registration
- **JWT:** Secure token-based authentication
- **HTTPS:** Encrypted data transmission

## Security Architecture

### Authentication Flow
1. User initiates OAuth or email login
2. Backend validates credentials
3. JWT token generated and returned
4. Frontend stores token securely
5. Token included in subsequent API calls

### Data Protection
- **Encryption:** All sensitive data encrypted at rest
- **Isolation:** User data completely separated
- **Access Control:** RBAC with fine-grained permissions
- **Audit Logging:** Complete activity tracking

### API Security
- **Rate Limiting:** Request throttling per user
- **Input Validation:** Pydantic schema validation
- **CORS:** Cross-origin resource sharing configuration
- **HTTPS:** TLS encryption for all communications

## Performance Considerations

### Frontend Optimization
- **Code Splitting:** Dynamic imports for route-based splitting
- **Image Optimization:** Next.js built-in image optimization
- **Bundle Analysis:** Webpack bundle analyzer integration
- **Caching:** Static asset caching strategies

### Backend Optimization
- **Async Processing:** FastAPI async/await patterns
- **Database Indexing:** Efficient search index structures
- **Caching:** Redis integration for session storage
- **Load Balancing:** Horizontal scaling capabilities

### Search Performance
- **Vector Indexing:** Efficient similarity search
- **Lazy Loading:** Progressive image loading
- **Pagination:** Result pagination for large datasets
- **Query Optimization:** Search query caching

## Scalability Features

### Horizontal Scaling
- **Stateless Backend:** No server-side session storage
- **Load Balancer Ready:** Multiple backend instances
- **Database Sharding:** User-based data partitioning
- **CDN Integration:** Static asset distribution

### Microservices Ready
- **Service Separation:** Clear service boundaries
- **API Gateway:** Centralized routing and authentication
- **Message Queues:** Async task processing
- **Health Checks:** Service monitoring and recovery

## Monitoring and Observability

### Logging
- **Structured Logging:** JSON-formatted log entries
- **Log Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Rotation:** Automated log file management
- **Centralized Logging:** Log aggregation and analysis

### Metrics
- **Performance Metrics:** Response time, throughput
- **Business Metrics:** User activity, search patterns
- **System Metrics:** CPU, memory, disk usage
- **Custom Metrics:** OpenAI API usage, file uploads

### Health Checks
- **Service Health:** Backend API availability
- **Dependency Health:** External service connectivity
- **Resource Health:** System resource monitoring
- **Automated Recovery:** Self-healing capabilities

## Deployment Architecture

### Containerization
- **Docker Images:** Optimized container images
- **Multi-stage Builds:** Efficient image construction
- **Health Checks:** Container health monitoring
- **Resource Limits:** CPU and memory constraints

### Orchestration
- **Docker Compose:** Local development environment
- **Kubernetes Ready:** Production deployment support
- **Service Discovery:** Dynamic service registration
- **Auto-scaling:** Automatic resource scaling

### Environment Management
- **Configuration:** Environment-specific settings
- **Secrets Management:** Secure credential storage
- **Feature Flags:** Runtime feature toggling
- **A/B Testing:** User experience experimentation

## Future Enhancements

### Planned Features
- **Real-time Collaboration:** Multi-user editing
- **Advanced Analytics:** User behavior insights
- **Mobile Apps:** Native iOS and Android applications
- **API Marketplace:** Third-party integrations

### Technical Improvements
- **GraphQL:** Flexible data querying
- **WebSockets:** Real-time updates
- **Service Mesh:** Advanced service communication
- **Machine Learning:** Enhanced AI capabilities

## Conclusion

The Visual Memory Search architecture is designed for scalability, security, and maintainability. The separation of concerns between frontend and backend, combined with modern technologies and best practices, provides a solid foundation for future growth and feature development.

The system's modular design allows for easy updates and extensions while maintaining high performance and security standards. The containerization approach ensures consistent deployment across different environments, from development to production.
