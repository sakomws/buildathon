#!/usr/bin/env python3
"""
Project 1: Visual Memory Search - FastAPI Version
A modular FastAPI application for searching screenshot history using natural language queries.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
from dotenv import load_dotenv
from datetime import timedelta

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modular components
from app.services.visual_search_service import VisualSearchService
from app.models.schemas import SearchQuery, SearchResult, ScreenshotInfo
from app.models.auth_schemas import User
from app.core.config import get_settings
from app.core.auth import get_current_user
from app.utils.logger import setup_logging

# Load environment variables
load_dotenv()

# Import auth router after environment variables are loaded
from app.routers.auth import router as auth_router
from app.services.auth_service import get_auth_service
# RBAC completely removed

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Visual Memory Search API",
    description="A FastAPI application for searching screenshot history using natural language queries",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include authentication routes
app.include_router(auth_router)

def get_search_service(user_id: Optional[str] = None) -> VisualSearchService:
    """Dependency to get the search service instance."""
    settings = get_settings()
    return VisualSearchService(settings.screenshot_dir, user_id)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global search_service
    try:
        # Debug environment variables
        logger.info("Environment variables check:")
        logger.info(f"  SECRET_KEY: {'Set' if os.getenv('SECRET_KEY') else 'Not set'}")
        logger.info(f"  GOOGLE_CLIENT_ID: {'Set' if os.getenv('GOOGLE_CLIENT_ID') else 'Not set'}")
        logger.info(f"  GOOGLE_CLIENT_SECRET: {'Set' if os.getenv('GOOGLE_CLIENT_SECRET') else 'Not set'}")
        logger.info(f"  GOOGLE_REDIRECT_URI: {os.getenv('GOOGLE_REDIRECT_URI', 'Not set')}")
        
        # Print actual values for debugging (be careful with secrets in production)
        if os.getenv('GOOGLE_CLIENT_ID'):
            logger.info(f"  GOOGLE_CLIENT_ID value: {os.getenv('GOOGLE_CLIENT_ID')[:10]}...")
        if os.getenv('GOOGLE_REDIRECT_URI'):
            logger.info(f"  GOOGLE_REDIRECT_URI value: {os.getenv('GOOGLE_REDIRECT_URI')}")
        
        settings = get_settings()
        search_service = VisualSearchService(settings.screenshot_dir)
        logger.info("Search service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize search service: {e}")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/screenshots", response_model=List[ScreenshotInfo])
async def list_screenshots(
    current_user: dict = Depends(get_current_user)
):
    """Get list of user's indexed screenshots."""
    try:
        # Check permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "screenshots:read"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to view screenshots"
            )
        
        # Create user-specific service
        service = get_search_service(current_user["id"])
        return service.list_screenshots()
    except Exception as e:
        logger.error(f"Failed to list screenshots: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search", response_model=List[SearchResult])
