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
                openai.api_key = api_key
                self.openai_client = openai
                # Test the connection
                try:
                    # Simple test call to verify API key works
                    test_response = openai.ChatCompletion.create(
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
            self._build_search_index()
            self._save_index()
            logger.info(f"Index created with {len(self.screenshots_data)} screenshots")
    
    def _process_screenshot(self, file_path: Path) -> Optional[Dict]:
        """Process a single screenshot to extract text and visual information."""
        try:
            # Load image
            image = Image.open(file_path)
            
            # Extract OCR text
            ocr_text = self._extract_ocr_text(image)
            
            # Generate visual description
            visual_description = self._generate_visual_description(file_path, image)
            
            # Create screenshot data
            screenshot_data = {
                "file_path": str(file_path),
                "filename": file_path.name,
                "ocr_text": ocr_text,
                "visual_description": visual_description,
                "file_size": file_path.stat().st_size,
                "dimensions": image.size
            }
            
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
        """Generate detailed visual description using OpenAI GPT-4 Vision with enhanced accuracy."""
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

            Provide the analysis in a structured, detailed format that captures every visual and functional aspect comprehensively. Be specific about locations, sizes, colors, and interactions to enable precise search matching.
            """

            response = openai.ChatCompletion.create(
                model="gpt-4o",
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
                max_tokens=2000,  # Increased from 1000 for more detailed descriptions
                temperature=0.05,  # Reduced for more consistent, accurate descriptions
                top_p=0.95,       # Added for better focus
                frequency_penalty=0.1,  # Added to reduce repetition
                presence_penalty=0.1    # Added to encourage comprehensive coverage
            )
            
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
        """Detect button-like elements in the image."""
        try:
            buttons = []
            
            # Simple edge detection for rectangular shapes
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
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
                    
                    # Check if it's button-sized (not too small, not too large)
                    if 50 <= w <= 300 and 20 <= h <= 100:
                        # Check if it's not just the image border
                        img_h, img_w = img_array.shape[:2]
                        if x > 10 and y > 10 and x + w < img_w - 10 and y + h < img_h - 10:
                            buttons.append("button")
                            break  # Just add one button detection
            
            return buttons
            
        except Exception as e:
            logger.error(f"Button detection failed: {e}")
            return []
    
    def _detect_dominant_colors(self, img_array: np.ndarray) -> List[str]:
        """Detect dominant colors in the image with improved accuracy."""
        try:
            colors = []
            
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # Define more precise color ranges with better thresholds
            color_ranges = {
                'blue': ([100, 100, 100], [130, 255, 255]),      # More saturated blue
                'red': ([0, 100, 100], [10, 255, 255]),          # More saturated red
                'green': ([40, 100, 100], [80, 255, 255]),       # More saturated green
                'yellow': ([20, 100, 100], [40, 255, 255]),      # More saturated yellow
                'purple': ([130, 100, 100], [160, 255, 255]),    # More saturated purple
                'orange': ([10, 100, 100], [20, 255, 255])       # More saturated orange
            }
            
            # Check each color with higher threshold
            for color_name, (lower, upper) in color_ranges.items():
                lower = np.array(lower)
                upper = np.array(upper)
                
                # Create mask for this color
                mask = cv2.inRange(hsv, lower, upper)
                
                # Count pixels of this color
                color_pixels = cv2.countNonZero(mask)
                total_pixels = mask.shape[0] * mask.shape[1]
                color_percentage = (color_pixels / total_pixels) * 100
                
                # Higher threshold (10% instead of 5%) to avoid false positives
                if color_percentage > 10:
                    colors.append(f"{color_name} color")
            
            # Special case: detect dark/light themes
            # Calculate overall brightness
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
            # Save metadata
            with open(self.index_file, 'w') as f:
                json.dump(self.screenshots_data, f, indent=2)
            
            # Save embeddings
            np.save(self.embeddings_file, self.index)
            
            logger.info("Index saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
    
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
                if 'embedding' in data:
                    similarity = cosine_similarity([query_embedding], [data['embedding']])[0][0]
                    similarities.append(similarity)
                else:
                    # Generate embedding if not present
                    combined_text = f"{data['ocr_text']} {data['visual_description']}"
                    embedding = self.embedding_model.encode([combined_text])[0]
                    data['embedding'] = embedding
                    similarities.append(cosine_similarity([query_embedding], [embedding])[0][0])
                    logger.info(f"Generated embedding for image {i+1}/{len(self.screenshots_data)}: {data['filename']}")
            
            # Enhanced confidence scoring with semantic analysis for ALL images
            boosted_similarities = self._boost_visual_matches(query, similarities)
            semantic_boosted = self._apply_semantic_boost(query, semantic_query, boosted_similarities)
            
            # Get top 5 matches with enhanced accuracy
            top_indices = np.argsort(semantic_boosted)[::-1][:top_k]
            
            logger.info(f"Top {len(top_indices)} results selected from {len(self.screenshots_data)} total images")
            
            results = []
            for idx in top_indices:
                if semantic_boosted[idx] > 0:  # Only include relevant results
                    result = {
                        "filename": self.screenshots_data[idx]["filename"],
                        "file_path": self.screenshots_data[idx]["file_path"],
                        "confidence_score": float(semantic_boosted[idx]),
                        "ocr_text": self.screenshots_data[idx]["ocr_text"][:200] + "..." if len(self.screenshots_data[idx]["ocr_text"]) > 200 else self.screenshots_data[idx]["ocr_text"],
                        "visual_description": self.screenshots_data[idx]["visual_description"],
                        "dimensions": self.screenshots_data[idx]["dimensions"],
                        "semantic_tags": self._extract_semantic_tags(self.screenshots_data[idx]["visual_description"]),
                        "ui_patterns": self._extract_ui_patterns_from_description(self.screenshots_data[idx]["visual_description"]),
                        "content_types": self._extract_content_types_from_description(self.screenshots_data[idx]["visual_description"]),
                        "rank": len(results) + 1  # Add ranking information
                    }
                    results.append(result)
                    logger.info(f"Result {len(results)}: {result['filename']} (Score: {result['confidence_score']:.3f})")
            
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
        """Enhance search query for better visual search."""
        query_lower = query.lower()
        enhanced = query
        
        # Add visual context for color queries
        if any(color in query_lower for color in ['blue', 'red', 'green', 'yellow', 'purple', 'orange']):
            enhanced += " visual appearance color"
        
        # Add UI context for button queries
        if 'button' in query_lower:
            enhanced += " user interface element"
        
        # Add form context for form queries
        if 'form' in query_lower:
            enhanced += " input fields interface"
        
        # Add layout context for layout queries
        if any(word in query_lower for word in ['layout', 'interface', 'design']):
            enhanced += " visual design appearance"
        
        return enhanced
    
    def _boost_visual_matches(self, query: str, similarities: np.ndarray) -> np.ndarray:
        """Boost similarity scores for visual matches with enhanced accuracy."""
        query_lower = query.lower()
        boosted = similarities.copy()
        
        # Normalize base similarities to 0-1 range
        if np.max(boosted) > 0:
            boosted = (boosted - np.min(boosted)) / (np.max(boosted) - np.min(boosted))
        
        # Enhanced color matching with more precise detection
        if any(color in query_lower for color in ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray', 'black', 'white']):
            for i, data in enumerate(self.screenshots_data):
                if data['visual_description']:
                    desc_lower = data['visual_description'].lower()
                    # Check for exact color matches with higher boost
                    for color in ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray', 'black', 'white']:
                        if color in query_lower and color in desc_lower:
                            boosted[i] *= 2.0  # Boost by 100% for exact color matches
                            break
                        elif color in query_lower and any(c in desc_lower for c in ['color', 'colored', 'theme', 'background']):
                            boosted[i] *= 1.7  # Boost by 70% for color-related descriptions
        
        # Enhanced button and UI element matching
        ui_elements = ['button', 'form', 'input', 'field', 'menu', 'sidebar', 'header', 'navigation', 'modal', 'dialog', 'tooltip']
        for element in ui_elements:
            if element in query_lower:
                for i, data in enumerate(self.screenshots_data):
                    if data['visual_description'] and element in data['visual_description'].lower():
                        boosted[i] *= 1.8  # Boost by 80% for UI element matches
        
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

    def _validate_results_with_openai(self, query: str, results: List[Dict]) -> List[Dict]:
        """Use OpenAI to validate search results and provide final confidence scores with enhanced accuracy."""
        logger.info(f"OpenAI validation check - use_openai: {self.use_openai}, client: {self.openai_client is not None}")
        
        if not self.use_openai or not self.openai_client:
            logger.info("OpenAI not available, skipping result validation")
            return results
        
        try:
            logger.info("Validating results with OpenAI for enhanced accuracy...")
            
            # Enhanced validation prompt for maximum accuracy
            validation_prompt = f"""
            You are an expert UI/UX analyst and search relevance evaluator. Your task is to analyze search results for a visual memory search system with maximum accuracy.

            SEARCH QUERY: "{query}"

            EVALUATION CRITERIA:
            1. **Visual Match Accuracy**: How well does the image visually match the query?
            2. **Content Relevance**: Does the content/functionality align with the query intent?
            3. **Element Presence**: Are the specific UI elements mentioned in the query present?
            4. **Context Alignment**: Does the overall context match the user's search intent?
            5. **Quality Assessment**: Overall quality and relevance of the match

            SCORING SYSTEM:
            - 0.9-1.0: Perfect match, exactly what was requested
            - 0.8-0.89: Excellent match, very close to request
            - 0.7-0.79: Good match, relevant but not perfect
            - 0.6-0.69: Fair match, somewhat relevant
            - 0.5-0.59: Weak match, barely relevant
            - 0.0-0.49: Poor match, not relevant

            You MUST evaluate ALL {len(results)} results. Respond with this EXACT JSON format:
            {{
                "results": [
                    {{
                        "index": 0,
                        "relevance_score": 0.85,
                        "explanation": "Detailed explanation of why this score was given...",
                        "semantic_tags": ["button", "blue", "interface", "form"],
                        "confidence_level": "high"
                    }}
                ]
            }}

            RESULTS TO EVALUATE:
            """
            
            for i, result in enumerate(results):
                validation_prompt += f"""
                RESULT {i+1} (Index: {i}):
                - Filename: {result['filename']}
                - Visual Description: {result['visual_description'][:150]}...
                - OCR Text: {result['ocr_text'][:100]}...
                - Base Score: {result['confidence_score']:.3f}
                - Dimensions: {result['dimensions'][0]}x{result['dimensions'][1]}
                
                Analyze this result against the query "{query}" and provide:
                1. A precise relevance score (0.0-1.0)
                2. Detailed explanation of your scoring
                3. Relevant semantic tags
                4. Confidence level in your assessment
                """
            
            validation_prompt += f"""
            
            CRITICAL REQUIREMENTS:
            1. You MUST validate ALL {len(results)} results (indices 0 to {len(results)-1})
            2. Provide detailed, specific explanations for each score
            3. Be consistent in your scoring methodology
            4. Consider both visual and semantic aspects
            5. Respond ONLY with valid JSON in the exact format shown above
            6. Ensure all scores are between 0.0 and 1.0
            """
            
            logger.info("Sending enhanced validation request to OpenAI...")
            
            # Get OpenAI validation with increased limits for better accuracy
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # Using GPT-4o for better accuracy
                messages=[
                    {"role": "system", "content": "You are a precise, analytical UI/UX expert. You must respond with valid JSON only and evaluate every result comprehensively."},
                    {"role": "user", "content": validation_prompt}
                ],
                max_tokens=3000,  # Increased from 1500 for comprehensive validation
                temperature=0.1,   # Reduced for more consistent scoring
                top_p=0.95,       # Better focus
                frequency_penalty=0.1,  # Reduce repetition
                presence_penalty=0.1    # Encourage comprehensive coverage
            )
            
            logger.info("OpenAI response received, parsing enhanced validation...")
            logger.info(f"Response content: {response.choices[0].message.content[:300]}...")
            
            # Parse OpenAI response
            try:
                validation_data = json.loads(response.choices[0].message.content.strip())
                logger.info(f"Parsed validation data: {len(validation_data.get('results', []))} results")
                
                # Update results with OpenAI validation
                validated_count = 0
                for validation in validation_data.get('results', []):
                    idx = validation.get('index', 0)
                    if idx < len(results):
                        results[idx]['openai_score'] = validation.get('relevance_score', 0.0)
                        results[idx]['openai_explanation'] = validation.get('explanation', '')
                        results[idx]['openai_tags'] = validation.get('semantic_tags', [])
                        results[idx]['openai_confidence'] = validation.get('confidence_level', 'medium')
                        
                        # Calculate final score as weighted average with enhanced weighting
                        original_score = results[idx]['confidence_score']
                        openai_score = results[idx]['openai_score']
                        
                        # Enhanced weighting: 30% original algorithm, 70% OpenAI validation for better accuracy
                        final_score = (original_score * 0.3) + (openai_score * 0.7)
                        results[idx]['final_score'] = final_score
                        validated_count += 1
                        logger.info(f"Validated result {idx}: {results[idx]['filename']} - OpenAI score: {openai_score:.3f}, Final: {final_score:.3f}")
                    else:
                        logger.warning(f"OpenAI returned index {idx} but we only have {len(results)} results")
                
                logger.info(f"OpenAI validation completed: {validated_count}/{len(results)} results validated with enhanced accuracy")
                
                # Ensure all results have final scores and enhanced metadata
                for i, result in enumerate(results):
                    if 'final_score' not in result:
                        result['final_score'] = result['confidence_score']
                        result['openai_score'] = None
                        result['openai_explanation'] = 'Not validated by OpenAI'
                        result['openai_tags'] = []
                        result['openai_confidence'] = 'none'
                        logger.warning(f"Result {i} ({result['filename']}) was not validated by OpenAI")
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse OpenAI response: {e}")
                logger.warning(f"Raw response: {response.choices[0].message.content}")
                # Fallback: use original scores
                for result in results:
                    result['final_score'] = result['confidence_score']
                    result['openai_score'] = None
                    result['openai_explanation'] = 'Validation failed - JSON parsing error'
                    result['openai_tags'] = []
                    result['openai_confidence'] = 'error'
            
            return results
            
        except Exception as e:
            logger.error(f"OpenAI validation failed: {e}")
            # Fallback: use original scores
            for result in results:
                result['final_score'] = result['confidence_score']
                result['openai_score'] = None
                result['openai_explanation'] = 'Validation failed - API error'
                result['openai_tags'] = []
                result['openai_confidence'] = 'error'
            
            return results

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
