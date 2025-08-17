const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs-extra');
const { v4: uuidv4 } = require('uuid');
const OpenAI = require('openai');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize OpenAI
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // Use /tmp for Vercel serverless functions
    const uploadDir = process.env.VERCEL ? '/tmp/uploads/' : 'uploads/';
    fs.ensureDirSync(uploadDir);
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueName = `${uuidv4()}-${file.originalname}`;
    cb(null, uniqueName);
  }
});

const upload = multer({
  storage: storage,
  limits: {
    fileSize: 50 * 1024 * 1024, // 50MB limit
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['audio/mp3', 'audio/wav', 'audio/m4a', 'audio/mpeg', 'audio/mp4', 'audio/x-m4a'];
    const fileName = file.originalname.toLowerCase();
    const allowedExtensions = ['.mp3', '.wav', '.m4a'];
    
    const hasValidMimeType = allowedTypes.includes(file.mimetype);
    const hasValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));
    
    // Accept file if either MIME type OR extension is valid
    if (hasValidMimeType || hasValidExtension) {
      cb(null, true);
    } else {
      console.log('File rejected:', file.mimetype, file.originalname);
      cb(new Error('Invalid file type. Only MP3, WAV, and M4A files are allowed.'), false);
    }
  }
});

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'Application is working', timestamp: new Date().toISOString() });
});

// Test OpenAI connection
app.get('/api/test-openai', async (req, res) => {
  try {
    const hasKey = !!process.env.OPENAI_API_KEY;
    const keyPrefix = process.env.OPENAI_API_KEY ? process.env.OPENAI_API_KEY.substring(0, 12) + '...' : 'Not Set';
    
    res.json({
      status: 'OpenAI API Key Check',
      hasApiKey: hasKey,
      keyPrefix: keyPrefix,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      error: 'Failed to check OpenAI configuration',
      details: error.message
    });
  }
});

// Upload and process audio
app.post('/api/upload-audio', upload.single('audio'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No audio file provided' });
    }

    const filePath = req.file.path;
    const fileName = req.file.filename;

    res.json({
      success: true,
      message: 'Audio file uploaded successfully',
      fileName: fileName,
      filePath: filePath
    });

  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ 
      error: 'Failed to upload audio file',
      details: error.message
    });
  }
});

// Process audio with OpenAI Whisper
app.post('/api/transcribe', async (req, res) => {
  try {
    const { filePath } = req.body;
    
    if (!filePath) {
      return res.status(400).json({ error: 'File path is required' });
    }

    // Check if file exists
    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ error: 'Audio file not found' });
    }

    // Transcribe audio using OpenAI Whisper
    const transcription = await openai.audio.transcriptions.create({
      file: fs.createReadStream(filePath),
      model: "whisper-1",
      response_format: "text"
    });

    res.json({
      success: true,
      transcript: transcription,
      wordCount: transcription.split(' ').length
    });

  } catch (error) {
    console.error('Transcription error:', error);
    console.error('Error details:', {
      message: error.message,
      status: error.status,
      type: error.type,
      code: error.code
    });
    res.status(500).json({ 
      error: 'Failed to transcribe audio',
      details: error.message,
      apiKey: process.env.OPENAI_API_KEY ? 'Set' : 'Not Set'
    });
  }
});

// Generate slides from transcript
app.post('/api/generate-slides', async (req, res) => {
  try {
    const { transcript } = req.body;
    
    if (!transcript) {
      return res.status(400).json({ error: 'Transcript is required' });
    }

    // Check transcript length and adjust approach
    const wordCount = transcript.split(' ').length;
    const isShortTranscript = wordCount < 20;
    
    // Generate slides using OpenAI GPT-4
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: `You are a professional presentation designer. Create a 5-slide presentation based on the provided transcript.
          
          ${isShortTranscript ? 
            `IMPORTANT: The transcript is very short (${wordCount} words). This might be a test phrase or incomplete content. 
            Please create a demonstration presentation that acknowledges this limitation while showing the presentation structure.` :
            'The transcript contains substantial content for a full presentation.'
          }
          
          Structure the slides as follows:
          1. Introduction & Overview - Sets context and roadmap
          2. Key Challenge & Context - Identifies problems and urgency  
          3. Core Strategy & Approach - Main solution framework
          4. Implementation & Results - Execution plan and outcomes
          5. Conclusion & Next Steps - Summary and call-to-action
          
          For each slide, provide:
          - A clear, concise title
          - 3-5 key bullet points
          - Detailed speaker notes (2-3 sentences)
          
          ${isShortTranscript ? 
            `For this short transcript, create slides that demonstrate the format while noting that more detailed content would be needed for a complete presentation.` :
            ''
          }
          
          Return the response as JSON with this structure:
          {
            "slides": [
              {
                "title": "Slide Title",
                "content": ["Bullet point 1", "Bullet point 2", "Bullet point 3"],
                "speakerNotes": "Detailed speaker notes for this slide"
              }
            ]
          }`
        },
        {
          role: "user",
          content: `Generate a professional 5-slide presentation based on this transcript: ${transcript}`
        }
      ],
      temperature: 0.7,
      max_tokens: 2000
    });

    const response = completion.choices[0].message.content;
    let slides;
    
    try {
      slides = JSON.parse(response);
    } catch (parseError) {
      // Fallback if JSON parsing fails
      slides = {
        slides: [
          {
            title: "Introduction",
            content: ["Content extracted from transcript"],
            speakerNotes: "Speaker notes for introduction"
          }
        ]
      };
    }

    res.json({
      success: true,
      slides: slides.slides || slides
    });

  } catch (error) {
    console.error('Slide generation error:', error);
    res.status(500).json({ error: 'Failed to generate slides' });
  }
});

