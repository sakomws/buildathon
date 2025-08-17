// Global variables
let mediaRecorder;
let audioChunks = [];
let recordingTimer;
let recordingStartTime;
let currentAudioFile = null;

// DOM elements
const fileUploadArea = document.getElementById('fileUploadArea');
const audioFileInput = document.getElementById('audioFile');
const recordBtn = document.getElementById('recordBtn');
const timer = document.getElementById('timer');
const recordingStatus = document.getElementById('recordingStatus');
const processingSection = document.getElementById('processingSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const resultsSection = document.getElementById('resultsSection');
const transcriptDisplay = document.getElementById('transcriptDisplay');
const slidesContainer = document.getElementById('slidesContainer');
const exportHtmlBtn = document.getElementById('exportHtmlBtn');
const exportPdfBtn = document.getElementById('exportPdfBtn');
const testBtn = document.getElementById('testBtn');
const statusMessage = document.getElementById('statusMessage');
const loadingModal = document.getElementById('loadingModal');
const modalTitle = document.getElementById('modalTitle');
const modalMessage = document.getElementById('modalMessage');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeFileUpload();
    initializeRecording();
    initializeTestButton();
    checkHealthStatus();
});

// File Upload Functionality
function initializeFileUpload() {
    // Click to upload
    fileUploadArea.addEventListener('click', () => {
        audioFileInput.click();
    });

    // Drag and drop
    fileUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadArea.classList.add('dragover');
    });

    fileUploadArea.addEventListener('dragleave', () => {
        fileUploadArea.classList.remove('dragover');
    });

    fileUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleAudioFile(files[0]);
        }
    });

    // File input change
    audioFileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleAudioFile(e.target.files[0]);
        }
    });
}

function handleAudioFile(file) {
    // Validate file type - check both MIME type and file extension
    const allowedTypes = ['audio/mp3', 'audio/wav', 'audio/m4a', 'audio/mpeg', 'audio/mp4', 'audio/x-m4a'];
    const fileName = file.name.toLowerCase();
    const allowedExtensions = ['.mp3', '.wav', '.m4a'];
    
    const hasValidMimeType = allowedTypes.includes(file.type);
    const hasValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));
    
    // Accept file if either MIME type OR extension is valid (fallback for MIME type issues)
    if (!hasValidMimeType && !hasValidExtension) {
        showError('Please select a valid audio file (MP3, WAV, or M4A)');
        console.log('File type rejected:', file.type, 'File name:', file.name);
        return;
    }

    // Validate file size (50MB limit)
    if (file.size > 50 * 1024 * 1024) {
        showError('File size must be less than 50MB');
        return;
    }

    currentAudioFile = file;
    updateStatus('Audio file selected: ' + file.name);
    processAudioFile(file);
}

// Recording Functionality
function initializeRecording() {
    recordBtn.addEventListener('click', toggleRecording);
}

async function toggleRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        stopRecording();
    } else {
        await startRecording();
    }
}

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioFile = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
            currentAudioFile = audioFile;
            processAudioFile(audioFile);
        };

        mediaRecorder.start();
        recordBtn.classList.add('recording');
        recordBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Recording';
        recordingStatus.textContent = 'Recording...';
        
        // Start timer
        recordingStartTime = Date.now();
        recordingTimer = setInterval(updateTimer, 1000);
        
        // Auto-stop after 3 minutes
        setTimeout(() => {
            if (mediaRecorder.state === 'recording') {
                stopRecording();
            }
        }, 180000); // 3 minutes

    } catch (error) {
        console.error('Error accessing microphone:', error);
        showError('Unable to access microphone. Please check permissions.');
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        
        recordBtn.classList.remove('recording');
        recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
        recordingStatus.textContent = 'Recording saved';
        
        clearInterval(recordingTimer);
    }
}

function updateTimer() {
    const elapsed = Date.now() - recordingStartTime;
    const minutes = Math.floor(elapsed / 60000);
    const seconds = Math.floor((elapsed % 60000) / 1000);
    timer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

// Audio Processing
async function processAudioFile(file) {
    showLoadingModal('Uploading audio file...', 'Please wait while we upload your audio file');
    
    try {
        // Upload file
        const formData = new FormData();
        formData.append('audio', file);

        const uploadResponse = await fetch('/api/upload-audio', {
            method: 'POST',
            body: formData
        });

        if (!uploadResponse.ok) {
            throw new Error('Failed to upload audio file');
        }

        const uploadResult = await uploadResponse.json();
        
        // Transcribe audio
        updateLoadingModal('Transcribing audio...', 'Converting speech to text using AI');
        
        const transcribeResponse = await fetch('/api/transcribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filePath: uploadResult.filePath
            })
        });

        if (!transcribeResponse.ok) {
            throw new Error('Failed to transcribe audio');
        }

        const transcribeResult = await transcribeResponse.json();
        
        // Generate slides
        updateLoadingModal('Generating slides...', 'Creating professional presentation with AI');
        
        const slidesResponse = await fetch('/api/generate-slides', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                transcript: transcribeResult.transcript
            })
        });

        if (!slidesResponse.ok) {
            throw new Error('Failed to generate slides');
        }

        const slidesResult = await slidesResponse.json();
        
        hideLoadingModal();
        displayResults(slidesResult.slides, transcribeResult.transcript);
        
    } catch (error) {
        console.error('Processing error:', error);
        hideLoadingModal();
        showError('Failed to process audio: ' + error.message);
    }
}

