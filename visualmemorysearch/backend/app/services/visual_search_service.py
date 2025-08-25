"""
Visual search service for finding similar screenshots.
"""

import os
import json
import logging
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModel, pipeline
from sentence_transformers import SentenceTransformer
import cv2
import openai
import pytesseract
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import UploadFile
from app.core.config import get_settings
from app.models.schemas import ScreenshotInfo, SearchResult
from app.utils.logger import get_logger

logger = get_logger(__name__)

class VisualSearchService:
    """Main service for visual memory search functionality."""
    
    def __init__(self, screenshot_dir: str, user_id: Optional[str] = None):
        """Initialize the visual search service."""
        self.screenshot_dir = Path(screenshot_dir)
        self.user_id = user_id
        
        # If user_id is provided, use user-specific paths
        if user_id:
            self.user_screenshot_dir = self.screenshot_dir / f"user_{user_id}"
            self.index_file = self.user_screenshot_dir / "search_index.json"
            self.embeddings_file = self.user_screenshot_dir / "embeddings.npy"
            # Ensure user-specific directory exists
            self.user_screenshot_dir.mkdir(parents=True, exist_ok=True)
        else:
            # Global service (for admin operations)
            self.user_screenshot_dir = self.screenshot_dir
            self.index_file = self.screenshot_dir / "search_index.json"
            self.embeddings_file = self.screenshot_dir / "embeddings.npy"
        
        # Ensure screenshot directory exists
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize data structures
        self.index = {}
        self.screenshots_data = []
        self.embeddings = None
        
        # Initialize models
        self.text_model = None
        self.vision_model = None
        self.embedding_model = None
        
        # OpenAI configuration
        self.openai_client = None
        self.use_openai = self._setup_openai()
        
        # Initialize models and load index
        self._initialize_models()
        self._load_or_create_index()
    
    def _setup_openai(self) -> bool:
        """Setup OpenAI client if API key is available."""
        try:
            # Try to get user-specific API key first
            api_key = None
            if self.user_id:
                try:
                    from app.services.auth_service import get_auth_service
                    auth_service = get_auth_service()
                    api_key = auth_service.get_user_openai_key(self.user_id)
                    logger.info(f"Using user-specific OpenAI key for user {self.user_id}")
                except Exception as e:
                    logger.warning(f"Could not get user-specific OpenAI key: {e}")
            
            # Fallback to global API key if no user-specific key
            if not api_key:
                settings = get_settings()
                api_key = settings.openai_api_key
                if api_key:
                    logger.info("Using global OpenAI API key")
            
            if api_key:
                self.openai_client = openai.OpenAI(api_key=api_key)
                
                # Test the connection
                try:
                    test_response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",  # Use a default model for testing
                        messages=[{"role": "user", "content": "Hello"}],
                        max_tokens=100
                    )
                    logger.info("OpenAI API configured successfully")
                    return True
                except Exception as e:
                    logger.warning(f"OpenAI API test failed: {e}")
                    return False
            else:
                logger.info("No OpenAI API key provided, OpenAI features disabled")
                return False
        except Exception as e:
            logger.error(f"Failed to setup OpenAI: {e}")
            return False
    
    def _initialize_models(self):
        """Initialize ML models."""
        try:
            settings = get_settings()
            
            # Initialize embedding model
            logger.info("Initializing embedding model...")
            try:
                self.embedding_model = SentenceTransformer(settings.embedding_model)
                logger.info("Embedding model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize embedding model: {e}")
                self.embedding_model = None
            
            # Initialize vision model
            logger.info("Initializing vision model...")
            try:
                self.vision_model = pipeline("image-to-text", model=settings.vision_model)
                logger.info("Vision model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize vision model: {e}")
                self.vision_model = None
            
            # Initialize text model (OCR)
            logger.info("OCR model ready (pytesseract)")
            
            # Check if models are ready
            models_ready = self.embedding_model is not None and self.vision_model is not None
            logger.info(f"Models initialization complete. Ready: {models_ready}")
            
        except Exception as e:
            logger.error(f"Failed to initialize models: {e}")
            # Don't raise, just log the error and continue
    
    def _load_or_create_index(self):
        """Load existing index or create new one."""
        try:
            if self.index_file.exists():
                logger.info("Loading existing search index...")
                with open(self.index_file, 'r') as f:
                    self.index = json.load(f)
                
                if self.embeddings_file.exists():
                    self.embeddings = np.load(self.embeddings_file)
                    logger.info(f"Loaded {len(self.embeddings)} embeddings")
                else:
                    logger.warning("Embeddings file not found, will recreate index")
                    self._rebuild_index()
            else:
                logger.info("No existing index found, creating new one...")
                self._rebuild_index()
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            self._rebuild_index()
    
    def _rebuild_index(self):
        """Rebuild the search index from scratch."""
        try:
            logger.info("Rebuilding search index...")
            self.index = {}
            self.screenshots_data = []
            
            # Process all screenshots in user-specific directory
            screenshot_files = list(self.user_screenshot_dir.glob("*.png")) + \
                             list(self.user_screenshot_dir.glob("*.jpg")) + \
                             list(self.user_screenshot_dir.glob("*.jpeg"))
            
            for file_path in screenshot_files:
                self._process_screenshot(file_path)
            
            # Save index and embeddings
            self._save_index()
            logger.info(f"Index rebuilt with {len(self.screenshots_data)} screenshots")
        except Exception as e:
            logger.error(f"Failed to rebuild index: {e}")
            raise
    
    def _process_screenshot(self, file_path: Path):
        """Process a single screenshot and add to index."""
        try:
            filename = file_path.name
            
            # Create thumbnail
            thumbnail_path = self.create_thumbnail(file_path)
            
            # Extract text content
            text_content = self._extract_text(file_path)
            
            # Extract visual features
            visual_features = self._extract_visual_features(file_path)
            
            # Create screenshot info
            screenshot_info = ScreenshotInfo(
                filename=filename,
                filepath=str(file_path),
                text_content=text_content,
                visual_features=visual_features.tolist() if visual_features is not None else None,
                metadata={
                    "file_size": file_path.stat().st_size,
                    "dimensions": self._get_image_dimensions(file_path),
                    "thumbnail_path": str(thumbnail_path) if thumbnail_path else None
                }
            )
            
            # Add to data structures
            self.screenshots_data.append(screenshot_info)
            self.index[filename] = len(self.screenshots_data) - 1
            
        except Exception as e:
            logger.error(f"Failed to process screenshot {file_path}: {e}")
    
    def _extract_text(self, image_path: Path) -> str:
        """Extract text from image using OCR."""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.warning(f"Failed to extract text from {image_path}: {e}")
            return ""
    
    def _extract_visual_features(self, image_path: Path) -> Optional[np.ndarray]:
        """Extract visual features from image."""
        try:
            image = Image.open(image_path)
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # For now, return a simple feature vector
            # In a production system, you might want to use a proper vision encoder
            img_array = np.array(image)
            # Simple color histogram as features
            features = np.histogram(img_array.flatten(), bins=256, range=[0, 256])[0]
            # Normalize
            features = features / np.sum(features)
            
            return features
        except Exception as e:
            logger.warning(f"Failed to extract visual features from {image_path}: {e}")
            return None
    
    def _get_image_dimensions(self, image_path: Path) -> Dict[str, int]:
        """Get image dimensions."""
        try:
            with Image.open(image_path) as img:
                return {"width": img.width, "height": img.height}
        except Exception:
            return {"width": 0, "height": 0}
    
    def create_thumbnail(self, image_path: Path, thumbnail_size: tuple = (200, 200)) -> Optional[Path]:
        """Create a thumbnail for the given image."""
        try:
            # Create thumbnails directory
            thumbnails_dir = image_path.parent / "thumbnails"
            thumbnails_dir.mkdir(exist_ok=True)
            
            # Generate thumbnail filename
            thumbnail_name = f"thumb_{image_path.name}"
            thumbnail_path = thumbnails_dir / thumbnail_name
            
            # Create thumbnail if it doesn't exist
            if not thumbnail_path.exists():
                with Image.open(image_path) as img:
                    # Convert to RGB if necessary
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Create thumbnail
                    img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
                    
                    # Save thumbnail
                    img.save(thumbnail_path, 'JPEG', quality=85, optimize=True)
                    logger.info(f"Created thumbnail: {thumbnail_path}")
            
            return thumbnail_path
        except Exception as e:
            logger.warning(f"Failed to create thumbnail for {image_path}: {e}")
            return None
    
    def _save_index(self):
        """Save the search index and embeddings."""
        try:
            # Save index
            with open(self.index_file, 'w') as f:
                json.dump(self.index, f, indent=2)
            
            # Save embeddings if available
            if self.embeddings is not None:
                np.save(self.embeddings_file, self.embeddings)
            
            logger.info("Index saved successfully")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
    
    def list_screenshots(self) -> List[ScreenshotInfo]:
        """Get list of all indexed screenshots."""
        return self.screenshots_data
    
    def search(self, query: str, search_type: str = "combined", max_results: int = 10, user_id: Optional[str] = None) -> List[SearchResult]:
        """Search screenshots using natural language query."""
        try:
            if not self.screenshots_data:
                return []
            
            # Get query embedding
            query_embedding = self.embedding_model.encode([query])[0]
            
            results = []
            
            for screenshot_info in self.screenshots_data:
                score = 0.0
                match_type = "none"
                highlights = []
                
                # Text search
                if search_type in ["text", "combined"] and screenshot_info.text_content:
                    text_score = self._calculate_text_similarity(query, screenshot_info.text_content)
                    if text_score > score:
                        score = text_score
                        match_type = "text"
                        highlights = [screenshot_info.text_content[:100] + "..." if len(screenshot_info.text_content) > 100 else screenshot_info.text_content]
                
                # Visual search
                if search_type in ["visual", "combined"] and screenshot_info.visual_features:
                    visual_score = self._calculate_visual_similarity(query_embedding, screenshot_info.visual_features)
                    if visual_score > score:
                        score = visual_score
                        match_type = "visual"
                        highlights = ["Visual match"]
                
                # OpenAI enhanced search if available
                if self.use_openai and search_type == "combined":
                    openai_score = self._openai_enhanced_search(query, screenshot_info, user_id)
                    if openai_score > score:
                        score = openai_score
                        match_type = "ai_enhanced"
                        highlights = ["AI-enhanced match"]
                
                if score > 0:
                    results.append(SearchResult(
                        screenshot=screenshot_info,
                        score=score,
                        match_type=match_type,
                        highlights=highlights
                    ))
            
            # Sort by score and limit results
            results.sort(key=lambda x: x.score, reverse=True)
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    def _calculate_text_similarity(self, query: str, text: str) -> float:
        """Calculate text similarity using embedding model."""
        try:
            query_embedding = self.embedding_model.encode([query])[0]
            text_embedding = self.embedding_model.encode([text])[0]
            
            similarity = cosine_similarity([query_embedding], [text_embedding])[0][0]
            return float(similarity)
        except Exception as e:
            logger.warning(f"Failed to calculate text similarity: {e}")
            return 0.0
    
    def _calculate_visual_similarity(self, query_embedding: np.ndarray, visual_features: List[float]) -> float:
        """Calculate visual similarity."""
        try:
            # Convert visual features to numpy array
            visual_array = np.array(visual_features)
            
            # Simple cosine similarity
            similarity = cosine_similarity([query_embedding[:len(visual_array)]], [visual_array])[0][0]
            return float(similarity)
        except Exception as e:
            logger.warning(f"Failed to calculate visual similarity: {e}")
            return 0.0
    
    def _openai_enhanced_search(self, query: str, screenshot_info: ScreenshotInfo, user_id: Optional[str] = None) -> float:
        """Use OpenAI to enhance search results."""
        try:
            # Get user-specific OpenAI key if available
            user_openai_key = None
            if user_id:
                from app.services.auth_service import get_auth_service
                auth_service = get_auth_service()
                user_openai_key = auth_service.get_user_openai_key(user_id)
            
            # Use user-specific key or fall back to global key
            api_key = user_openai_key or get_settings().openai_api_key
            
            if not api_key:
                logger.debug("No OpenAI API key available, skipping enhanced search")
                return 0.0
            
            # Create OpenAI client with the appropriate key
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            # Create context for OpenAI
            context = f"Query: {query}\n"
            if screenshot_info.text_content:
                context += f"Text content: {screenshot_info.text_content[:500]}...\n"
            
            logger.debug(f"Making OpenAI API call for query: {query}")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that evaluates how well a screenshot matches a search query. Return only a number between 0 and 1, where 1 is a perfect match."},
                    {"role": "user", "content": f"{context}\nHow well does this screenshot match the query? Return only a number between 0 and 1."}
                ],
                max_tokens=10
            )
            
            try:
                score_text = response.choices[0].message.content.strip()
                logger.debug(f"OpenAI response: {score_text}")
                score = float(score_text)
                clamped_score = min(max(score, 0.0), 1.0)  # Clamp between 0 and 1
                logger.debug(f"OpenAI score: {clamped_score}")
                return clamped_score
            except ValueError as ve:
                logger.warning(f"Failed to parse OpenAI score '{score_text}': {ve}")
                return 0.0
                
        except Exception as e:
            logger.warning(f"OpenAI enhanced search failed: {e}")
            return 0.0
    
    async def upload_and_index_screenshot(self, file: UploadFile, user_storage_path: Optional[Path] = None) -> str:
        """Upload and index a new screenshot."""
        try:
            # Use user-specific directory
            storage_dir = self.user_screenshot_dir
            file_path = storage_dir / file.filename
            
            # Ensure directory exists
            storage_dir.mkdir(parents=True, exist_ok=True)
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Process and index the screenshot
            self._process_screenshot(file_path)
            
            # Save updated index
            self._save_index()
            
            logger.info(f"Screenshot {file.filename} uploaded and indexed successfully")
            return file.filename
            
        except Exception as e:
            logger.error(f"Failed to upload and index screenshot: {e}")
            raise
    
    def get_screenshot_info(self, filename: str) -> Optional[ScreenshotInfo]:
        """Get information about a specific screenshot."""
        if filename in self.index:
            idx = self.index[filename]
            return self.screenshots_data[idx]
        return None
    
    def delete_screenshot(self, filename: str) -> bool:
        """Delete a screenshot and remove it from the index."""
        try:
            if filename not in self.index:
                return False
            
            # Remove file from user-specific directory
            file_path = self.user_screenshot_dir / filename
            if file_path.exists():
                file_path.unlink()
            
            # Remove from index
            idx = self.index[filename]
            del self.screenshots_data[idx]
            del self.index[filename]
            
            # Rebuild index to fix indices
            self._rebuild_index()
            
            logger.info(f"Screenshot {filename} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete screenshot {filename}: {e}")
            return False