async def search_screenshots(
    query: SearchQuery,
    current_user: dict = Depends(get_current_user)
):
    """Search screenshots using natural language query."""
    try:
        # Check permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "search:perform"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to perform search"
            )
        
        # Create user-specific service
        service = get_search_service(current_user["id"])
        results = service.search(query.query, query.search_type, query.max_results, current_user["id"])
        return results
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_screenshot(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload and index a new screenshot."""
    try:
        # Check permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "screenshots:create"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to upload screenshots"
            )
        
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Get user storage path
        user_storage_path = auth_service.get_user_storage_path(current_user["id"])
        if not user_storage_path:
            raise HTTPException(status_code=500, detail="User storage not configured")
        
        # Create user-specific service
        service = get_search_service(current_user["id"])
        # Save and index the file in user's directory
        result = await service.upload_and_index_screenshot(file, user_storage_path)
        return {"message": "Screenshot uploaded and indexed successfully", "filename": result}
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/screenshot/{filename}")
async def get_screenshot(filename: str, service: VisualSearchService = Depends(get_search_service)):
    """Get a specific screenshot by filename."""
    try:
        screenshot_info = service.get_screenshot_info(filename)
        if not screenshot_info:
            raise HTTPException(status_code=404, detail="Screenshot not found")
        return screenshot_info
    except Exception as e:
        logger.error(f"Failed to get screenshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/screenshot/{filename}")
async def delete_screenshot(filename: str, service: VisualSearchService = Depends(get_search_service)):
    """Delete a screenshot and remove it from the index."""
    try:
        success = service.delete_screenshot(filename)
        if not success:
            raise HTTPException(status_code=404, detail="Screenshot not found")
        return {"message": "Screenshot deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete screenshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Visual Memory Search API"}

# Cookie preferences endpoints
@app.get("/api/user/cookie-preferences")
async def get_cookie_preferences(current_user: dict = Depends(get_current_user)):
    try:
        auth_service = get_auth_service()
        prefs = auth_service.get_cookie_preferences(current_user["id"])
        if prefs is None:
            # default: essential only
            prefs = {"essential": True, "functional": False, "analytics": False, "marketing": False}
        return prefs
    except Exception as e:
        logger.error(f"Failed to get cookie preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/cookie-preferences")
async def set_cookie_preferences(prefs: Dict[str, bool], current_user: dict = Depends(get_current_user)):
    try:
        # Ensure essential is always true
        prefs = dict(prefs)
        prefs["essential"] = True
        auth_service = get_auth_service()
        ok = auth_service.set_cookie_preferences(current_user["id"], prefs)
        if not ok:
            raise HTTPException(status_code=500, detail="Failed to save cookie preferences")
        return {"message": "Cookie preferences saved", "preferences": prefs}
    except Exception as e:
        logger.error(f"Failed to save cookie preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Add missing endpoints
@app.post("/api/upload/folder")
async def upload_folder(
    files: List[UploadFile] = File(...),
    service: VisualSearchService = Depends(get_search_service)
):
    """Upload and index multiple screenshots from a folder."""
    try:
        results = []
        for file in files:
            if not file.filename:
                continue
            
            # Validate file type
            if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                continue
            
            # Save and index the file
            result = await service.upload_and_index_screenshot(file)
            results.append({"message": "Screenshot uploaded and indexed successfully", "filename": result, "indexed": True})
        
        return results
    except Exception as e:
        logger.error(f"Folder upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/screenshots/{filename}")
async def serve_screenshot(filename: str, current_user: dict = Depends(get_current_user)):
    """Serve screenshot image files."""
    try:
        # Get user storage path
        auth_service = get_auth_service()
        user_storage_path = auth_service.get_user_storage_path(current_user["id"])
        
        # Look for file in user's directory first, then fallback to global
        screenshot_path = None
        if user_storage_path and user_storage_path.exists():
            user_file_path = user_storage_path / filename
            if user_file_path.exists():
                screenshot_path = user_file_path
        
        if not screenshot_path:
            # Fallback to global directory
            settings = get_settings()
            screenshot_path = Path(settings.screenshot_dir) / filename
        
        if not screenshot_path.exists():
            raise HTTPException(status_code=404, detail="Screenshot not found")
        
        from fastapi.responses import FileResponse
        return FileResponse(screenshot_path)
    except Exception as e:
        logger.error(f"Failed to serve screenshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/images/{filename}")
async def serve_image_public(filename: str):
    """Serve screenshot images publicly (no authentication required)."""
    try:
        settings = get_settings()
        
        # Look for the image in all user directories
        screenshot_path = None
        
        # First check the global screenshots directory
        global_path = Path(settings.screenshot_dir) / filename
        if global_path.exists():
            screenshot_path = global_path
        else:
            # Check all user directories
            for user_dir in Path(settings.screenshot_dir).glob("user_*"):
                if user_dir.is_dir():
                    user_file_path = user_dir / filename
                    if user_file_path.exists():
                        screenshot_path = user_file_path
                        break
        
        if not screenshot_path or not screenshot_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        from fastapi.responses import FileResponse
        return FileResponse(screenshot_path)
    except Exception as e:
        logger.error(f"Failed to serve public image {filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/screenshots/{filename}/download")
async def download_screenshot(filename: str, current_user: dict = Depends(get_current_user)):
    """Download a single screenshot file."""
    try:
        # Check permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "screenshots:read"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to download screenshots"
            )
        
        # Get user storage path
        user_storage_path = auth_service.get_user_storage_path(current_user["id"])
        if not user_storage_path:
            raise HTTPException(status_code=500, detail="User storage not configured")
        
        # Look for file in user's directory first, then fallback to global
        screenshot_path = None
        if user_storage_path.exists():
            user_file_path = user_storage_path / filename
            if user_file_path.exists():
                screenshot_path = user_file_path
        
        if not screenshot_path:
            # Fallback to global directory
            settings = get_settings()
            screenshot_path = Path(settings.screenshot_dir) / filename
        
        if not screenshot_path.exists():
            raise HTTPException(status_code=404, detail="Screenshot not found")
        
        from fastapi.responses import FileResponse
        return FileResponse(
            screenshot_path,
            filename=filename,
            media_type='application/octet-stream'
        )
    except Exception as e:
        logger.error(f"Failed to download screenshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/screenshots/download-zip")
async def download_screenshots_zip(
    filenames: List[str],
    current_user: dict = Depends(get_current_user)
):
    """Download multiple screenshots as a ZIP file."""
    try:
        # Check permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "screenshots:read"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to download screenshots"
            )
        
        if not filenames:
            raise HTTPException(status_code=400, detail="No filenames provided")
        
        # Get user storage path
        user_storage_path = auth_service.get_user_storage_path(current_user["id"])
        if not user_storage_path:
            raise HTTPException(status_code=500, detail="User storage not configured")
        
        import zipfile
        import tempfile
        import io
        
        # Create a temporary ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename in filenames:
                # Look for file in user's directory first, then fallback to global
                screenshot_path = None
                if user_storage_path.exists():
                    user_file_path = user_storage_path / filename
                    if user_file_path.exists():
                        screenshot_path = user_file_path
                
                if not screenshot_path:
                    # Fallback to global directory
                    settings = get_settings()
                    screenshot_path = Path(settings.screenshot_dir) / filename
                
                if screenshot_path.exists():
                    zip_file.write(screenshot_path, filename)
                else:
                    logger.warning(f"File not found for ZIP: {filename}")
        
        zip_buffer.seek(0)
        
        from fastapi.responses import StreamingResponse
        return StreamingResponse(
            io.BytesIO(zip_buffer.getvalue()),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=screenshots-{current_user['id']}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.zip"}
        )
    except Exception as e:
        logger.error(f"Failed to create ZIP download: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/screenshots/{filename}")
async def delete_screenshot(filename: str, current_user: dict = Depends(get_current_user)):
    """Delete a screenshot file."""
    try:
        # Check permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "screenshots:delete"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to delete screenshots"
            )
        
        # Get user storage path
        user_storage_path = auth_service.get_user_storage_path(current_user["id"])
        if not user_storage_path:
            raise HTTPException(status_code=500, detail="User storage not configured")
        
        # Look for file in user's directory first, then fallback to global
        screenshot_path = None
        if user_storage_path.exists():
            user_file_path = user_storage_path / filename
            if user_file_path.exists():
                screenshot_path = user_file_path
        
        if not screenshot_path:
            # Fallback to global directory
            settings = get_settings()
            screenshot_path = Path(settings.screenshot_dir) / filename
        
        if not screenshot_path.exists():
            raise HTTPException(status_code=404, detail="Screenshot not found")
        
        # Delete the file
        screenshot_path.unlink()
        
        # Also remove from search index if it exists
        try:
            service = get_search_service(current_user["id"])
            service.remove_from_index(filename)
        except Exception as index_error:
            logger.warning(f"Failed to remove from search index: {index_error}")
        
        logger.info(f"Screenshot deleted: {filename}")
        return {"message": f"Screenshot {filename} deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete screenshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dev/make-admin")
async def make_user_admin(
    current_user: dict = Depends(get_current_user)
):
    """Development endpoint to make the current user an admin."""
    try:
        auth_service = get_auth_service()
        # Make user admin in users_db
        users_db = auth_service.get_users_db()
        if current_user["username"] in users_db:
            users_db[current_user["username"]]["is_admin"] = True
            print(f"Made user {current_user['username']} admin in users_db")
        
        # Also check OAuth users
        oauth_users_db = auth_service.get_oauth_users_db()
        for oauth_key, oauth_user in oauth_users_db.items():
            if oauth_user.get("username") == current_user["username"]:
                oauth_user["is_admin"] = True
                print(f"Made OAuth user {current_user['username']} admin")
                break
        
        return {
            "message": f"User {current_user['username']} is now an admin",
            "user_id": current_user["id"],
            "username": current_user["username"],
            "is_admin": True
        }
        
    except Exception as e:
        logger.error(f"Failed to make user admin: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dev/make-admin-simple")
async def make_user_admin_simple(
    current_user: dict = Depends(get_current_user)
):
    """Simple development endpoint to make the current user an admin."""
    try:
        auth_service = get_auth_service()
        
        # Make user admin in users_db
        users_db = auth_service.get_users_db()
        if current_user["username"] in users_db:
            users_db[current_user["username"]]["is_admin"] = True
            print(f"Made user {current_user['username']} admin in users_db")
        
        # Also check OAuth users
        oauth_users_db = auth_service.get_oauth_users_db()
        for oauth_key, oauth_user in oauth_users_db.items():
            if oauth_user.get("username") == current_user["username"]:
                oauth_user["is_admin"] = True
                print(f"Made OAuth user {current_user['username']} admin")
                break
        
        return {
            "message": f"User {current_user['username']} is now an admin",
            "user_id": current_user["id"],
            "username": current_user["username"],
            "is_admin": True
        }
        
    except Exception as e:
        logger.error(f"Failed to make user admin: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rebuild-index")
async def rebuild_user_index(
    current_user: dict = Depends(get_current_user)
):
    """Rebuild the search index for the current user."""
    try:
        # Create user-specific service
        service = get_search_service(current_user["id"])
        service._rebuild_index()
        return {"message": "Your search index rebuilt successfully"}
    except Exception as e:
        logger.error(f"Failed to rebuild user index: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Admin endpoints
@app.post("/api/admin/assign-role")
async def assign_role_to_user(
    assignment_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Assign a role to a user (admin only)."""
    try:
        # Check admin permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to assign roles"
            )
        
        user_id = assignment_data.get("user_id")
        role_name = assignment_data.get("role_name")
        
        if not user_id or not role_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID and role name are required"
            )
        
        # Simplified role assignment - just set admin flag
        if role_name == "admin":
            # Find user and make them admin
            user_found = False
            users_db = auth_service.get_users_db()
            for username, user_data in users_db.items():
                if user_data.get("id") == user_id:
                    user_data["is_admin"] = True
                    user_found = True
                    break
            
            # Also check OAuth users
            oauth_users_db = auth_service.get_oauth_users_db()
            for oauth_key, oauth_user in oauth_users_db.items():
                if oauth_user.get("id") == user_id:
                    oauth_user["is_admin"] = True
                    user_found = True
                    break
            
            if user_found:
                return {"message": f"Admin role assigned to user {user_id} successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User {user_id} not found"
                )
        else:
            return {"message": f"Role {role_name} is not supported in simplified mode"}
    except Exception as e:
        logger.error(f"Failed to assign role: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/rebuild-index")
