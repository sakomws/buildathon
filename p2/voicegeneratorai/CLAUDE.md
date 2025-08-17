# Voice-to-Slide Generator - Claude Code Context

## Project Overview
This is a **voice-to-slide generator** web application that transforms 3-minute spoken presentations into professional slide decks with speaker notes. The application uses AI-powered speech recognition and content generation to create 5 structured slides from audio input.

## Architecture & Tech Stack

### Backend (Node.js + Express)
- **Framework**: Express.js server on port 3000
- **File Upload**: Multer for handling audio files (MP3, WAV, M4A)
- **AI Integration**: OpenAI API (Whisper for transcription, GPT-4 for slide generation)
- **File Storage**: Local uploads directory with UUID-based filenames
- **Security**: CORS enabled, file type/size validation (50MB limit)

### Frontend (Vanilla JavaScript + HTML/CSS)
- **Recording**: Web Audio API with MediaRecorder for in-browser recording
- **Upload**: Drag & drop file handling with validation
- **UI**: Modern gradient design (purple-to-blue) with responsive layout
- **Interactions**: Real-time status updates, loading modals, keyboard shortcuts

### AI Components
- **Speech-to-Text**: OpenAI Whisper API for audio transcription
- **Content Generation**: GPT-4 for intelligent slide structure and content
- **Slide Structure**: Fixed 5-slide format (Introduction, Challenge, Strategy, Implementation, Conclusion)

## Key Features
- Upload or record audio (max 3 minutes, 50MB limit)
- Real-time recording with timer and auto-stop
- AI-powered transcription using Whisper
- Professional slide generation with speaker notes
- HTML export functionality (PDF coming soon)
- Responsive design with visual feedback

## File Structure
```
/
├── server.js           # Express server with API endpoints
├── package.json        # Dependencies and scripts
├── public/
│   ├── index.html     # Main UI
│   ├── script.js      # Frontend JavaScript
│   └── styles.css     # CSS styling
├── uploads/           # Audio file storage
├── env.example        # Environment configuration template
└── README.md         # Detailed documentation
```

## API Endpoints
- `GET /api/health` - Application health check
- `POST /api/upload-audio` - Upload audio file
- `POST /api/transcribe` - Transcribe audio with Whisper
- `POST /api/generate-slides` - Generate slides with GPT-4
- `POST /api/export-html` - Export presentation as HTML

## Development Commands
- `npm start` - Start production server
- `npm run dev` - Start with nodemon for development
- `npm run build` - Webpack production build
- `npm test` - Run Jest tests

## Environment Setup
Required environment variables:
- `OPENAI_API_KEY` - OpenAI API key for Whisper and GPT-4
- `PORT` - Server port (default: 3000)
- Optional: `OPENAI_ORG_ID`, voice settings

## Dependencies
Key packages:
- express, cors, multer - Web server and file handling
- openai - OpenAI API integration
- dotenv - Environment configuration
- fluent-ffmpeg - Audio processing utilities
- uuid - Unique file naming
- fs-extra - Enhanced file system operations

## Usage Flow
1. User uploads audio or records in browser
2. Audio file is uploaded to server
3. Whisper API transcribes speech to text
4. GPT-4 generates structured 5-slide presentation
5. Results displayed with export options
6. User can download as HTML presentation

## Known Limitations
- PDF export not yet implemented
- Local file storage (no cloud integration)
- No user authentication or session management
- Limited to English language processing
- 3-minute recording limit for quality optimization

## Future Enhancements
- PDF export functionality
- User authentication and presentation history
- Multiple presentation templates
- Cloud storage integration
- Collaboration features
- Analytics and usage tracking