// Export slides as HTML
app.post('/api/export-html', async (req, res) => {
  try {
    const { slides } = req.body;
    
    if (!slides || !Array.isArray(slides)) {
      return res.status(400).json({ error: 'Valid slides data is required' });
    }

    const htmlContent = generateHTML(slides);
    
    res.setHeader('Content-Type', 'text/html');
    res.setHeader('Content-Disposition', 'attachment; filename="presentation.html"');
    res.send(htmlContent);

  } catch (error) {
    console.error('Export error:', error);
    res.status(500).json({ error: 'Failed to export slides' });
  }
});

// Helper function to generate HTML
function generateHTML(slides) {
  const slideIcons = ['🎯', '⚡', '🚀', '⚙️', '✅'];
  const slideGradients = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  ];
  
  const slideHTML = slides.map((slide, index) => {
    const slideNumber = index + 1;
    const slideIcon = slideIcons[index] || '📊';
    const gradient = slideGradients[index] || slideGradients[0];
    const textColor = (slideNumber === 4 || slideNumber === 5) ? '#1a202c' : 'white';
    
    return `
    <div class="slide" style="
      page-break-after: always; 
      margin-bottom: 60px;
      background: ${gradient};
      color: ${textColor};
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
      position: relative;
      aspect-ratio: 16 / 10;
      min-height: 600px;
    ">
      <div style="
        padding: 60px;
        height: 100%;
        display: flex;
        flex-direction: column;
        position: relative;
        box-sizing: border-box;
      ">
        <div style="
          position: absolute;
          top: 30px;
          right: 40px;
          background: rgba(255, 255, 255, 0.2);
          color: inherit;
          width: 50px;
          height: 50px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 18px;
          font-weight: 700;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.3);
        ">${slideNumber}</div>
        
        <h1 style="
          font-size: 3.5rem;
          font-weight: 800;
          margin-bottom: 40px;
          line-height: 1.1;
          letter-spacing: -0.02em;
          margin-top: 0;
        ">${slide.title}</h1>
        
        <ul style="
          list-style: none;
          margin: 0;
          padding: 0;
          flex: 1;
        ">
          ${slide.content.map(point => `
            <li style="
              padding: 15px 0;
              font-size: 1.8rem;
              line-height: 1.4;
              position: relative;
              padding-left: 50px;
              margin-bottom: 20px;
              font-weight: 500;
            ">
              <span style="
                position: absolute;
                left: 0;
                top: 50%;
                transform: translateY(-50%);
                width: 24px;
                height: 24px;
                background: ${(slideNumber === 4 || slideNumber === 5) ? 'rgba(0, 0, 0, 0.1)' : 'rgba(255, 255, 255, 0.9)'};
                border-radius: 50%;
                display: block;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
              "></span>
              ${point}
            </li>
          `).join('')}
        </ul>
        
        <div style="
          position: absolute;
          bottom: 40px;
          right: 60px;
          font-size: 150px;
          opacity: 0.15;
          pointer-events: none;
        ">${slideIcon}</div>
      </div>
    </div>
    
    <div style="
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 30px;
      margin-bottom: 40px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    ">
      <h3 style="
        color: #475569;
        margin-bottom: 15px;
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
      ">💬 Speaker Notes - Slide ${slideNumber}</h3>
      <p style="
        color: #64748b;
        margin: 0;
        line-height: 1.6;
        font-size: 1.1rem;
      ">${slide.speakerNotes}</p>
    </div>
  `;
  }).join('');

  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Voice-to-Slide Presentation</title>
      <style>
        body { 
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          margin: 30px;
          line-height: 1.6;
          background: #f8fafc;
        }
        .slide { page-break-after: always; }
        @media print {
          body { background: white; }
          .slide { page-break-after: always; }
        }
      </style>
    </head>
    <body>
      <div style="
        text-align: center;
        margin-bottom: 50px;
        padding: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
      ">
        <h1 style="
          margin: 0 0 10px 0;
          font-size: 2.5rem;
          font-weight: 700;
          text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        ">🎤➡️📊 Voice-to-Slide Presentation</h1>
        <p style="
          margin: 0;
          opacity: 0.9;
          font-size: 1.2rem;
        ">Generated with AI-powered voice recognition and content creation</p>
      </div>
      ${slideHTML}
      
      <div style="
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        color: #64748b;
        font-size: 0.9rem;
      ">
        Created with Voice-to-Slide Generator • ${new Date().toLocaleDateString()}
      </div>
    </body>
    </html>
  `;
}

// Error handling middleware
app.use((error, req, res, next) => {
  console.error(error.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Voice-to-Slide Generator running on http://localhost:${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/api/health`);
});

