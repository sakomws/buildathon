# Voice-to-Slide Generator 🎤➡️📊

Transform your 3-minute spoken presentation into a professional, AI-powered slide deck with speaker notes in seconds.

![Voice-to-Slide Generator](https://img.shields.io/badge/Status-Ready-brightgreen)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4%20%2B%20Whisper-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🎯 Core Functionality
- **Audio Input Options**: Upload audio files (MP3, WAV, M4A) or record directly in-browser
- **3-minute Recording Limit**: Built-in timer and auto-stop functionality
- **Real-time Processing**: Visual progress indicators and status updates
- **5-Slide Generation**: Professional presentation structure with speaker notes

### 🎨 Design Features
- **Modern Interface**: Beautiful purple-to-blue gradient design
- **Responsive Layout**: Works perfectly on desktop and mobile devices
- **Professional UI**: Clean, intuitive user experience
- **Visual Feedback**: Progress bars, loading states, and status messages

### 🧠 Technical Capabilities
- **Speech Recognition**: OpenAI Whisper API for accurate transcription
- **AI Content Generation**: GPT-4 powered slide structuring
- **Export Options**: HTML download (PDF coming soon)
- **Speaker Notes**: Detailed notes for each slide
- **File Size Limits**: 50MB max for uploaded files

## 🚀 Quick Start

### Prerequisites
- Node.js (v14 or higher)
- OpenAI API key
- Modern web browser with microphone access

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd voice-to-slide-generator
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

4. **Start the application**
   ```bash
   npm start
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 📋 Usage Guide

### Recording Audio
1. Click **"Start Recording"** or press **Spacebar**
2. Speak clearly into your microphone
3. Recording automatically stops after 3 minutes
4. Click **"Stop Recording"** to finish early

### Uploading Audio Files
1. Drag & drop audio files onto the upload area
2. Or click to browse and select files
3. Supported formats: MP3, WAV, M4A
4. Maximum file size: 50MB

### Processing & Results
1. Audio is automatically transcribed using OpenAI Whisper
2. AI generates 5 professional slides with speaker notes
3. Review your presentation in the results section
4. Export as HTML for immediate use

## 🏗️ Architecture

### Backend (Node.js + Express)
- **File Upload**: Multer for handling audio file uploads
- **Audio Processing**: OpenAI Whisper API integration
- **Content Generation**: OpenAI GPT-4 for slide creation
- **Export System**: HTML generation with professional styling

### Frontend (Vanilla JavaScript)
- **Audio Recording**: Web Audio API with MediaRecorder
- **File Handling**: Drag & drop with validation
- **Real-time Updates**: Progress indicators and status messages
- **Responsive Design**: Mobile-first approach

### AI Integration
- **Speech-to-Text**: OpenAI Whisper for accurate transcription
- **Content Generation**: GPT-4 for intelligent slide structuring
- **Professional Formatting**: Structured 5-slide presentations

## 📊 Slide Structure

Each generated presentation follows this professional structure:

1. **Introduction & Overview** - Sets context and roadmap
2. **Key Challenge & Context** - Identifies problems and urgency
3. **Core Strategy & Approach** - Main solution framework
4. **Implementation & Results** - Execution plan and outcomes
5. **Conclusion & Next Steps** - Summary and call-to-action

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/upload-audio` | POST | Upload audio file |
| `/api/transcribe` | POST | Transcribe audio with Whisper |
| `/api/generate-slides` | POST | Generate slides with GPT-4 |
| `/api/export-html` | POST | Export presentation as HTML |

## 🛠️ Development

### Running in Development Mode
```bash
npm run dev
```

### Building for Production
```bash
npm run build
```

### Running Tests
```bash
npm test
```

## 🔒 Security & Best Practices

- ✅ **Environment Variables**: API keys stored securely
- ✅ **File Validation**: Type and size restrictions
- ✅ **Error Handling**: Comprehensive error management
- ✅ **Input Sanitization**: XSS protection
- ✅ **CORS Configuration**: Proper cross-origin setup

## 🚧 Future Enhancements

### Planned Features
- [ ] **PDF Export**: Server-side PDF generation
- [ ] **User Authentication**: Login and user management
- [ ] **Presentation Templates**: Multiple design themes
- [ ] **Collaboration**: Share and edit presentations
- [ ] **Analytics**: Usage statistics and insights

### Technical Improvements
- [ ] **WebSocket Integration**: Real-time progress updates
- [ ] **Caching System**: Improve performance
- [ ] **Database Integration**: Store presentation history
- [ ] **Cloud Storage**: Audio file management
- [ ] **API Rate Limiting**: Prevent abuse

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing GPT-4 and Whisper APIs
- **Font Awesome** for beautiful icons
- **Express.js** for the robust backend framework
- **Modern CSS** for stunning visual design

## 📞 Support

- **Documentation**: Check this README for setup and usage
- **Issues**: Report bugs via GitHub Issues
- **Questions**: Open a discussion for general questions
- **Help**: Click the help icon (?) in the bottom-right corner

---

**Made with ❤️ for better presentations**