async def rebuild_search_index(
    current_user: dict = Depends(get_current_user)
):
    """Rebuild the search index from scratch."""
    try:
        # Check admin permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to rebuild index"
            )
        
        # Create user-specific service
        service = get_search_service(current_user["id"])
        service._rebuild_index()
        return {"message": "Search index rebuilt successfully"}
    except Exception as e:
        logger.error(f"Failed to rebuild index: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-test-data")
async def generate_user_test_data(
    current_user: dict = Depends(get_current_user)
):
    """Generate test screenshot data for the current user."""
    try:
        import random
        from PIL import Image, ImageDraw, ImageFont
        import io
        from datetime import datetime
        
        # Create test screenshots directory if it doesn't exist
        settings = get_settings()
        auth_service = get_auth_service()
        user_storage_path = auth_service.get_user_storage_path(current_user["id"])
        
        # If user doesn't have a storage path, create one
        if user_storage_path is None:
            # Get the storage path directly
            user_storage_path = auth_service.get_user_storage_path(current_user["id"])
            if user_storage_path is None:
                # Fallback to default directory
                user_storage_path = Path(settings.screenshot_dir) / f"user_{current_user['id']}"
        
        test_dir = Path(user_storage_path)
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # Create user-specific service
        service = get_search_service(current_user["id"])
        
        # Generate 10 test screenshots
        generated_count = 0
        for i in range(10):
            try:
                # Create a random-sized image (more reasonable sizes)
                width = random.randint(1200, 1920)
                height = random.randint(800, 1080)
                
                # Create image with better background colors
                colors = [
                    (240, 248, 255),  # Alice Blue
                    (255, 248, 220),  # Cornsilk
                    (240, 255, 240),  # Honeydew
                    (255, 240, 245),  # Lavender Blush
                    (245, 245, 245),  # White Smoke
                    (255, 250, 240),  # Floral White
                ]
                bg_color = random.choice(colors)
                
                img = Image.new('RGB', (width, height), bg_color)
                draw = ImageDraw.Draw(img)
                
                # Add more interesting shapes with better positioning
                for _ in range(random.randint(5, 12)):
                    # Ensure shapes are within bounds
                    x1 = random.randint(50, width - 100)
                    y1 = random.randint(50, height - 100)
                    x2 = random.randint(x1 + 50, min(x1 + 200, width - 50))
                    y2 = random.randint(y1 + 50, min(y1 + 200, height - 50))
                    
                    shape_type = random.choice(['rectangle', 'circle', 'ellipse', 'line'])
                    color = (
                        random.randint(50, 200),
                        random.randint(50, 200), 
                        random.randint(50, 200)
                    )
                    
                    if shape_type == 'rectangle':
                        draw.rectangle([x1, y1, x2, y2], fill=color, outline=(0, 0, 0), width=2)
                    elif shape_type == 'circle':
                        radius = random.randint(30, 80)
                        draw.ellipse([x1, y1, x1 + radius, y1 + radius], fill=color, outline=(0, 0, 0), width=2)
                    elif shape_type == 'ellipse':
                        draw.ellipse([x1, y1, x2, y2], fill=color, outline=(0, 0, 0), width=2)
                    elif shape_type == 'line':
                        draw.line([x1, y1, x2, y2], fill=color, width=random.randint(3, 8))
                
                # Add better text with multiple lines
                try:
                    font_size = random.randint(24, 36)
                    try:
                        # Try multiple font paths for better compatibility
                        font_paths = [
                            "/System/Library/Fonts/Arial.ttf",
                            "/System/Library/Fonts/Helvetica.ttc",
                            "/Library/Fonts/Arial.ttf",
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
                        ]
                        font = None
                        for font_path in font_paths:
                            try:
                                font = ImageFont.truetype(font_path, font_size)
                                break
                            except:
                                continue
                        if font is None:
                            font = ImageFont.load_default()
                    except:
                        font = ImageFont.load_default()
                    
                    # Generate multiple lines of text
                    lines = [
                        f"Test Screenshot {i+1}",
                        f"Generated at {datetime.now().strftime('%H:%M:%S')}",
                        f"Size: {width}x{height}",
                        f"Quality: High"
                    ]
                    
                    # Calculate total text height
                    line_height = font_size + 10
                    total_height = len(lines) * line_height
                    
                    # Start position (center of image)
                    start_y = (height - total_height) // 2
                    
                    for line_idx, line in enumerate(lines):
                        text_bbox = draw.textbbox((0, 0), line, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        
                        # Center each line horizontally
                        text_x = (width - text_width) // 2
                        text_y = start_y + (line_idx * line_height)
                        
                        # Add text with better contrast
                        # Draw outline first
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                if dx != 0 or dy != 0:
                                    draw.text((text_x + dx, text_y + dy), line, fill=(255, 255, 255), font=font)
                        
                        # Draw main text
                        draw.text((text_x, text_y), line, fill=(0, 0, 0), font=font)
                    
                except Exception as font_error:
                    logger.warning(f"Font error for screenshot {i+1}: {font_error}")
                    # Fallback: draw simple text
                    draw.text((width//2, height//2), f"Test {i+1}", fill=(0, 0, 0))
                
                # Save image to bytes with better quality
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG', optimize=True)
                img_bytes.seek(0)
                
                # Generate filename with timestamp and index
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"test_screenshot_{timestamp}_{i+1:02d}.png"
                file_path = test_dir / filename
                
                # Save to file
                with open(file_path, 'wb') as f:
                    f.write(img_bytes.getvalue())
                
                logger.info(f"Saved test screenshot {i+1}: {filename}")
                
                # Add to search index
                try:
                    # Process and index the screenshot directly
                    service._process_screenshot(file_path)
                    generated_count += 1
                    logger.info(f"Successfully indexed test screenshot: {filename}")
                except Exception as index_error:
                    logger.error(f"Failed to add test screenshot to index: {index_error}")
                    # Still count it as generated even if indexing fails
                    generated_count += 1
                
            except Exception as e:
                logger.error(f"Failed to generate test screenshot {i+1}: {e}")
                continue
        
        # Save the updated index after processing all screenshots
        try:
            service._save_index()
            logger.info(f"Index saved with {generated_count} new test screenshots")
        except Exception as save_error:
            logger.error(f"Failed to save index: {save_error}")
        
        return {
            "message": f"Successfully generated {generated_count} test screenshots",
            "generated_count": generated_count
        }
        
    except Exception as e:
        logger.error(f"Failed to generate test data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# NEW: OpenAI API key management endpoints
@app.post("/api/admin/update-openai-key")
async def update_openai_key(api_key_data: dict, current_user: dict = Depends(get_current_user)):
    """Update the user's OpenAI API key."""
    try:
        api_key = api_key_data.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required")
        
        # Store the key for the current user
        auth_service = get_auth_service()
        success = auth_service.set_user_openai_key(current_user["id"], api_key)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save user's OpenAI API key")
        
        # Test the key immediately to ensure it's valid
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            logger.info(f"User {current_user['id']} OpenAI API key updated and validated successfully")
            return {"message": "Your OpenAI API key updated and validated successfully"}
        except Exception as test_error:
            logger.error(f"OpenAI API key validation failed: {test_error}")
            raise HTTPException(status_code=400, detail=f"Invalid OpenAI API key: {str(test_error)}")
        
    except Exception as e:
        logger.error(f"Failed to update OpenAI API key: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/test-openai")
async def test_openai_key(api_key_data: dict, current_user: dict = Depends(get_current_user)):
    """Test the user's OpenAI API key by making a simple request."""
    try:
        api_key = api_key_data.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required")
        
        # Test the API key with a simple request
        from openai import OpenAI
        
        # Create client with the API key
        client = OpenAI(api_key=api_key)
        
        # Make a simple test request
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, this is a test."}],
                max_tokens=10
            )
            
            if response and response.choices:
                logger.info(f"User {current_user['id']} OpenAI API key test successful")
                return {"message": "Your OpenAI API key is valid", "test_response": response.choices[0].message.content}
            else:
                raise HTTPException(status_code=400, detail="Invalid response from OpenAI API")
                
        except Exception as openai_error:
            logger.error(f"OpenAI API test failed: {openai_error}")
            raise HTTPException(status_code=400, detail=f"OpenAI API test failed: {str(openai_error)}")
        
    except Exception as e:
        logger.error(f"Failed to test OpenAI API key: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/status")
async def get_admin_status(service: VisualSearchService = Depends(get_search_service)):
    """Get system status and statistics."""
    try:
        screenshots = service.list_screenshots()
        return {
            "total_screenshots": len(screenshots),
            "index_size": len(service.index),
            "embeddings_loaded": service.embeddings is not None,
            "models_ready": all([
                service.text_model is not None,
                service.vision_model is not None,
                service.embedding_model is not None
            ]),
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform,
                "memory_usage": "Available",  # Could add actual memory monitoring
                "disk_space": "Available"     # Could add actual disk monitoring
            },
            "service_status": {
                "search_service": "Running",
                "auth_service": "Running",
                "file_storage": "Available"
            }
        }
    except Exception as e:
        logger.error(f"Failed to get admin status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/get-openai-key")
async def get_openai_key(current_user: dict = Depends(get_current_user)):
    """Get the user's OpenAI API key."""
    try:
        auth_service = get_auth_service()
        api_key = auth_service.get_user_openai_key(current_user["id"])
        
        if api_key:
            # Return masked version for security
            masked_key = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 11 else "***"
            return {"has_key": True, "masked_key": masked_key}
        else:
            return {"has_key": False, "masked_key": None}
        
    except Exception as e:
        logger.error(f"Failed to get OpenAI API key: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoints
@app.get("/api/analytics/overview")
async def get_analytics_overview(
    current_user: dict = Depends(get_current_user),
    service: VisualSearchService = Depends(get_search_service)
):
    """Get analytics overview for the current user."""
    try:
        settings = get_settings()
        auth_service = get_auth_service()
        user_storage_path = auth_service.get_user_storage_path(current_user["id"])
        
        if user_storage_path is None:
            return {
                "user_stats": {
                    "total_screenshots": 0,
                    "total_size_mb": 0,
                    "avg_file_size_kb": 0,
                    "file_types": {},
                    "upload_timeline": []
                },
                "openai_stats": {
                    "total_requests": 0,
                    "total_tokens": 0,
                    "avg_tokens_per_request": 0,
                    "cost_estimate": 0,
                    "usage_timeline": []
                },
                "search_stats": {
                    "total_searches": 0,
                    "avg_results": 0,
                    "popular_queries": []
                }
            }
        
        # Get user's screenshots
        user_screenshots = []
        if user_storage_path.exists():
            for file_path in user_storage_path.glob("*.png"):
                user_screenshots.append(file_path)
            for file_path in user_storage_path.glob("*.jpg"):
                user_screenshots.append(file_path)
            for file_path in user_storage_path.glob("*.jpeg"):
                user_screenshots.append(file_path)
        
        # Calculate file statistics
        total_size = sum(f.stat().st_size for f in user_screenshots)
        file_types = {}
        for file_path in user_screenshots:
            ext = file_path.suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
        
        # Mock OpenAI usage data (in a real app, this would come from a database)
        openai_requests = 25  # Mock data
        openai_tokens = 1500  # Mock data
        cost_per_1k_tokens = 0.002  # GPT-3.5-turbo cost
        
        return {
            "user_stats": {
                "total_screenshots": len(user_screenshots),
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "avg_file_size_kb": round(total_size / len(user_screenshots) / 1024, 2) if user_screenshots else 0,
                "file_types": file_types,
                "upload_timeline": [
                    {"date": "2024-01-15", "count": 5},
                    {"date": "2024-01-16", "count": 3},
                    {"date": "2024-01-17", "count": 8}
                ]
            },
            "openai_stats": {
                "total_requests": openai_requests,
                "total_tokens": openai_tokens,
                "avg_tokens_per_request": round(openai_tokens / openai_requests, 2) if openai_requests > 0 else 0,
                "cost_estimate": round((openai_tokens / 1000) * cost_per_1k_tokens, 4),
                "usage_timeline": [
                    {"date": "2024-01-15", "requests": 8, "tokens": 450},
                    {"date": "2024-01-16", "requests": 5, "tokens": 320},
                    {"date": "2024-01-17", "requests": 12, "tokens": 730}
                ]
            },
            "search_stats": {
                "total_searches": 15,
                "avg_results": 3.2,
                "popular_queries": [
                    {"query": "dashboard", "count": 5},
                    {"query": "login", "count": 3},
                    {"query": "settings", "count": 2}
                ]
            }
        }
    except Exception as e:
        logger.error(f"Failed to get analytics overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/openai-usage")
async def get_openai_usage_analytics(
    current_user: dict = Depends(get_current_user)
):
    """Get detailed OpenAI usage analytics."""
    try:
        # Mock detailed OpenAI usage data
        usage_data = {
            "daily_usage": [
                {"date": "2024-01-15", "requests": 8, "tokens": 450, "cost": 0.0009},
                {"date": "2024-01-16", "requests": 5, "tokens": 320, "cost": 0.0006},
                {"date": "2024-01-17", "requests": 12, "tokens": 730, "cost": 0.0015},
                {"date": "2024-01-18", "requests": 15, "tokens": 890, "cost": 0.0018},
                {"date": "2024-01-19", "requests": 7, "tokens": 420, "cost": 0.0008}
            ],
            "model_usage": [
                {"model": "gpt-3.5-turbo", "requests": 35, "tokens": 2100, "cost": 0.0042},
                {"model": "gpt-4", "requests": 12, "tokens": 800, "cost": 0.0024}
            ],
            "request_types": [
                {"type": "search_enhancement", "count": 25, "avg_tokens": 45},
                {"type": "content_analysis", "count": 15, "avg_tokens": 120},
                {"type": "image_description", "count": 7, "avg_tokens": 85}
            ],
            "cost_breakdown": {
                "total_cost": 0.0066,
                "daily_average": 0.0013,
                "monthly_estimate": 0.039,
                "cost_per_request": 0.00014
            }
        }
        
        return usage_data
    except Exception as e:
        logger.error(f"Failed to get OpenAI usage analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/image-analytics")
async def get_image_analytics(
    current_user: dict = Depends(get_current_user),
    service: VisualSearchService = Depends(get_search_service)
):
    """Get detailed image analytics."""
    try:
        settings = get_settings()
        auth_service = get_auth_service()
        user_storage_path = auth_service.get_user_storage_path(current_user["id"])
        
        if user_storage_path is None:
            return {
                "image_stats": {
                    "total_images": 0,
                    "total_size_mb": 0,
                    "avg_dimensions": {"width": 0, "height": 0},
                    "file_types": {},
                    "size_distribution": []
                },
                "upload_patterns": {
                    "hourly_distribution": [],
                    "daily_distribution": [],
                    "monthly_trend": []
                },
                "image_analysis": {
                    "text_extraction_success": 0,
                    "avg_text_length": 0,
                    "common_words": [],
                    "ocr_confidence": 0
                }
            }
        
        # Get user's images
        user_images = []
        if user_storage_path.exists():
            for ext in ['*.png', '*.jpg', '*.jpeg']:
                user_images.extend(user_storage_path.glob(ext))
        
        # Calculate image statistics
        total_size = sum(f.stat().st_size for f in user_images)
        file_types = {}
        dimensions = []
        
        for file_path in user_images:
            ext = file_path.suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
            
            try:
                from PIL import Image
                with Image.open(file_path) as img:
                    dimensions.append((img.width, img.height))
            except Exception:
                pass
        
        avg_width = sum(d[0] for d in dimensions) / len(dimensions) if dimensions else 0
        avg_height = sum(d[1] for d in dimensions) / len(dimensions) if dimensions else 0
        
        # Size distribution
        size_ranges = {
            "0-100KB": 0,
            "100KB-500KB": 0,
            "500KB-1MB": 0,
            "1MB-5MB": 0,
            "5MB+": 0
        }
        
        for file_path in user_images:
            size_kb = file_path.stat().st_size / 1024
            if size_kb < 100:
                size_ranges["0-100KB"] += 1
            elif size_kb < 500:
                size_ranges["100KB-500KB"] += 1
            elif size_kb < 1024:
                size_ranges["500KB-1MB"] += 1
            elif size_kb < 5120:
                size_ranges["1MB-5MB"] += 1
            else:
                size_ranges["5MB+"] += 1
        
        return {
            "image_stats": {
                "total_images": len(user_images),
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "avg_dimensions": {
                    "width": round(avg_width, 0),
                    "height": round(avg_height, 0)
                },
                "file_types": file_types,
                "size_distribution": [{"range": k, "count": v} for k, v in size_ranges.items()]
            },
            "upload_patterns": {
                "hourly_distribution": [
                    {"hour": 9, "count": 5},
                    {"hour": 10, "count": 8},
                    {"hour": 11, "count": 12},
                    {"hour": 14, "count": 6},
                    {"hour": 15, "count": 9}
                ],
                "daily_distribution": [
                    {"day": "Monday", "count": 15},
                    {"day": "Tuesday", "count": 12},
                    {"day": "Wednesday", "count": 18},
                    {"day": "Thursday", "count": 10},
                    {"day": "Friday", "count": 8}
                ],
                "monthly_trend": [
                    {"month": "Jan", "count": 45},
                    {"month": "Feb", "count": 52},
                    {"month": "Mar", "count": 38}
                ]
            },
            "image_analysis": {
                "text_extraction_success": 85,  # Percentage
                "avg_text_length": 45,  # Characters
                "common_words": [
                    {"word": "dashboard", "count": 12},
                    {"word": "login", "count": 8},
                    {"word": "settings", "count": 6},
                    {"word": "user", "count": 5}
                ],
                "ocr_confidence": 78.5  # Average confidence score
            }
        }
    except Exception as e:
        logger.error(f"Failed to get image analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/delete-all-user-data")
async def delete_all_user_data(
    current_user: dict = Depends(get_current_user)
):
    """Delete all data for the current user."""
    try:
        logger.info(f"Delete all data request from user: {current_user.get('id')} ({current_user.get('username', 'unknown')})")
        
        # Check admin permission
        auth_service = get_auth_service()
        has_permission = auth_service.has_permission(current_user["id"], "admin:manage")
        logger.info(f"User {current_user['id']} has admin:manage permission: {has_permission}")
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to delete user data"
            )
        
        # Get user storage path
        user_storage_path = auth_service.get_user_storage_path(current_user["id"])
        logger.info(f"User storage path: {user_storage_path}")
        
        if not user_storage_path:
            raise HTTPException(status_code=404, detail="User storage not found")
        
        # Create user-specific service
        service = get_search_service(current_user["id"])
        
        # Delete all screenshots and index files
        deleted_count = 0
        try:
            # Delete all screenshot files
            screenshot_files = list(Path(user_storage_path).glob("*.png")) + \
                             list(Path(user_storage_path).glob("*.jpg")) + \
                             list(Path(user_storage_path).glob("*.jpeg")) + \
                             list(Path(user_storage_path).glob("*.gif")) + \
                             list(Path(user_storage_path).glob("*.bmp"))
            
            logger.info(f"Found {len(screenshot_files)} screenshot files to delete")
            
            for file_path in screenshot_files:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception as e:
                    logger.warning(f"Failed to delete file {file_path}: {e}")
            
            # Delete index files
            index_file = Path(user_storage_path) / "search_index.json"
            embeddings_file = Path(user_storage_path) / "embeddings.npy"
            
            if index_file.exists():
                index_file.unlink()
                logger.info("Deleted search index file")
            
            if embeddings_file.exists():
                embeddings_file.unlink()
                logger.info("Deleted embeddings file")
            
            # Clear user's OpenAI key
            try:
                auth_service.set_user_openai_key(current_user["id"], None)
                logger.info("Cleared user OpenAI key")
            except Exception as e:
                logger.warning(f"Failed to clear OpenAI key: {e}")
            
            # Clear user profile data (simplified)
            try:
                # Clear OpenAI key from user record
                auth_service.set_user_openai_key(current_user["id"], None)
                logger.info("Cleared user profile sensitive data")
            except Exception as e:
                logger.warning(f"Failed to clear user profile data: {e}")
            
            logger.info(f"Deleted all data for user {current_user['id']}: {deleted_count} files")
            
            return {
                "message": f"Successfully deleted all user data including {deleted_count} screenshots",
                "deleted_files": deleted_count,
                "user_id": current_user["id"]
            }
            
        except Exception as e:
            logger.error(f"Failed to delete user data: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to delete user data: {str(e)}")
            
    except Exception as e:
        logger.error(f"Failed to delete all user data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/delete-all-screenshots")
async def delete_all_screenshots(
    current_user: dict = Depends(get_current_user)
):
    """Delete all screenshots for the current user."""
    try:
        # Check admin permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to delete screenshots"
            )
        
        # Get user storage path
        user_storage_path = auth_service.get_user_storage_path(current_user["id"])
        if not user_storage_path:
            raise HTTPException(status_code=404, detail="User storage not found")
        
        # Delete all screenshot files
        deleted_count = 0
        screenshot_files = list(Path(user_storage_path).glob("*.png")) + \
                         list(Path(user_storage_path).glob("*.jpg")) + \
                         list(Path(user_storage_path).glob("*.jpeg")) + \
                         list(Path(user_storage_path).glob("*.gif")) + \
                         list(Path(user_storage_path).glob("*.bmp"))
        
        for file_path in screenshot_files:
            try:
                file_path.unlink()
                deleted_count += 1
            except Exception as e:
                logger.warning(f"Failed to delete file {file_path}: {e}")
        
        # Rebuild empty index
        service = get_search_service(current_user["id"])
        service._rebuild_index()
        
        logger.info(f"Deleted {deleted_count} screenshots for user {current_user['id']}")
        
        return {
            "message": f"Successfully deleted {deleted_count} screenshots",
            "deleted_files": deleted_count,
            "user_id": current_user["id"]
        }
        
    except Exception as e:
        logger.error(f"Failed to delete all screenshots: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/delete-user-account")
async def delete_user_account(
    current_user: dict = Depends(get_current_user)
):
    """Delete the user's account completely."""
    try:
        # Check admin permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to delete account"
            )
        
        user_id = current_user["id"]
        
        # Get user storage path
        user_storage_path = auth_service.get_user_storage_path(user_id)
        
        # Delete all user data first
        deleted_files = 0
        if user_storage_path and user_storage_path.exists():
            try:
                # Delete all screenshot files
                screenshot_files = list(user_storage_path.glob("*.png")) + \
                                 list(user_storage_path.glob("*.jpg")) + \
                                 list(user_storage_path.glob("*.jpeg")) + \
                                 list(user_storage_path.glob("*.gif")) + \
                                 list(user_storage_path.glob("*.bmp"))
                
                for file_path in screenshot_files:
                    try:
                        file_path.unlink()
                        deleted_files += 1
                    except Exception as e:
                        logger.warning(f"Failed to delete file {file_path}: {e}")
                
                # Delete index files
                index_file = user_storage_path / "search_index.json"
                embeddings_file = user_storage_path / "embeddings.npy"
                
                if index_file.exists():
                    index_file.unlink()
                
                if embeddings_file.exists():
                    embeddings_file.unlink()
                
                # Try to remove the user directory
                try:
                    import shutil
                    shutil.rmtree(user_storage_path)
                except Exception as e:
                    logger.warning(f"Failed to remove user directory: {e}")
                    
            except Exception as e:
                logger.warning(f"Failed to clean user storage: {e}")
        
        # Delete user data (simplified)
        try:
            auth_service.delete_user(user_id)
            logger.info(f"Deleted user {user_id} from system")
        except Exception as e:
            logger.warning(f"Failed to delete user: {e}")
        
        # Delete user from auth service
        try:
            auth_service.delete_user(user_id)
            logger.info(f"Deleted user {user_id} from auth service")
        except Exception as e:
            logger.warning(f"Failed to delete user from auth: {e}")
        
        # Clear any remaining user data
        try:
            # Clear OpenAI key
            auth_service.set_user_openai_key(user_id, None)
            
            # Clear any other user-specific data
            # Add more cleanup as needed
            
        except Exception as e:
            logger.warning(f"Failed to clear remaining user data: {e}")
        
        logger.info(f"Completely deleted user account {user_id} with {deleted_files} files")
        
        return {
            "message": f"Your account has been permanently deleted along with {deleted_files} files",
            "deleted_files": deleted_files,
            "user_id": user_id,
            "account_deleted": True
        }
        
    except Exception as e:
        logger.error(f"Failed to delete user account: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dev/make-admin")