// Display Results
function displayResults(slides, transcript) {
    resultsSection.style.display = 'block';
    processingSection.style.display = 'none';
    
    // Display transcription
    transcriptDisplay.innerHTML = `
        <div class="transcript-content">
            <p><strong>Transcribed Text:</strong></p>
            <p style="font-style: italic; color: #666; background: #f9f9f9; padding: 10px; border-radius: 4px; border-left: 3px solid #4F46E5;">
                "${transcript || 'No transcription available'}"
            </p>
            <small>Word count: ${transcript ? transcript.split(' ').length : 0}</small>
        </div>
    `;
    
    // Check if transcript is too short and show warning
    if (transcript && transcript.split(' ').length < 10) {
        transcriptDisplay.innerHTML += `
            <div class="transcript-warning" style="background: #FEF3C7; border: 1px solid #F59E0B; color: #92400E; padding: 10px; border-radius: 4px; margin-top: 10px;">
                <i class="fas fa-exclamation-triangle"></i> 
                <strong>Note:</strong> Your audio seems quite short. For better results, try speaking for 30-60 seconds with more detailed content about your topic.
            </div>
        `;
    }
    
    slidesContainer.innerHTML = '';
    
    slides.forEach((slide, index) => {
        const slideElement = createSlideElement(slide, index + 1);
        slidesContainer.appendChild(slideElement);
    });
    
    // Store slides for export
    window.generatedSlides = slides;
    window.generatedTranscript = transcript;
    
    updateStatus('Presentation generated successfully!');
    
    // Enable export buttons
    exportHtmlBtn.addEventListener('click', exportAsHTML);
}

function createSlideElement(slide, slideNumber) {
    const slideDiv = document.createElement('div');
    slideDiv.className = 'slide-preview';
    slideDiv.setAttribute('data-slide', slideNumber);
    
    // Define professional visual icons for each slide type
    const slideVisualIcons = {
        1: '🎯', // Introduction
        2: '⚡', // Challenge  
        3: '🚀', // Strategy
        4: '⚙️', // Implementation
        5: '✅'  // Conclusion
    };
    
    const visualIcon = slideVisualIcons[slideNumber] || '📊';
    
    slideDiv.innerHTML = `
        <div class="slide-header">
            <div class="slide-number">${slideNumber}</div>
            <h2 class="slide-title">${slide.title}</h2>
            <ul class="slide-content">
                ${slide.content.map(point => `<li>${point}</li>`).join('')}
            </ul>
            <div class="slide-visual-icon">${visualIcon}</div>
        </div>
        <div class="speaker-notes">
            <h4><i class="fas fa-comments"></i> Speaker Notes</h4>
            <p>${slide.speakerNotes}</p>
        </div>
    `;
    
    return slideDiv;
}

// Export Functionality
async function exportAsHTML() {
    try {
        if (!window.generatedSlides) {
            showError('No slides to export');
            return;
        }

        const response = await fetch('/api/export-html', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                slides: window.generatedSlides
            })
        });

        if (!response.ok) {
            throw new Error('Failed to export slides');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'presentation.html';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        updateStatus('Presentation exported successfully!');
        
    } catch (error) {
        console.error('Export error:', error);
        showError('Failed to export presentation: ' + error.message);
    }
}

// Test Button
function initializeTestButton() {
    testBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            updateStatus(data.status);
        } catch (error) {
            showError('Test failed: ' + error.message);
        }
    });
}

// Health Check
async function checkHealthStatus() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        updateStatus(data.status);
    } catch (error) {
        updateStatus('Application is working (offline mode)');
    }
}

// Utility Functions
function showLoadingModal(title, message) {
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    loadingModal.style.display = 'flex';
}

function updateLoadingModal(title, message) {
    modalTitle.textContent = title;
    modalMessage.textContent = message;
}

function hideLoadingModal() {
    loadingModal.style.display = 'none';
}

function updateStatus(message) {
    statusMessage.textContent = message;
}

function showError(message) {
    statusMessage.textContent = 'Error: ' + message;
    statusMessage.style.color = '#ef4444';
    
    // Reset color after 5 seconds
    setTimeout(() => {
        statusMessage.style.color = '#6b7280';
    }, 5000);
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Spacebar to start/stop recording
    if (e.code === 'Space' && e.target === document.body) {
        e.preventDefault();
        if (recordBtn) {
            recordBtn.click();
        }
    }
    
    // Escape to close modal
    if (e.code === 'Escape') {
        hideLoadingModal();
    }
});

// Help functionality
document.querySelector('.help-icon').addEventListener('click', () => {
    alert(`Voice-to-Slide Generator Help

🎤 Recording:
- Click "Start Recording" to record audio
- Maximum 3 minutes per recording
- Use Spacebar to start/stop recording

📁 Upload:
- Drag & drop audio files or click to browse
- Supported: MP3, WAV, M4A (max 50MB)

📊 Processing:
- AI transcribes your speech to text
- Generates 5 professional slides
- Includes speaker notes for each slide

📤 Export:
- Download as HTML (PDF coming soon)
- Professional presentation format

💡 Tips:
- Speak clearly for better transcription
- Keep presentations under 3 minutes
- Use the preview button to see results`);
});

// Preview functionality
document.querySelector('.preview-btn').addEventListener('click', () => {
    if (window.generatedSlides) {
        // Show a preview modal with the first slide
        const firstSlide = window.generatedSlides[0];
        alert(`Preview: ${firstSlide.title}

${firstSlide.content.join('\n')}

Speaker Notes: ${firstSlide.speakerNotes}`);
    } else {
        alert('No slides to preview. Please generate a presentation first.');
    }
});

