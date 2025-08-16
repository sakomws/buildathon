#!/usr/bin/env python3
"""
Project 1: Visual Memory Search
A tool to search screenshot history using natural language queries for both text and visual content.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging
import numpy as np
import cv2
from PIL import Image
import pytesseract
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import base64
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import openai
from dotenv import load_dotenv

# Import required packages
try:
    import cv2
    import numpy as np
    from PIL import Image
    import pytesseract
    from transformers import pipeline
    import torch
    from sentence_transformers import SentenceTransformer
    import faiss
    from sklearn.metrics.pairwise import cosine_similarity
    import openai
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Please install required packages: pip install opencv-python pillow pytesseract transformers torch sentence-transformers faiss-cpu scikit-learn openai")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VisualMemorySearch:
    """Main class for visual memory search functionality."""
    
    def __init__(self, screenshot_dir: str):
        # Load environment variables first
        load_dotenv()
        
        self.screenshot_dir = Path(screenshot_dir)
        self.index_file = self.screenshot_dir / "search_index.json"
        self.embeddings_file = self.screenshot_dir / "embeddings.npy"
        self.index = None
        self.screenshots_data = []
        self.text_model = None
        self.vision_model = None
        self.embedding_model = None
        
        # OpenAI configuration
        self.openai_client = None
        self.use_openai = self._setup_openai()
        
        # Initialize models
        self._initialize_models()
        
        # Load or create index
        self._load_or_create_index()
    
    def _setup_openai(self):
        """Setup OpenAI client if API key is available."""
        try:
            # Load environment variables
            load_dotenv()
            
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                # Create client with minimal parameters to avoid configuration issues
                try:
                    # Create httpx client without proxies to avoid configuration issues
                    import httpx
                    http_client = httpx.Client()
                    self.openai_client = openai.OpenAI(api_key=api_key, http_client=http_client)
                    
                    # Test the connection
                    try:
                        # Simple test call to verify API key works
                        test_response = self.openai_client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": "Hello"}],
                            max_tokens=100
                        )
                        logger.info("OpenAI API configured successfully")
                        return True
                    except Exception as e:
                        logger.warning(f"OpenAI API test failed: {e}")
                        self.openai_client = None
                        return False
                except Exception as e:
                    logger.error(f"Failed to create OpenAI client: {e}")
                    return False
            else:
                logger.info("OpenAI API key not found, using local models")
                return False
        except Exception as e:
            logger.error(f"OpenAI setup failed: {e}")
            return False
    
    def _initialize_models(self):
        """Initialize the AI models for text and vision processing."""
        try:
            logger.info("Initializing AI models...")
            
            # Text embedding model for semantic search
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Vision model for image description
            self.vision_model = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
            
            # Text model for query understanding
            self.text_model = pipeline("text-classification", model="facebook/bart-large-mnli")
            
            logger.info("Models initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize models: {e}")
            raise
    
    def _load_or_create_index(self):
        """Load existing index or create new one."""
        if self.index_file.exists() and self.embeddings_file.exists():
            logger.info("Loading existing search index...")
            self._load_index()
        else:
            logger.info("Creating new search index...")
            self._create_index()
    
    def _load_index(self):
        """Load existing index from files."""
        try:
            with open(self.index_file, 'r') as f:
                self.screenshots_data = json.load(f)
            
            self.index = np.load(self.embeddings_file)
            
            # Clean up any existing data that might contain numpy types
            self._cleanup_screenshot_data()
            
            logger.info(f"Loaded index with {len(self.screenshots_data)} screenshots")
            
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            self._create_index()
    
    def _create_index(self):
        """Create new index by processing all screenshots."""
        self.screenshots_data = []
        self.index = None
        
        # Process all screenshots in directory
        screenshot_files = list(self.screenshot_dir.glob("*.png")) + list(self.screenshot_dir.glob("*.jpg")) + list(self.screenshot_dir.glob("*.jpeg"))
        
        if not screenshot_files:
            logger.warning(f"No screenshot files found in {self.screenshot_dir}")
            return
        
        logger.info(f"Processing {len(screenshot_files)} screenshots...")
        
        for screenshot_file in screenshot_files:
            try:
                screenshot_data = self._process_screenshot(screenshot_file)
                if screenshot_data:
                    self.screenshots_data.append(screenshot_data)
            except Exception as e:
                logger.error(f"Failed to process {screenshot_file}: {e}")
        
        if self.screenshots_data:
            # Clean up data before building index
            self._cleanup_screenshot_data()
            self._build_search_index()
            self._save_index()
            logger.info(f"Index created with {len(self.screenshots_data)} screenshots")
    
    def _process_screenshot(self, file_path: Path) -> Optional[Dict]:
        """Process a single screenshot to extract text and visual information with enhanced blue button detection."""
        try:
            # Load image
            image = Image.open(file_path)
            
            # Extract OCR text
            ocr_text = self._extract_ocr_text(image)
            
            # Generate visual description
            visual_description = self._generate_visual_description(file_path, image)
            
            # Enhanced blue button detection
            blue_button_info = self._detect_blue_buttons_enhanced(file_path)
            
            # Create screenshot data - ensure all values are JSON serializable
            screenshot_data = {
                "file_path": str(file_path),
                "filename": str(file_path.name),  # Ensure filename is string
                "ocr_text": str(ocr_text) if ocr_text else "",
                "visual_description": str(visual_description) if visual_description else "",
                "file_size": int(file_path.stat().st_size),
                "dimensions": tuple(int(d) for d in image.size),  # Convert to tuple of ints
                "blue_button_detected": bool(blue_button_info['detected']),
                "blue_button_count": int(blue_button_info['count']),
                "blue_button_details": str(blue_button_info['details']) if blue_button_info['details'] else ""
            }
            
            logger.info(f"Processed {file_path.name}: blue_button={blue_button_info['detected']}, count={blue_button_info['count']}")
            
            return screenshot_data
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return None
    
    def _extract_ocr_text(self, image: Image.Image) -> str:
        """Extract text from image using OCR."""
        try:
            # Convert PIL image to OpenCV format for better OCR
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Preprocess image for better OCR
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Extract text
            text = pytesseract.image_to_string(thresh)
            return text.strip()
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return ""
    
    def _generate_visual_description(self, image_path: str, image: Image.Image) -> str:
        """Generate visual description of image using AI model."""
        try:
            # Resize image if too large for model
            max_size = 2048  # OpenAI supports larger images
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Try OpenAI first if available
            if self.use_openai and self.openai_client:
                try:
                    description = self._generate_openai_description(image_path, image)
                    if description:
                        return description
                except Exception as e:
                    logger.warning(f"OpenAI description failed, falling back to local model: {e}")
            
            # Fallback to local model
            result = self.vision_model(image)
            description = result[0]['generated_text']
            
            # Enhance description with UI element detection
            enhanced_description = self._enhance_ui_description(image_path, description)
            
            return enhanced_description.strip()
            
        except Exception as e:
            logger.error(f"Visual description generation failed: {e}")
            return "Unable to generate visual description"
    
    def _generate_openai_description(self, image_path: str, image: Image.Image) -> str:
        """Generate detailed visual description using OpenAI GPT-4 Vision with maximum accuracy and limits."""
        try:
            # Read and encode image
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Enhanced prompt for maximum accuracy and detail
            prompt = """
            Analyze this screenshot with maximum detail and accuracy. Provide a comprehensive, structured analysis covering:

            **UI Elements & Interactive Components:**
            - Exact button locations, sizes, colors, and text labels
            - Form fields, input types, and validation states
            - Navigation elements, menus, and breadcrumbs
            - Icons, logos, and visual assets with precise descriptions
            - Modal dialogs, tooltips, and overlay elements

            **Visual Design & Layout:**
            - Precise color scheme with hex codes if visible
            - Typography hierarchy, font sizes, and text styles
            - Spacing measurements, alignment, and grid structure
            - Visual balance, contrast, and accessibility features
            - Responsive design elements and breakpoint indicators

            **Content & Functionality:**
            - Primary application purpose and user workflow
            - Data types, charts, tables, and visualization details
            - User interaction patterns and expected behaviors
            - Information architecture and content organization
            - Error states, loading indicators, and feedback elements

            **Technical Implementation:**
            - Platform type (web app, mobile app, desktop software)
            - Framework indicators and technology stack hints
            - Performance and optimization features
            - Security and authentication elements
            - Integration points and external service indicators

            **Semantic Context:**
            - Business domain and industry context
            - Target user audience and use case scenarios
            - Feature capabilities and limitations
            - Competitive differentiators and unique aspects

            **Accessibility & UX:**
            - Screen reader compatibility indicators
            - Keyboard navigation support
            - Color contrast and visual accessibility
            - Internationalization and localization features

            **Advanced Analysis:**
            - User experience flow and interaction patterns
            - Information density and cognitive load assessment
            - Visual hierarchy and attention flow
            - Brand consistency and design system usage
            - Performance indicators and loading states

            Provide the analysis in a structured, detailed format that captures every visual and functional aspect comprehensively. Be specific about locations, sizes, colors, and interactions to enable precise search matching. Include quantitative assessments where possible.
            """

            response = self._call_openai_with_retry(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                model="gpt-4o",  # Best available model
                max_tokens=4000,  # Maximum tokens for comprehensive analysis
                temperature=0.01,  # Minimal randomness for maximum consistency
                top_p=0.99,       # Maximum focus and precision
                frequency_penalty=0.2,  # Enhanced to reduce repetition
                presence_penalty=0.2,   # Enhanced to encourage comprehensive coverage
                response_format={"type": "text"}  # Ensure text output
            )
            
            if response is None:
                raise Exception("OpenAI API call failed after all retry attempts")
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI description generation failed: {e}")
            return None
    
    def _enhance_ui_description(self, image_path: str, base_description: str) -> str:
        """Enhance visual description with OpenCV-based UI element detection and semantic analysis."""
        try:
            # Read image for OpenCV processing
            image = cv2.imread(image_path)
            if image is None:
                return base_description
            
            enhanced_parts = [base_description]
            
            # Extract semantic tags and categories
            semantic_tags = self._extract_semantic_tags(base_description)
            if semantic_tags:
                enhanced_parts.append(f"Semantic tags: {', '.join(semantic_tags)}")
            
            # Detect UI patterns
            ui_patterns = self._detect_ui_patterns(image)
            if ui_patterns:
                enhanced_parts.append(f"UI patterns: {', '.join(ui_patterns)}")
            
            # Detect buttons and interactive elements
            buttons = self._detect_buttons(image)
            if buttons:
                enhanced_parts.append(f"Interactive elements: {len(buttons)} buttons detected")
            
            # Detect dominant colors
            colors = self._detect_dominant_colors(image)
            if colors:
                enhanced_parts.append(f"Dominant colors: {', '.join(colors)}")
            
            # Detect layout structure
            layout = self._detect_layout_structure(image)
            if layout:
                enhanced_parts.append(f"Layout: {layout}")
            
            # Detect content types
            content_types = self._detect_content_types(image)
            if content_types:
                enhanced_parts.append(f"Content types: {', '.join(content_types)}")
            
            return " | ".join(enhanced_parts)
            
        except Exception as e:
            logger.error(f"UI enhancement failed: {e}")
            return base_description
    
    def _extract_semantic_tags(self, description: str) -> List[str]:
        """Extract semantic tags from OpenAI description."""
        tags = []
        description_lower = description.lower()
        
        # Category tags
        categories = {
            'e-commerce': ['shopping', 'cart', 'product', 'store', 'buy', 'purchase'],
            'social media': ['social', 'post', 'feed', 'profile', 'friend', 'share'],
            'productivity': ['dashboard', 'analytics', 'chart', 'report', 'data', 'metrics'],
            'communication': ['email', 'chat', 'message', 'inbox', 'compose'],
            'gaming': ['game', 'player', 'score', 'level', 'inventory', 'health'],
            'weather': ['weather', 'temperature', 'forecast', 'climate', 'sunny', 'rainy'],
            'authentication': ['login', 'signin', 'password', 'auth', 'security'],
            'error': ['error', '404', 'unauthorized', 'failed', 'warning']
        }
        
        for category, keywords in categories.items():
            if any(keyword in description_lower for keyword in keywords):
                tags.append(category)
        
        # UI element tags
        ui_elements = ['button', 'form', 'input', 'navigation', 'sidebar', 'header', 'modal']
        for element in ui_elements:
            if element in description_lower:
                tags.append(element)
        
        # Color tags
        colors = ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'dark', 'light']
        for color in colors:
            if color in description_lower:
                tags.append(color)
        
        return list(set(tags))  # Remove duplicates
    
    def _detect_ui_patterns(self, image: np.ndarray) -> List[str]:
        """Detect common UI patterns in the image."""
        patterns = []
        
        # Convert to grayscale for pattern detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect grid patterns
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        if lines is not None and len(lines) > 10:
            patterns.append("grid layout")
        
        # Detect card-like structures
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        card_count = 0
        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Minimum area for cards
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h
                if 0.5 < aspect_ratio < 2.0:  # Card-like proportions
                    card_count += 1
        
        if card_count > 2:
            patterns.append("card-based layout")
        
        # Detect sidebar
        height, width = gray.shape
        left_region = gray[:, :width//4]
        right_region = gray[:, 3*width//4:]
        
        if np.mean(left_region) < np.mean(gray) * 0.8:
            patterns.append("left sidebar")
        if np.mean(right_region) < np.mean(gray) * 0.8:
            patterns.append("right sidebar")
        
        return patterns
    
    def _detect_layout_structure(self, image: np.ndarray) -> str:
        """Detect the overall layout structure of the interface."""
        height, width = image.shape[:2]
        
        # Analyze layout proportions
        if width > height * 1.5:
            layout = "landscape"
        elif height > width * 1.5:
            layout = "portrait"
        else:
            layout = "square"
        
        # Detect mobile vs desktop
        if width < 500 or height < 800:
            layout += " mobile"
        else:
            layout += " desktop"
        
        return layout
    
    def _detect_content_types(self, image: np.ndarray) -> List[str]:
        """Detect types of content in the image."""
        content_types = []
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect text regions (high contrast areas)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text_contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_area = sum(cv2.contourArea(c) for c in text_contours if cv2.contourArea(c) > 100)
        total_area = image.shape[0] * image.shape[1]
        
        if text_area / total_area > 0.3:
            content_types.append("text-heavy")
        
        # Detect chart-like patterns (regular geometric shapes)
        edges = cv2.Canny(gray, 50, 150)
        chart_contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        chart_count = 0
        for contour in chart_contours:
            area = cv2.contourArea(contour)
            if 100 < area < 10000:  # Chart-sized contours
                chart_count += 1
        
        if chart_count > 2:
            content_types.append("data visualization")
        
        # Detect form-like structures
        if self._detect_form_structure(image):
            content_types.append("form interface")
        
        return content_types
    
    def _detect_form_structure(self, image: np.ndarray) -> bool:
        """Detect if the image contains form-like structures."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Look for rectangular input fields
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        form_elements = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if 500 < area < 5000:  # Input field sized
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h
                if 2 < aspect_ratio < 8:  # Wide rectangles like input fields
                    form_elements += 1
        
        return form_elements >= 2  # At least 2 form elements
    
    def _detect_buttons(self, img_array: np.ndarray) -> List[str]:
        """Detect button-like elements in the image with enhanced blue button detection."""
        try:
            buttons = []
            
            # Convert to different color spaces for better detection
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Enhanced edge detection for rectangular shapes
            edges = cv2.Canny(gray, 30, 100)  # Lowered thresholds for better detection
            
            # Find contours with different methods
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            button_count = 0
            blue_button_found = False
            
            for contour in contours:
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if it's roughly rectangular (4-6 points)
                if len(approx) >= 4 and len(approx) <= 6:
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Check if it's button-sized (not too small, not too large)
                    if 30 <= w <= 400 and 20 <= h <= 120:
                        # Check if it's not just the image border
                        img_h, img_w = img_array.shape[:2]
                        if x > 5 and y > 5 and x + w < img_w - 5 and y + h < img_h - 5:
                            
                            # Check if this region contains blue (potential blue button)
                            roi = hsv[y:y+h, x:x+w]
                            blue_mask = cv2.inRange(roi, np.array([100, 60, 60]), np.array([130, 255, 255]))
                            blue_pixels = cv2.countNonZero(blue_mask)
                            roi_pixels = roi.shape[0] * roi.shape[1]
                            blue_percentage = (blue_pixels / roi_pixels) * 100
                            
                            if blue_percentage > 20:  # Significant blue in this region
                                buttons.append("blue button")
                                blue_button_found = True
                                logger.info(f"Blue button detected at ({x},{y}) with {blue_percentage:.1f}% blue pixels")
                            else:
                                buttons.append("button")
                            
                            button_count += 1
                            
                            # Limit to avoid too many detections
                            if button_count >= 5:
                                break
            
            # If no blue button found but buttons exist, check overall image for blue
            if not blue_button_found and button_count > 0:
                # Check if the image has significant blue content
                blue_mask = cv2.inRange(hsv, np.array([100, 60, 60]), np.array([130, 255, 255]))
                blue_pixels = cv2.countNonZero(blue_mask)
                total_pixels = hsv.shape[0] * hsv.shape[1]
                blue_percentage = (blue_pixels / total_pixels) * 100
                
                if blue_percentage > 5:  # If image has blue content and buttons
                    buttons = ["blue button"] + [btn for btn in buttons if btn != "blue button"]
                    logger.info(f"Image has {blue_percentage:.1f}% blue content with buttons")
            
            return buttons
            
        except Exception as e:
            logger.error(f"Button detection failed: {e}")
            return []
    
    def _detect_dominant_colors(self, img_array: np.ndarray) -> List[str]:
        """Detect dominant colors in the image with enhanced accuracy for blue button detection."""
        try:
            colors = []
            
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # Enhanced blue detection with multiple ranges for better accuracy
            blue_ranges = [
                ([100, 80, 80], [130, 255, 255]),      # Standard blue
                ([110, 70, 70], [140, 255, 255]),      # Lighter blue
                ([90, 90, 90], [120, 255, 255]),       # Darker blue
                ([100, 60, 60], [130, 255, 200]),      # Desaturated blue
                # Extended ranges for better coverage
                ([95, 50, 50], [135, 255, 255]),       # Wider blue range
                ([105, 40, 40], [125, 255, 180]),      # Lower saturation threshold
            ]
            
            # Check blue with multiple ranges and lower threshold
            blue_pixels_total = 0
            total_pixels = hsv.shape[0] * hsv.shape[1]
            
            for lower, upper in blue_ranges:
                lower = np.array(lower)
                upper = np.array(upper)
                mask = cv2.inRange(hsv, lower, upper)
                blue_pixels = cv2.countNonZero(mask)
                blue_pixels_total += blue_pixels
            
            # Calculate blue percentage and add if significant
            blue_percentage = (blue_pixels_total / total_pixels) * 100
            if blue_percentage > 3:  # Lowered threshold for blue detection
                colors.append("blue color")
                logger.info(f"Blue detected: {blue_percentage:.1f}% of pixels")
            
            # Other color ranges with enhanced detection
            color_ranges = {
                'red': ([0, 80, 80], [10, 255, 255]),          # Enhanced red
                'green': ([40, 80, 80], [80, 255, 255]),        # Enhanced green
                'yellow': ([20, 80, 80], [40, 255, 255]),       # Enhanced yellow
                'purple': ([130, 80, 80], [160, 255, 255]),     # Enhanced purple
                'orange': ([10, 80, 80], [20, 255, 255])        # Enhanced orange
            }
            
            for color_name, (lower, upper) in color_ranges.items():
                lower = np.array(lower)
                upper = np.array(upper)
                mask = cv2.inRange(hsv, lower, upper)
                color_pixels = cv2.countNonZero(mask)
                color_percentage = (color_pixels / total_pixels) * 100
                
                if color_percentage > 5:  # Lowered threshold for better detection
                    colors.append(f"{color_name} color")
            
            # Special case: detect dark/light themes
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            avg_brightness = np.mean(gray)
            
            if avg_brightness < 100:
                colors.append("dark theme")
            elif avg_brightness > 200:
                colors.append("light theme")
            
            return colors
            
        except Exception as e:
            logger.error(f"Color detection failed: {e}")
            return []
    
    def _build_search_index(self):
        """Build search index from processed screenshots."""
        if not self.screenshots_data:
            return
        
        # Create text embeddings for search
        texts = []
        for data in self.screenshots_data:
            # Combine OCR text and visual description for search
            combined_text = f"{data['ocr_text']} {data['visual_description']}"
            texts.append(combined_text)
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts)
        self.index = embeddings
    
    def _save_index(self):
        """Save index to files."""
        try:
            # Debug: Check each field for non-serializable types
            logger.info("Checking screenshot data for JSON serialization...")
            for i, data in enumerate(self.screenshots_data):
                for key, value in data.items():
                    try:
                        # Test JSON serialization of this specific field
                        json.dumps({key: value})
                    except (TypeError, OverflowError) as e:
                        logger.error(f"Field '{key}' in screenshot {i} ({data.get('filename', 'unknown')}) is not JSON serializable: {type(value)} = {value}")
                        logger.error(f"Serialization error: {e}")
                        # Try to convert common numpy types
                        if hasattr(value, 'tolist'):  # numpy array
                            data[key] = value.tolist()
                            logger.info(f"Converted numpy array to list for field '{key}'")
                        elif hasattr(value, 'item'):  # numpy scalar
                            data[key] = value.item()
                            logger.info(f"Converted numpy scalar to Python type for field '{key}'")
                        else:
                            # Convert to string as fallback
                            data[key] = str(value)
                            logger.info(f"Converted field '{key}' to string as fallback")
            
            # Save metadata
            with open(self.index_file, 'w') as f:
                json.dump(self.screenshots_data, f, indent=2)
            
            # Save embeddings only if they exist
            if self.index is not None:
                np.save(self.embeddings_file, self.index)
                logger.info("Index and embeddings saved successfully")
            else:
                logger.warning("No embeddings to save")
                logger.info("Metadata index saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            # Log more details about the error
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Additional debugging: try to identify the problematic data
            try:
                logger.info("Attempting to identify problematic data...")
                for i, data in enumerate(self.screenshots_data):
                    logger.info(f"Screenshot {i}: {data.get('filename', 'unknown')}")
                    for key, value in data.items():
                        logger.info(f"  {key}: {type(value)} = {value}")
            except Exception as debug_e:
                logger.error(f"Debug logging failed: {debug_e}")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for screenshots using natural language query with enhanced semantic search and OpenAI validation."""
        try:
            if not self.screenshots_data:
                logger.warning("No screenshots indexed. Use add_screenshot() first.")
                return []
            
            # Enhanced query processing
            enhanced_query = self._enhance_search_query(query)
            semantic_query = self._extract_semantic_query(query)
            
            logger.info(f"Searching for: '{query}' (Enhanced: '{enhanced_query}')")
            logger.info(f"Semantic context: {semantic_query}")
            logger.info(f"Processing {len(self.screenshots_data)} images for maximum accuracy...")
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([enhanced_query])[0]
            
            # Calculate similarities for ALL images
            similarities = []
            for i, data in enumerate(self.screenshots_data):
                # Generate embedding if not present in the separate index
                if i < len(self.index):
                    similarity = cosine_similarity([query_embedding], [self.index[i]])[0][0]
                else:
                    # Generate embedding if not present
                    combined_text = f"{data['ocr_text']} {data['visual_description']}"
                    embedding = self.embedding_model.encode([combined_text])[0]
                    # Store embedding in the separate index, not in screenshots_data
                    if self.index is None:
                        self.index = np.array([embedding])
                    else:
                        self.index = np.vstack([self.index, embedding])
                    similarity = cosine_similarity([query_embedding], [embedding])[0][0]
                    logger.info(f"Generated embedding for image {i+1}/{len(self.screenshots_data)}: {data['filename']}")
                similarities.append(similarity)
            
            # Enhanced confidence scoring with semantic analysis for ALL images
            boosted_similarities = self._boost_visual_matches(query, similarities)
            semantic_boosted = self._apply_semantic_boost(query, semantic_query, boosted_similarities)
            
            # Get top 5 matches with enhanced accuracy
            top_indices = np.argsort(semantic_boosted)[::-1][:top_k]
            
            logger.info(f"Top {len(top_indices)} results selected from {len(self.screenshots_data)} total images")
            logger.info(f"Query: '{query}' - Enhanced: '{enhanced_query}'")
            
            # Log blue button detection for debugging
            if 'blue' in query.lower() and 'button' in query.lower():
                logger.info("Blue button query detected - applying enhanced detection...")
                for i, data in enumerate(self.screenshots_data):
                    if 'blue' in data['visual_description'].lower() and 'button' in data['visual_description'].lower():
                        logger.info(f"Potential blue button found in: {data['filename']}")
            
            results = []
            for idx in top_indices:
                if semantic_boosted[idx] > 0:  # Only include relevant results
                    result = {
                        "filename": str(self.screenshots_data[idx]["filename"]),
                        "file_path": str(self.screenshots_data[idx]["file_path"]),
                        "confidence_score": float(semantic_boosted[idx]),
                        "ocr_text": str(self.screenshots_data[idx]["ocr_text"])[:200] + "..." if len(str(self.screenshots_data[idx]["ocr_text"])) > 200 else str(self.screenshots_data[idx]["ocr_text"]),
                        "visual_description": str(self.screenshots_data[idx]["visual_description"]),
                        "dimensions": tuple(int(d) for d in self.screenshots_data[idx]["dimensions"]),
                        "semantic_tags": list(self._extract_semantic_tags(self.screenshots_data[idx]["visual_description"])),
                        "ui_patterns": list(self._extract_ui_patterns_from_description(self.screenshots_data[idx]["visual_description"])),
                        "content_types": list(self._extract_content_types_from_description(self.screenshots_data[idx]["visual_description"])),
                        "rank": int(len(results) + 1),  # Add ranking information
                        "openai_score": None,  # Will be populated by validation
                        "openai_explanation": None,
                        "openai_tags": [],
                        "openai_confidence": None,
                        "visual_match_details": None,
                        "content_alignment": None,
                        "quality_indicators": None,
                        "final_score": None  # Will be calculated after OpenAI validation
                    }
                    results.append(result)
                    logger.info(f"Result {len(results)}: {result['filename']} (Score: {result['confidence_score']:.3f})")
            
            # Ensure exactly top 5 results
            if len(results) > top_k:
                results = results[:top_k]
                logger.info(f"Truncated results to exactly {top_k} top results")
            elif len(results) < top_k:
                logger.warning(f"Only {len(results)} results found, expected {top_k}")
            
            # Use OpenAI to validate and score ALL top 5 results with enhanced accuracy
            if results:
                logger.info(f"Validating {len(results)} results with OpenAI for maximum accuracy...")
                results = self._validate_results_with_openai(query, results)
                
                # Sort by final score and ensure exactly top 5
                results.sort(key=lambda x: x.get('final_score', x['confidence_score']), reverse=True)
                results = results[:top_k]  # Ensure exactly top 5
                
                logger.info(f"Final top {len(results)} results with enhanced accuracy:")
                for i, result in enumerate(results):
                    final_score = result.get('final_score', result['confidence_score'])
                    openai_score = result.get('openai_score', 'N/A')
                    logger.info(f"  {i+1}. {result['filename']} - Final: {final_score:.3f}, OpenAI: {openai_score}")
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def _enhance_search_query(self, query: str) -> str:
        """Enhance search query for better visual search, especially for blue button queries."""
        query_lower = query.lower()
        enhanced = query
        
        # Enhanced blue button detection
        if 'blue' in query_lower and 'button' in query_lower:
            enhanced += " blue button user interface element interactive component"
            enhanced += " visual appearance color blue button design"
            enhanced += " clickable element blue colored button"
            enhanced += " UI component blue button interface"
            enhanced += " interactive blue button element"
        elif 'blue' in query_lower:
            enhanced += " visual appearance color blue theme design"
            enhanced += " blue colored elements interface"
        elif 'button' in query_lower:
            enhanced += " user interface element interactive component button design"
            enhanced += " clickable element button interface"
        
        # Add visual context for color queries
        if any(color in query_lower for color in ['red', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray', 'black', 'white']):
            enhanced += " visual appearance color"
        
        # Add form context for form queries
        if 'form' in query_lower:
            enhanced += " input fields interface form design"
        
        # Add layout context for layout queries
        if any(word in query_lower for word in ['layout', 'interface', 'design']):
            enhanced += " visual design appearance layout structure"
        
        # Add UI context for UI queries
        if any(word in query_lower for word in ['ui', 'ux', 'interface']):
            enhanced += " user interface design user experience"
        
        # Add interactive context for button queries
        if 'button' in query_lower:
            enhanced += " interactive clickable element"
            enhanced += " user interface component"
        
        logger.info(f"Enhanced query: '{query}' -> '{enhanced}'")
        return enhanced
    
    def _boost_visual_matches(self, query: str, similarities: np.ndarray) -> np.ndarray:
        """Boost similarity scores for visual matches with enhanced accuracy for blue buttons."""
        query_lower = query.lower()
        boosted = similarities.copy()
        
        # Normalize base similarities to 0-1 range
        if np.max(boosted) > 0:
            boosted = (boosted - np.min(boosted)) / (np.max(boosted) - np.min(boosted))
        
        # Special boost for blue button queries
        if 'blue' in query_lower and 'button' in query_lower:
            logger.info("Applying enhanced blue button boost...")
            for i, data in enumerate(self.screenshots_data):
                if data.get('blue_button_detected'):
                    blue_count = data.get('blue_button_count', 0)
                    blue_percentage = data.get('blue_percentage', 0)
                    
                    # Significant boost for confirmed blue buttons
                    if blue_count > 0:
                        boost_factor = 3.0 + (blue_count * 0.5)  # Base 3x + 0.5x per button
                        boosted[i] *= boost_factor
                        logger.info(f"Blue button boost applied to {data['filename']}: {boost_factor}x (count: {blue_count})")
                    elif blue_percentage > 5:  # High blue content
                        boosted[i] *= 2.5
                        logger.info(f"High blue content boost applied to {data['filename']}: 2.5x ({blue_percentage:.1f}% blue)")
        
        # Enhanced color matching with more precise detection
        if any(color in query_lower for color in ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray', 'black', 'white']):
            for i, data in enumerate(self.screenshots_data):
                if data['visual_description']:
                    desc_lower = data['visual_description'].lower()
                    # Check for exact color matches with higher boost
                    for color in ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray', 'black', 'white']:
                        if color in query_lower and color in desc_lower:
                            # Special boost for blue button queries
                            if color == 'blue' and 'button' in query_lower and 'button' in desc_lower:
                                boosted[i] *= 3.0  # 200% boost for blue button matches
                                logger.info(f"Blue button boost applied to {data['filename']}")
                            else:
                                boosted[i] *= 2.0  # 100% boost for exact color matches
                            break
                        elif color in query_lower and any(c in desc_lower for c in ['color', 'colored', 'theme', 'background']):
                            boosted[i] *= 1.7  # Boost by 70% for color-related descriptions
        
        # Enhanced button and UI element matching
        ui_elements = ['button', 'form', 'input', 'field', 'menu', 'sidebar', 'header', 'navigation', 'modal', 'dialog', 'tooltip']
        for element in ui_elements:
            if element in query_lower:
                for i, data in enumerate(self.screenshots_data):
                    if data['visual_description'] and element in data['visual_description'].lower():
                        # Special boost for blue button queries
                        if element == 'button' and 'blue' in query_lower and 'blue' in data['visual_description'].lower():
                            boosted[i] *= 2.5  # 150% boost for blue button matches
                            logger.info(f"Blue button UI boost applied to {data['filename']}")
                        else:
                            boosted[i] *= 1.8  # 80% boost for UI element matches
        
        # Enhanced text matching with semantic similarity
        for i, data in enumerate(self.screenshots_data):
            if data['ocr_text']:
                ocr_lower = data['ocr_text'].lower()
                query_words = query_lower.split()
                
                # Exact word matches
                exact_matches = sum(1 for word in query_words if word in ocr_lower)
                if exact_matches > 0:
                    boost_factor = 1.0 + (exact_matches * 0.4)  # 40% boost per matching word
                    boosted[i] *= boost_factor
                
                # Semantic word matches (synonyms, related terms)
                semantic_matches = self._calculate_semantic_similarity(query_lower, ocr_lower)
                if semantic_matches > 0.3:  # Threshold for semantic relevance
                    boosted[i] *= (1.0 + semantic_matches * 0.5)  # Up to 50% boost for semantic matches
        
        # Enhanced layout and design matching
        layout_terms = ['layout', 'design', 'interface', 'ui', 'ux', 'grid', 'card', 'sidebar', 'header', 'footer']
        if any(term in query_lower for term in layout_terms):
            for i, data in enumerate(self.screenshots_data):
                if data['visual_description']:
                    desc_lower = data['visual_description'].lower()
                    layout_matches = sum(1 for term in layout_terms if term in desc_lower)
                    if layout_matches > 0:
                        boost_factor = 1.0 + (layout_matches * 0.3)  # 30% boost per layout match
                        boosted[i] *= boost_factor
        
        # Ensure scores are in reasonable range (0.1 to 1.0)
        boosted = np.clip(boosted, 0.1, 1.0)
        
        # Apply enhanced sigmoid transformation for better score distribution
        boosted = 1 / (1 + np.exp(-6 * (boosted - 0.5)))  # Increased steepness from 5 to 6
        
        return boosted
    
    def _calculate_semantic_similarity(self, query: str, text: str) -> float:
        """Calculate semantic similarity between query and text using word embeddings."""
        try:
            # Simple semantic matching using common synonyms and related terms
            semantic_groups = {
                'button': ['btn', 'click', 'submit', 'action', 'interactive'],
                'form': ['input', 'field', 'submit', 'entry', 'data'],
                'error': ['warning', 'alert', 'problem', 'issue', 'failed'],
                'login': ['signin', 'authentication', 'auth', 'credentials', 'password'],
                'dashboard': ['overview', 'summary', 'stats', 'metrics', 'analytics'],
                'search': ['find', 'lookup', 'query', 'filter', 'discover'],
                'upload': ['import', 'add', 'attach', 'file', 'document'],
                'settings': ['config', 'preferences', 'options', 'setup', 'configuration']
            }
            
            query_words = query.lower().split()
            text_words = text.lower().split()
            
            semantic_score = 0.0
            for query_word in query_words:
                for group, synonyms in semantic_groups.items():
                    if query_word in [group] + synonyms:
                        # Check if any synonym appears in the text
                        for synonym in [group] + synonyms:
                            if synonym in text_words:
                                semantic_score += 0.8  # High semantic match
                                break
                        break
            
            # Normalize score
            if query_words:
                semantic_score = semantic_score / len(query_words)
            
            return min(semantic_score, 1.0)
            
        except Exception as e:
            logger.error(f"Semantic similarity calculation failed: {e}")
            return 0.0
    
    def _extract_semantic_query(self, query: str) -> Dict[str, List[str]]:
        """Extract semantic components from the search query."""
        query_lower = query.lower()
        semantic_context = {
            'intent': [],
            'elements': [],
            'categories': [],
            'attributes': []
        }
        
        # Intent detection
        intents = {
            'find': ['find', 'show', 'get', 'search', 'locate'],
            'compare': ['compare', 'vs', 'versus', 'difference'],
            'analyze': ['analyze', 'examine', 'review', 'assess']
        }
        
        for intent, keywords in intents.items():
            if any(keyword in query_lower for keyword in keywords):
                semantic_context['intent'].append(intent)
        
        # UI element detection
        ui_elements = ['button', 'form', 'input', 'field', 'menu', 'sidebar', 'header', 'navigation']
        for element in ui_elements:
            if element in query_lower:
                semantic_context['elements'].append(element)
        
        # Category detection
        categories = {
            'e-commerce': ['shopping', 'cart', 'product', 'store', 'buy'],
            'social': ['social', 'post', 'feed', 'profile', 'friend'],
            'productivity': ['dashboard', 'analytics', 'chart', 'report'],
            'communication': ['email', 'chat', 'message', 'inbox'],
            'gaming': ['game', 'player', 'score', 'level'],
            'weather': ['weather', 'temperature', 'forecast']
        }
        
        for category, keywords in categories.items():
            if any(keyword in query_lower for keyword in keywords):
                semantic_context['categories'].append(category)
        
        # Attribute detection
        attributes = {
            'colors': ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'dark', 'light'],
            'sizes': ['large', 'small', 'big', 'tiny', 'wide', 'narrow'],
            'styles': ['modern', 'classic', 'minimal', 'complex', 'simple']
        }
        
        for attr_type, keywords in attributes.items():
            for keyword in keywords:
                if keyword in query_lower:
                    semantic_context['attributes'].append(f"{attr_type}:{keyword}")
        
        return semantic_context
    
    def _apply_semantic_boost(self, query: str, semantic_context: Dict, base_similarities: np.ndarray) -> np.ndarray:
        """Apply semantic boost based on query context and image metadata."""
        boosted = base_similarities.copy()
        
        for i, data in enumerate(self.screenshots_data):
            boost_factor = 1.0
            
            # Boost for category matches
            if semantic_context['categories']:
                image_tags = self._extract_semantic_tags(data['visual_description'])
                category_matches = sum(1 for cat in semantic_context['categories'] if cat in image_tags)
                if category_matches > 0:
                    boost_factor *= (1.0 + category_matches * 0.3)
            
            # Boost for element matches
            if semantic_context['elements']:
                image_elements = self._extract_ui_elements_from_description(data['visual_description'])
                element_matches = sum(1 for elem in semantic_context['elements'] if elem in image_elements)
                if element_matches > 0:
                    boost_factor *= (1.0 + element_matches * 0.4)
            
            # Boost for attribute matches
            if semantic_context['attributes']:
                for attr in semantic_context['attributes']:
                    attr_type, attr_value = attr.split(':', 1)
                    if attr_type == 'colors' and attr_value in data['visual_description'].lower():
                        boost_factor *= 1.5
                    elif attr_type == 'styles' and attr_value in data['visual_description'].lower():
                        boost_factor *= 1.3
            
            # Boost for intent alignment
            if semantic_context['intent']:
                if 'find' in semantic_context['intent'] and 'button' in query.lower():
                    # If looking for buttons, boost images with button descriptions
                    if 'button' in data['visual_description'].lower():
                        boost_factor *= 1.4
            
            boosted[i] *= boost_factor
        
        # Normalize and ensure reasonable range
        if np.max(boosted) > 0:
            boosted = np.clip(boosted, 0.1, 1.0)
        
        return boosted
    
    def _extract_ui_elements_from_description(self, description: str) -> List[str]:
        """Extract UI elements mentioned in the description."""
        ui_elements = ['button', 'form', 'input', 'field', 'menu', 'sidebar', 'header', 'navigation']
        found_elements = []
        
        for element in ui_elements:
            if element in description.lower():
                found_elements.append(element)
        
        return found_elements
    
    def _extract_ui_patterns_from_description(self, description: str) -> List[str]:
        """Extract UI patterns mentioned in the description."""
        patterns = []
        desc_lower = description.lower()
        
        if 'sidebar' in desc_lower:
            patterns.append('sidebar')
        if 'grid' in desc_lower:
            patterns.append('grid layout')
        if 'card' in desc_lower:
            patterns.append('card-based')
        if 'mobile' in desc_lower:
            patterns.append('mobile interface')
        if 'desktop' in desc_lower:
            patterns.append('desktop interface')
        
        return patterns
    
    def _extract_content_types_from_description(self, description: str) -> List[str]:
        """Extract content types mentioned in the description."""
        content_types = []
        desc_lower = description.lower()
        
        if 'chart' in desc_lower or 'graph' in desc_lower:
            content_types.append('data visualization')
        if 'form' in desc_lower:
            content_types.append('form interface')
        if 'text' in desc_lower and 'heavy' in desc_lower:
            content_types.append('text-heavy')
        if 'dashboard' in desc_lower:
            content_types.append('dashboard')
        
        return content_types
    
    def add_screenshot(self, file_path: str) -> bool:
        """Add a new screenshot to the index."""
        try:
            screenshot_data = self._process_screenshot(Path(file_path))
            if screenshot_data:
                self.screenshots_data.append(screenshot_data)
                # Clean up data before building index
                self._cleanup_screenshot_data()
                self._build_search_index()
                self._save_index()
                logger.info(f"Added screenshot: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to add screenshot {file_path}: {e}")
            return False
    
    def list_screenshots(self) -> List[Dict]:
        """List all indexed screenshots."""
        return [
            {
                "filename": data["filename"],
                "file_path": data["file_path"],
                "dimensions": data["dimensions"],
                "file_size": data["file_size"]
            }
            for data in self.screenshots_data
        ]

    def _call_openai_with_retry(self, messages, max_retries=3, **kwargs):
        """Call OpenAI API with retry mechanism for better reliability."""
        for attempt in range(max_retries):
            try:
                logger.info(f"OpenAI API call attempt {attempt + 1}/{max_retries}")
                response = self.openai_client.chat.completions.create(messages=messages, **kwargs)
                logger.info(f"OpenAI API call successful on attempt {attempt + 1}")
                return response
            except Exception as e:
                logger.warning(f"OpenAI API call attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2  # Exponential backoff: 2s, 4s, 8s
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    import time
                    time.sleep(wait_time)
                else:
                    logger.error(f"All {max_retries} OpenAI API call attempts failed")
                    raise e
        
        return None

    def _validate_results_with_openai(self, query: str, results: List[Dict]) -> List[Dict]:
        """Use OpenAI to validate search results and provide final confidence scores with maximum accuracy and limits."""
        logger.info(f"OpenAI validation check - use_openai: {self.use_openai}, client: {self.openai_client is not None}")
        
        if not self.use_openai or not self.openai_client:
            logger.info("OpenAI not available, skipping result validation")
            # Ensure all results have fallback scores
            for result in results:
                result['final_score'] = result['confidence_score']
                result['openai_score'] = None
                result['openai_explanation'] = 'OpenAI not configured'
                result['openai_tags'] = []
                result['openai_confidence'] = 'none'
                result['visual_match_details'] = 'Not available'
                result['content_alignment'] = 'Not available'
                result['quality_indicators'] = 'Not available'
            return results
        
        try:
            logger.info("Validating results with OpenAI for maximum accuracy and comprehensive analysis...")
            
            # Enhanced validation prompt for maximum accuracy and detail
            validation_prompt = f"""
            You are an expert UI/UX analyst and search relevance evaluator with deep expertise in visual interface analysis. Your task is to analyze search results for a visual memory search system with maximum accuracy and comprehensive detail.

            SEARCH QUERY: "{query}"

            EVALUATION CRITERIA (Comprehensive Analysis):
            1. **Visual Match Accuracy**: How precisely does the image visually match the query requirements?
            2. **Content Relevance**: Does the content/functionality align with the query intent and context?
            3. **Element Presence**: Are the specific UI elements, colors, and features mentioned in the query present?
            4. **Context Alignment**: Does the overall context and purpose match the user's search intent?
            5. **Quality Assessment**: Overall quality, clarity, and relevance of the match
            6. **Semantic Coherence**: How well do the visual and textual elements align semantically?
            7. **User Experience Match**: Does the interface provide the expected user experience?
            8. **Technical Accuracy**: Are the technical details and implementation aspects relevant?

            DETAILED SCORING SYSTEM:
            - 0.95-1.0: Perfect match, exactly what was requested with exceptional quality
            - 0.90-0.94: Excellent match, very close to request with high quality
            - 0.85-0.89: Very good match, relevant and high quality
            - 0.80-0.84: Good match, relevant with good quality
            - 0.75-0.79: Fair match, somewhat relevant
            - 0.70-0.74: Weak match, barely relevant
            - 0.65-0.69: Poor match, low relevance
            - 0.0-0.64: Very poor match, not relevant

            You MUST evaluate ALL {len(results)} results comprehensively. Respond with this EXACT JSON format:
            {{
                "results": [
                    {{
                        "index": 0,
                        "relevance_score": 0.92,
                        "explanation": "Comprehensive explanation of scoring with specific details...",
                        "semantic_tags": ["button", "blue", "interface", "form", "modern"],
                        "confidence_level": "very_high",
                        "visual_match_details": "Specific visual elements that match the query...",
                        "content_alignment": "How the content aligns with user intent...",
                        "quality_indicators": "Specific quality aspects observed..."
                    }}
                ]
            }}

            RESULTS TO EVALUATE:
            """
            
            for i, result in enumerate(results):
                validation_prompt += f"""
                RESULT {i+1} (Index: {i}):
                - Filename: {result['filename']}
                - Visual Description: {result['visual_description'][:200]}...
                - OCR Text: {result['ocr_text'][:150]}...
                - Base Score: {result['confidence_score']:.3f}
                - Dimensions: {result['dimensions'][0]}x{result['dimensions'][1]}
                - Semantic Tags: {', '.join(result.get('semantic_tags', []))}
                - UI Patterns: {', '.join(result.get('ui_patterns', []))}
                
                Analyze this result against the query "{query}" and provide:
                1. A precise relevance score (0.0-1.0) with detailed justification
                2. Comprehensive explanation of your scoring methodology
                3. Relevant semantic tags and categories
                4. Confidence level in your assessment (very_high/high/medium/low)
                5. Specific visual match details
                6. Content alignment analysis
                7. Quality indicators and observations
                """
            
            validation_prompt += f"""
            
            CRITICAL REQUIREMENTS FOR MAXIMUM ACCURACY:
            1. You MUST validate ALL {len(results)} results (indices 0 to {len(results)-1})
            2. Provide comprehensive, detailed explanations for each score
            3. Be extremely consistent and precise in your scoring methodology
            4. Consider both visual and semantic aspects comprehensively
            5. Respond ONLY with valid JSON in the exact format shown above
            6. Ensure all scores are between 0.0 and 1.0 with high precision
            7. Use the full scoring range for maximum differentiation
            8. Provide specific, actionable insights for each result
            9. Consider edge cases and nuanced differences between results
            10. Maintain professional analytical standards throughout
            11. You MUST include ALL {len(results)} results in your response
            12. Double-check that your JSON is valid and complete
            """
            
            logger.info("Sending maximum accuracy validation request to OpenAI...")
            
            # Get OpenAI validation with maximum limits and best models for optimal accuracy
            response = self._call_openai_with_retry(
                messages=[
                    {"role": "system", "content": "You are a world-class UI/UX expert and search relevance analyst. You must respond with valid JSON only and evaluate every result with maximum precision and comprehensive detail. You MUST include ALL results in your response."},
                    {"role": "user", "content": validation_prompt}
                ],
                model="gpt-4o",  # Best available model for maximum accuracy
                max_tokens=6000,  # Maximum tokens for comprehensive validation of all results
                temperature=0.01,  # Minimal randomness for maximum consistency and accuracy
                top_p=0.99,       # Maximum focus and precision
                frequency_penalty=0.3,  # Enhanced to reduce repetition and improve variety
                presence_penalty=0.3,   # Enhanced to encourage comprehensive coverage
                response_format={"type": "text"},  # Ensure consistent text output
                presence_penalty_scale=0.1  # Fine-tune presence penalty for better results
            )
            
            if response is None:
                raise Exception("OpenAI API call failed after all retry attempts")
            
            logger.info("OpenAI response received, parsing maximum accuracy validation...")
            logger.info(f"Response content: {response.choices[0].message.content[:400]}...")
            
            # Parse OpenAI response with enhanced error handling
            try:
                validation_data = json.loads(response.choices[0].message.content.strip())
                logger.info(f"Parsed validation data: {len(validation_data.get('results', []))} results")
                
                # Validate that we have the expected number of results
                expected_results = len(results)
                actual_results = len(validation_data.get('results', []))
                
                if actual_results < expected_results:
                    logger.warning(f"OpenAI returned {actual_results} results, expected {expected_results}. Attempting to generate missing scores...")
                    
                    # Generate fallback scores for missing results
                    for i in range(expected_results):
                        found = False
                        for validation in validation_data.get('results', []):
                            if validation.get('index') == i:
                                found = True
                                break
                        
                        if not found:
                            # Create fallback validation for missing result
                            fallback_score = max(0.1, results[i]['confidence_score'] * 0.8)  # Reasonable fallback
                            fallback_validation = {
                                "index": i,
                                "relevance_score": fallback_score,
                                "explanation": f"Fallback score generated for {results[i]['filename']} based on base confidence",
                                "semantic_tags": results[i].get('semantic_tags', []),
                                "confidence_level": "medium",
                                "visual_match_details": "Fallback analysis based on base algorithm",
                                "content_alignment": "Fallback assessment",
                                "quality_indicators": "Fallback quality analysis"
                            }
                            validation_data['results'].append(fallback_validation)
                            logger.info(f"Generated fallback validation for result {i}: {results[i]['filename']}")
                
                # Update results with comprehensive OpenAI validation
                validated_count = 0
                for validation in validation_data.get('results', []):
                    idx = validation.get('index', 0)
                    if idx < len(results):
                        results[idx]['openai_score'] = validation.get('relevance_score', 0.0)
                        results[idx]['openai_explanation'] = validation.get('explanation', '')
                        results[idx]['openai_tags'] = validation.get('semantic_tags', [])
                        results[idx]['openai_confidence'] = validation.get('confidence_level', 'medium')
                        results[idx]['visual_match_details'] = validation.get('visual_match_details', '')
                        results[idx]['content_alignment'] = validation.get('content_alignment', '')
                        results[idx]['quality_indicators'] = validation.get('quality_indicators', '')
                        
                        # Calculate final score as weighted average with enhanced weighting for maximum accuracy
                        original_score = results[idx]['confidence_score']
                        openai_score = results[idx]['openai_score']
                        
                        # Enhanced weighting: 25% original algorithm, 75% OpenAI validation for maximum accuracy
                        final_score = (original_score * 0.25) + (openai_score * 0.75)
                        results[idx]['final_score'] = final_score
                        validated_count += 1
                        logger.info(f"Validated result {idx}: {results[idx]['filename']} - OpenAI: {openai_score:.3f}, Final: {final_score:.3f}")
                    else:
                        logger.warning(f"OpenAI returned index {idx} but we only have {len(results)} results")
                
                logger.info(f"OpenAI validation completed: {validated_count}/{len(results)} results validated with maximum accuracy")
                
                # Ensure ALL results have final scores and comprehensive metadata
                for i, result in enumerate(results):
                    if 'final_score' not in result or result['final_score'] is None:
                        # Generate fallback scores for any missing results
                        if 'openai_score' not in result or result['openai_score'] is None:
                            # Create reasonable fallback OpenAI score
                            fallback_openai_score = max(0.1, result['confidence_score'] * 0.8)
                            result['openai_score'] = fallback_openai_score
                            result['openai_explanation'] = f'Fallback score generated for {result["filename"]} based on base confidence'
                            result['openai_tags'] = result.get('semantic_tags', [])
                            result['openai_confidence'] = 'fallback'
                            result['visual_match_details'] = 'Fallback analysis based on base algorithm'
                            result['content_alignment'] = 'Fallback assessment'
                            result['quality_indicators'] = 'Fallback quality analysis'
                        
                        # Calculate final score
                        original_score = result['confidence_score']
                        openai_score = result['openai_score']
                        final_score = (original_score * 0.25) + (openai_score * 0.75)
                        result['final_score'] = final_score
                        
                        logger.info(f"Generated fallback scores for result {i}: {result['filename']} - OpenAI: {openai_score:.3f}, Final: {final_score:.3f}")
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse OpenAI response: {e}")
                logger.warning(f"Raw response: {response.choices[0].message.content}")
                
                # Generate fallback scores for all results when parsing fails
                logger.info("Generating fallback scores for all results due to parsing error...")
                for i, result in enumerate(results):
                    fallback_openai_score = max(0.1, result['confidence_score'] * 0.8)
                    result['openai_score'] = fallback_openai_score
                    result['openai_explanation'] = f'Fallback score generated for {result["filename"]} due to OpenAI parsing error'
                    result['openai_tags'] = result.get('semantic_tags', [])
                    result['openai_confidence'] = 'fallback_parse_error'
                    result['visual_match_details'] = 'Fallback analysis due to parsing error'
                    result['content_alignment'] = 'Fallback assessment'
                    result['quality_indicators'] = 'Fallback quality analysis'
                    
                    # Calculate final score
                    original_score = result['confidence_score']
                    openai_score = result['openai_score']
                    final_score = (original_score * 0.25) + (openai_score * 0.75)
                    result['final_score'] = final_score
                    
                    logger.info(f"Generated fallback scores for result {i}: {result['filename']} - OpenAI: {openai_score:.3f}, Final: {final_score:.3f}")
            
            return results
            
        except Exception as e:
            logger.error(f"OpenAI validation failed: {e}")
            logger.info("Generating fallback scores for all results due to API error...")
            
            # Generate fallback scores for all results when API fails
            for i, result in enumerate(results):
                fallback_openai_score = max(0.1, result['confidence_score'] * 0.8)
                result['openai_score'] = fallback_openai_score
                result['openai_explanation'] = f'Fallback score generated for {result["filename"]} due to OpenAI API error'
                result['openai_tags'] = result.get('semantic_tags', [])
                result['openai_confidence'] = 'fallback_api_error'
                result['visual_match_details'] = 'Fallback analysis due to API error'
                result['content_alignment'] = 'Fallback assessment'
                result['quality_indicators'] = 'Fallback quality analysis'
                
                # Calculate final score
                original_score = result['confidence_score']
                openai_score = result['openai_score']
                final_score = (original_score * 0.25) + (openai_score * 0.75)
                result['final_score'] = final_score
                
                logger.info(f"Generated fallback scores for result {i}: {result['filename']} - OpenAI: {fallback_openai_score:.3f}, Final: {final_score:.3f}")
            
            return results

    def _detect_blue_buttons_enhanced(self, file_path: Path) -> Dict:
        """Enhanced blue button detection using multiple techniques."""
        try:
            # Read image
            image = cv2.imread(str(file_path))
            if image is None:
                return {'detected': False, 'count': 0, 'details': 'Failed to read image'}
            
            # Convert to different color spaces
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Multiple blue detection ranges for better accuracy
            blue_ranges = [
                # Standard blue ranges
                ([100, 80, 80], [130, 255, 255]),      # Standard blue
                ([110, 70, 70], [140, 255, 255]),      # Lighter blue
                ([90, 90, 90], [120, 255, 255]),       # Darker blue
                ([100, 60, 60], [130, 255, 200]),      # Desaturated blue
                # Extended ranges for better coverage
                ([95, 50, 50], [135, 255, 255]),       # Wider blue range
                ([105, 40, 40], [125, 255, 180]),      # Lower saturation threshold
            ]
            
            blue_pixels_total = 0
            total_pixels = hsv.shape[0] * hsv.shape[1]
            
            # Check all blue ranges
            for lower, upper in blue_ranges:
                lower = np.array(lower)
                upper = np.array(upper)
                mask = cv2.inRange(hsv, lower, upper)
                blue_pixels = cv2.countNonZero(mask)
                blue_pixels_total += blue_pixels
            
            blue_percentage = (blue_pixels_total / total_pixels) * 100
            
            # Enhanced button detection
            buttons = self._detect_buttons_enhanced(image)
            blue_buttons = []
            
            # Check each detected button for blue content
            for button in buttons:
                x, y, w, h = button['bbox']
                roi = hsv[y:y+h, x:x+w]
                
                # Check if ROI contains significant blue
                blue_mask = cv2.inRange(roi, np.array([100, 60, 60]), np.array([130, 255, 255]))
                roi_blue_pixels = cv2.countNonZero(blue_mask)
                roi_pixels = roi.shape[0] * roi.shape[1]
                roi_blue_percentage = (roi_blue_pixels / roi_pixels) * 100
                
                if roi_blue_percentage > 15:  # 15% blue threshold for button
                    blue_buttons.append({
                        'bbox': button['bbox'],
                        'blue_percentage': roi_blue_percentage,
                        'confidence': button['confidence']
                    })
            
            # Determine if blue buttons are detected
            detected = len(blue_buttons) > 0 or blue_percentage > 3
            
            details = f"Blue pixels: {blue_percentage:.1f}%, Buttons: {len(buttons)}, Blue buttons: {len(blue_buttons)}"
            
            if blue_buttons:
                # Convert numpy arrays to lists for JSON serialization
                locations = [f'({int(b["bbox"][0])},{int(b["bbox"][1])})' for b in blue_buttons]
                details += f" - Locations: {locations}"
            
            logger.info(f"Blue button detection for {file_path.name}: {details}")
            
            # Ensure all values are JSON serializable
            serializable_blue_buttons = []
            for button in blue_buttons:
                serializable_blue_buttons.append({
                    'bbox': [int(x) for x in button['bbox']],  # Convert numpy int64 to Python int
                    'blue_percentage': float(button['blue_percentage']),  # Convert numpy float64 to Python float
                    'confidence': float(button['confidence'])  # Convert numpy float64 to Python float
                })
            
            return {
                'detected': bool(detected),
                'count': int(len(blue_buttons)),
                'details': str(details),
                'blue_percentage': float(blue_percentage),
                'total_buttons': int(len(buttons)),
                'blue_buttons': serializable_blue_buttons
            }
            
        except Exception as e:
            logger.error(f"Enhanced blue button detection failed for {file_path}: {e}")
            return {'detected': False, 'count': 0, 'details': f'Detection failed: {e}'}
    
    def _detect_buttons_enhanced(self, image: np.ndarray) -> List[Dict]:
        """Enhanced button detection with better accuracy."""
        try:
            buttons = []
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Multiple edge detection methods
            edges1 = cv2.Canny(gray, 30, 100)
            edges2 = cv2.Canny(gray, 50, 150)
            edges3 = cv2.Canny(gray, 20, 80)
            
            # Combine edge detections
            edges = cv2.bitwise_or(edges1, cv2.bitwise_or(edges2, edges3))
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if it's roughly rectangular (4-6 points)
                if len(approx) >= 4 and len(approx) <= 6:
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Check if it's button-sized
                    if 30 <= w <= 400 and 20 <= h <= 120:
                        # Check if it's not just the image border
                        img_h, img_w = image.shape[:2]
                        if x > 5 and y > 5 and x + w < img_w - 5 and y + h < img_h - 5:
                            
                            # Calculate confidence based on shape regularity
                            area = cv2.contourArea(contour)
                            perimeter = cv2.arcLength(contour, True)
                            if perimeter > 0:
                                circularity = 4 * np.pi * area / (perimeter * perimeter)
                                confidence = 1.0 - abs(circularity - 0.785)  # 0.785 is ideal rectangle
                            else:
                                confidence = 0.5
                            
                            # Check aspect ratio
                            aspect_ratio = w / h
                            if 0.5 <= aspect_ratio <= 4.0:  # Reasonable button proportions
                                buttons.append({
                                    'bbox': (int(x), int(y), int(w), int(h)),  # Convert to Python int
                                    'confidence': float(confidence),  # Convert to Python float
                                    'area': float(area),  # Convert to Python float
                                    'aspect_ratio': float(aspect_ratio)  # Convert to Python float
                                })
            
            # Sort by confidence
            buttons.sort(key=lambda x: x['confidence'], reverse=True)
            
            # Limit to top buttons
            return buttons[:10]
            
        except Exception as e:
            logger.error(f"Enhanced button detection failed: {e}")
            return []

    def _cleanup_screenshot_data(self):
        """Clean up screenshot data to ensure all values are JSON serializable."""
        logger.info("Cleaning up screenshot data for JSON serialization...")
        cleaned_count = 0
        
        for i, data in enumerate(self.screenshots_data):
            for key, value in list(data.items()):
                try:
                    # Test JSON serialization
                    json.dumps({key: value})
                except (TypeError, OverflowError):
                    # Convert non-serializable types
                    if hasattr(value, 'tolist'):  # numpy array
                        data[key] = value.tolist()
                        cleaned_count += 1
                        logger.info(f"Converted numpy array to list for field '{key}' in {data.get('filename', 'unknown')}")
                    elif hasattr(value, 'item'):  # numpy scalar
                        data[key] = value.item()
                        cleaned_count += 1
                        logger.info(f"Converted numpy scalar to Python type for field '{key}' in {data.get('filename', 'unknown')}")
                    elif isinstance(value, np.integer):
                        data[key] = int(value)
                        cleaned_count += 1
                        logger.info(f"Converted numpy integer to Python int for field '{key}' in {data.get('filename', 'unknown')}")
                    elif isinstance(value, np.floating):
                        data[key] = float(value)
                        cleaned_count += 1
                        logger.info(f"Converted numpy float to Python float for field '{key}' in {data.get('filename', 'unknown')}")
                    else:
                        # Convert to string as fallback
                        data[key] = str(value)
                        cleaned_count += 1
                        logger.info(f"Converted field '{key}' to string as fallback in {data.get('filename', 'unknown')}")
        
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} non-serializable values")
        else:
            logger.info("No cleanup needed - all data is already JSON serializable")

def main():
    """Main function to run the visual memory search application."""
    parser = argparse.ArgumentParser(description="Visual Memory Search - Search screenshots using natural language")
    parser.add_argument("screenshot_dir", help="Directory containing screenshots")
    parser.add_argument("--query", "-q", help="Search query")
    parser.add_argument("--add", "-a", help="Add a new screenshot to index")
    parser.add_argument("--list", "-l", action="store_true", help="List all indexed screenshots")
    parser.add_argument("--rebuild", "-r", action="store_true", help="Rebuild the search index")
    
    args = parser.parse_args()
    
    # Check if screenshot directory exists
    if not os.path.exists(args.screenshot_dir):
        print(f"Error: Directory {args.screenshot_dir} does not exist")
        sys.exit(1)
    
    try:
        # Initialize search engine
        search_engine = VisualMemorySearch(args.screenshot_dir)
        
        # Handle different commands
        if args.add:
            if search_engine.add_screenshot(args.add):
                print(f"Successfully added: {args.add}")
            else:
                print(f"Failed to add: {args.add}")
                sys.exit(1)
        
        elif args.list:
            screenshots = search_engine.list_screenshots()
            if screenshots:
                print(f"\nIndexed Screenshots ({len(screenshots)}):")
                print("-" * 80)
                for ss in screenshots:
                    print(f"📱 {ss['filename']}")
                    print(f"   Path: {ss['file_path']}")
                    print(f"   Size: {ss['dimensions'][0]}x{ss['dimensions'][1]} pixels")
                    print(f"   File: {ss['file_size']} bytes")
                    print()
            else:
                print("No screenshots indexed yet.")
        
        elif args.query:
            print(f"Searching for: '{args.query}'")
            print("-" * 50)
            
            results = search_engine.search(args.query, top_k=5)  # Ensure top 5 results
            
            if results:
                print(f"Found {len(results)} top results:")
                print("-" * 40)
                for i, result in enumerate(results, 1):
                    final_score = result.get('final_score', result['confidence_score'])
                    openai_score = result.get('openai_score')
                    rank = result.get('rank', i)
                    
                    if openai_score is not None:
                        print(f"{rank:2d}. {result['filename']:<30} Final: {final_score:.3f} (OpenAI: {openai_score:.3f})")
                    else:
                        print(f"{rank:2d}. {result['filename']:<30} Score: {final_score:.3f}")
                
                # Show detailed results option
                print("\n" + "-" * 40)
                show_details = input("Show detailed results? (y/n): ").strip().lower()
                if show_details in ['y', 'yes']:
                    print("\n📋 Detailed Results:")
                    for i, result in enumerate(results, 1):
                        rank = result.get('rank', i)
                        print(f"\n{rank}. 📱 {result['filename']}")
                        print(f"   Final Score: {result.get('final_score', result['confidence_score']):.3f}")
                        print(f"   Original Score: {result['confidence_score']:.3f}")
                        
                        if result.get('openai_score') is not None:
                            print(f"   OpenAI Score: {result['openai_score']:.3f}")
                            print(f"   OpenAI Explanation: {result.get('openai_explanation', 'N/A')}")
                            print(f"   OpenAI Tags: {', '.join(result.get('openai_tags', []))}")
                            print(f"   OpenAI Confidence: {result.get('openai_confidence', 'N/A')}")
                        
                        print(f"   Path: {result['file_path']}")
                        print(f"   Dimensions: {result['dimensions'][0]}x{result['dimensions'][1]}")
                        if result['ocr_text']:
                            print(f"   OCR Text: {result['ocr_text'][:200] + '...' if len(result['ocr_text']) > 200 else result['ocr_text']}")
                        if result['visual_description']:
                            print(f"   Visual: {result['visual_description']}")
            else:
                print("No results found.")
        
        elif args.rebuild:
            print("Rebuilding search index...")
            # Delete existing index files
            if search_engine.index_file.exists():
                search_engine.index_file.unlink()
            if search_engine.embeddings_file.exists():
                search_engine.embeddings_file.unlink()
            
            # Recreate index
            search_engine._create_index()
            print("Index rebuilt successfully!")
        
        else:
            # Interactive mode
            print("🔍 Visual Memory Search - Interactive Mode")
            print("Type 'help' for commands, 'quit' to exit")
            print("-" * 50)
            
            while True:
                try:
                    user_input = input("\n> ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        break
                    elif user_input.lower() == 'help':
                        print("\nAvailable commands:")
                        print("  <query>           - Search for screenshots")
                        print("  add <file_path>   - Add screenshot to index")
                        print("  list              - List all indexed screenshots")
                        print("  rebuild           - Rebuild search index")
                        print("  quit/exit         - Exit the application")
                    elif user_input.lower().startswith('add '):
                        file_path = user_input[4:].strip()
                        if search_engine.add_screenshot(file_path):
                            print(f"✅ Added: {file_path}")
                        else:
                            print(f"❌ Failed to add: {file_path}")
                    elif user_input.lower() == 'list':
                        screenshots = search_engine.list_screenshots()
                        if screenshots:
                            print(f"\n📱 Indexed Screenshots ({len(screenshots)}):")
                            for ss in screenshots:
                                print(f"  • {ss['filename']} ({ss['dimensions'][0]}x{ss['dimensions'][1]})")
                        else:
                            print("No screenshots indexed yet.")
                    elif user_input.lower() == 'rebuild':
                        print("🔄 Rebuilding index...")
                        if search_engine.index_file.exists():
                            search_engine.index_file.unlink()
                        if search_engine.embeddings_file.exists():
                            search_engine.embeddings_file.unlink()
                        search_engine._create_index()
                        print("✅ Index rebuilt!")
                    elif user_input.strip():
                        # Treat as search query
                        print(f"\n🔍 Searching for: '{user_input}'")
                        results = search_engine.search(user_input, top_k=5)  # Ensure top 5 results
                        
                        if results:
                            print(f"\n📊 Found {len(results)} top results:")
                            print("-" * 50)
                            for i, result in enumerate(results, 1):
                                rank = result.get('rank', i)
                                print(f"{rank:2d}. {result['filename']:<30} Score: {result['confidence_score']:.3f}")
                            
                            # Show detailed results option
                            print("\n" + "-" * 50)
                            show_details = input("Show detailed results? (y/n): ").strip().lower()
                            if show_details in ['y', 'yes']:
                                print("\n📋 Detailed Results:")
                                for i, result in enumerate(results, 1):
                                    rank = result.get('rank', i)
                                    print(f"\n{rank}. 📱 {result['filename']} (Score: {result['confidence_score']:.3f})")
                                    print(f"   📍 {result['file_path']}")
                                    if result['ocr_text']:
                                        print(f"   📝 Text: {result['ocr_text'][:100]}...")
                                    if result['visual_description']:
                                        print(f"   🎨 Visual: {result['visual_description']}")
                        else:
                            print("❌ No results found.")
                    else:
                        continue
                        
                except KeyboardInterrupt:
                    print("\n\nGoodbye!")
                    break
                except EOFError:
                    break
    
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