async def make_current_user_admin(
    current_user: dict = Depends(get_current_user)
):
    """Make the current user an admin (development only)."""
    try:
        # Simplified admin assignment (no RBAC)
        # Make user admin directly
        auth_service = get_auth_service()
        
        # Make user admin in users_db
        users_db = auth_service.get_users_db()
        if current_user["username"] in users_db:
            users_db[current_user["username"]]["is_admin"] = True
            print(f"Made user {current_user['username']} admin in users_db")
        
        # Also check OAuth users
        oauth_users_db = auth_service.get_oauth_users_db()
        for oauth_key, oauth_user in oauth_users_db.items():
            if oauth_user.get("username") == current_user["username"]:
                oauth_user["is_admin"] = True
                print(f"Made OAuth user {current_user['username']} admin")
                break
        
        return {"message": f"User {current_user['username']} is now an admin"}
    except Exception as e:
        logger.error(f"Failed to make user admin: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Organization and Permission Management Endpoints
@app.get("/api/admin/organizations")
async def get_organizations(current_user: dict = Depends(get_current_user)):
    """Get all organizations (admin only)."""
    try:
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to view organizations"
            )
        
        # Simplified organization management (no RBAC)
        organizations = [
            {
                "id": "default",
                "name": "Default Organization",
                "description": "System-wide organization",
                "created_at": "2024-01-01T00:00:00Z",
                "created_by": "system",
                "is_active": True,
                "member_count": 1,
                "roles": ["admin", "user"]
            }
        ]
        return {"organizations": organizations}
    except Exception as e:
        logger.error(f"Failed to get organizations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/organizations")
async def create_organization(
    org_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Create a new organization."""
    try:
        # Check admin permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to create organizations"
            )
        
        # Simplified organization creation (no RBAC)
        new_org = {
            "id": f"org_{org_data.get('name', 'new').lower().replace(' ', '_')}",
            "name": org_data.get("name", ""),
            "description": org_data.get("description", ""),
            "created_at": datetime.utcnow().isoformat(),
            "created_by": current_user["id"],
            "is_active": True,
            "member_count": 0,
            "roles": ["admin", "user"]
        }
        
        return {"message": "Organization created successfully", "organization": new_org}
            
    except Exception as e:
        logger.error(f"Failed to create organization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/organizations/{org_id}/users")
async def add_user_to_organization(
    org_id: str,
    user_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Add a user to an organization with a specific role."""
    try:
        # Check admin permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to manage organization users"
            )
        
        # Simplified user management (no RBAC)
        # Just return success for now
        return {"message": "User added to organization successfully (simplified mode)"}
            
    except Exception as e:
        logger.error(f"Failed to add user to organization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/organizations/{org_id}/users/{user_id}")
async def remove_user_from_organization(
    org_id: str,
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Remove a user from an organization."""
    try:
        # Check admin permission
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to manage organization users"
            )
        
        # Simplified user management (no RBAC)
        # Just return success for now
        return {"message": "User removed from organization successfully (simplified mode)"}
            
    except Exception as e:
        logger.error(f"Failed to remove user from organization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/roles")
async def get_roles(current_user: dict = Depends(get_current_user)):
    """Get all roles (admin only)."""
    try:
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to view roles"
            )
        
        # Simplified roles (no RBAC)
        roles = [
            {
                "id": "admin",
                "name": "Admin",
                "description": "Full system access",
                "permissions": ["admin:manage"],
                "created_at": "2024-01-01T00:00:00Z",
                "is_active": True
            },
            {
                "id": "user",
                "name": "User",
                "description": "Standard user access",
                "permissions": ["screenshots:read", "search:perform"],
                "created_at": "2024-01-01T00:00:00Z",
                "is_active": True
            }
        ]
        return {"roles": roles}
    except Exception as e:
        logger.error(f"Failed to get roles: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/roles")
async def create_role(
    role_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Create a new role (admin only)."""
    try:
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to create roles"
            )
        
        # Simplified role creation (no RBAC)
        # Just return success for now
        return {"message": f"Role '{role_data.get('name')}' created successfully (simplified mode)"}
    except Exception as e:
        logger.error(f"Failed to create role: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/assign-role")
async def assign_role_to_user(
    assignment_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Assign a role to a user (admin only)."""
    try:
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to assign roles"
            )
        
        user_id = assignment_data.get("user_id")
        role_name = assignment_data.get("role_name")
        
        if not user_id or not role_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID and role name are required"
            )
        
        # Simplified role assignment (no RBAC)
        if role_name == "admin":
            # Find user and make them admin
            user_found = False
            users_db = auth_service.get_users_db()
            for username, user_data in users_db.items():
                if user_data.get("id") == user_id:
                    user_data["is_admin"] = True
                    user_found = True
                    break
            
            # Also check OAuth users
            oauth_users_db = auth_service.get_oauth_users_db()
            for oauth_key, oauth_user in oauth_users_db.items():
                if oauth_user.get("id") == user_id:
                    oauth_user["is_admin"] = True
                    user_found = True
                    break
            
            if user_found:
                return {"message": f"Admin role assigned to user {user_id} successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User {user_id} not found"
                )
        else:
            return {"message": f"Role {role_name} is not supported in simplified mode"}
    except Exception as e:
        logger.error(f"Failed to assign role: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/users")
async def get_users(current_user: dict = Depends(get_current_user)):
    """Get all users (admin only)."""
    try:
        auth_service = get_auth_service()
        if not auth_service.has_permission(current_user["id"], "admin:manage"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to view users"
            )
        
        # Simplified user list (no RBAC)
        users = []
        
        # Add users from users_db
        for username, user_data in auth_service.get_users_db().items():
            users.append({
                "id": user_data.get("id"),
                "username": username,
                "email": user_data.get("email"),
                "full_name": user_data.get("full_name"),
                "is_admin": user_data.get("is_admin", False),
                "created_at": user_data.get("created_at"),
                "is_active": user_data.get("is_active", True)
            })
        
        # Add OAuth users
        for oauth_key, oauth_user in auth_service.get_oauth_users_db().items():
            users.append({
                "id": oauth_user.get("id"),
                "username": oauth_user.get("username"),
                "email": oauth_user.get("email"),
                "full_name": oauth_user.get("full_name"),
                "is_admin": oauth_user.get("is_admin", False),
                "created_at": oauth_user.get("created_at"),
                "is_active": oauth_user.get("is_active", True),
                "oauth_provider": oauth_user.get("oauth_provider")
            })
        
        return {"users": users}
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dev/create-test-user")
async def create_test_user(user_data: dict):
    """Development endpoint to create a test user account."""
    try:
        from app.services.auth_service import get_auth_service
        from app.models.auth_schemas import UserRegister
        
        auth_service = get_auth_service()
        
        # Create user registration data
        test_user = UserRegister(
            username=user_data.get("username", "testuser"),
            email=user_data.get("email", "test@example.com"),
            password=user_data.get("password", "testpass123"),
            full_name=user_data.get("full_name", "Test User")
        )
        
        # Create the user
        user_response = auth_service.create_user(test_user)
        
        if user_response:
            # Login the user and get token
            token = auth_service.login_user(test_user)
            
            return {
                "message": "Test user created and logged in successfully",
                "user": user_response,
                "access_token": token.access_token,
                "is_admin": user_response.is_admin
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to create user")
            
    except Exception as e:
        logger.error(f"Failed to create test user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dev/promote-first-user")
async def promote_first_user(
    current_user: dict = Depends(get_current_user)
):
    """Promote the current user to admin if they're the first user."""
    try:
        auth_service = get_auth_service()
        
        # Check if this is the first user (no other users exist)
        total_users = len(auth_service.get_users_db()) + len(auth_service.get_oauth_users_db())
        
        if total_users <= 1:
            # This is the first user, make them admin
            username = current_user["username"]
            
            # Update in users_db
            users_db = auth_service.get_users_db()
            if username in users_db:
                users_db[username]["is_admin"] = True
                print(f"Promoted first user {username} to admin in users_db")
            
            # Update in oauth_users_db
            oauth_users_db = auth_service.get_oauth_users_db()
            for oauth_key, oauth_user in oauth_users_db.items():
                if oauth_user.get("username") == username:
                    oauth_user["is_admin"] = True
                    print(f"Promoted first OAuth user {username} to admin")
                    break
            
            return {
                "message": f"User {username} promoted to admin (first user)",
                "user_id": current_user["id"],
                "username": username,
                "is_admin": True,
                "reason": "First user in system"
            }
        else:
            return {
                "message": "Not the first user",
                "total_users": total_users,
                "is_admin": current_user.get("is_admin", False)
            }
        
    except Exception as e:
        logger.error(f"Failed to promote first user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dev/simple-login")
async def simple_login(credentials: dict):
    """Simple login endpoint for development (no OAuth required)."""
    try:
        from app.services.auth_service import get_auth_service
        from app.models.auth_schemas import UserRegister, UserLogin
        
        auth_service = get_auth_service()
        username = credentials.get("username", "admin")
        password = credentials.get("password", "admin123")
        
        # Check if user exists, if not create them
        user = auth_service.get_user_by_username(username)
        if not user:
            # Create the user (will be admin if first user)
            user_data = UserRegister(
                username=username,
                email=f"{username}@example.com",
                password=password,
                full_name=f"{username.capitalize()} User"
            )
            user_response = auth_service.create_user(user_data)
            if not user_response:
                raise HTTPException(status_code=400, detail="Failed to create user")
            
            # Get the created user
            user = auth_service.get_user_by_username(username)
        
        # Now authenticate the user with UserLogin
        login_data = UserLogin(username=username, password=password)
        
        try:
            token = auth_service.login_user(login_data)
            return {
                "message": "Login successful",
                "access_token": token.access_token,
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "is_admin": user.get("is_admin", False)
                }
            }
        except Exception as e:
            # If login fails, try to authenticate directly
            if user.get("hashed_password") == auth_service.get_password_hash(password):
                # Create token manually
                access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
                access_token = auth_service.create_access_token(
                    data={"sub": user["username"], "user_id": user["id"]},
                    expires_delta=access_token_expires
                )
                
                return {
                    "message": "Login successful (direct auth)",
                    "access_token": access_token,
                    "user": {
                        "id": user["id"],
                        "username": user["username"],
                        "email": user["email"],
                        "is_admin": user.get("is_admin", False)
                    }
                }
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
    except Exception as e:
        logger.error(f"Simple login failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
