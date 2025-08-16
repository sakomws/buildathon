#!/usr/bin/env python3
"""
Generate Test Dataset for Visual Memory Search
Creates sample screenshots with various content types for testing
"""

import os
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random

def create_error_screenshot():
    """Create a screenshot showing an error message."""
    # Create image
    img = Image.new('RGB', (800, 600), color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font, fallback to default
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 800, 60], fill='#dc3545')
    draw.text((20, 20), "❌ Authentication Error", fill='white', font=font_large)
    
    # Error content
    draw.text((50, 100), "Error Code: 401 Unauthorized", fill='#dc3545', font=font_medium)
    draw.text((50, 140), "Your session has expired. Please log in again.", fill='#6c757d', font=font_medium)
    
    # Error details
    draw.text((50, 200), "Details:", fill='#495057', font=font_medium)
    draw.text((70, 230), "• Invalid or expired access token", fill='#6c757d', font=font_small)
    draw.text((70, 250), "• Session timeout after 30 minutes", fill='#6c757d', font=font_small)
    draw.text((70, 270), "• Please refresh the page and try again", fill='#6c757d', font=font_small)
    
    # Buttons
    draw.rectangle([50, 350, 200, 390], fill='#007bff', outline='#0056b3')
    draw.text((80, 360), "Login Again", fill='white', font=font_medium)
    
    draw.rectangle([220, 350, 320, 390], fill='#6c757d', outline='#545b62')
    draw.text((240, 360), "Cancel", fill='white', font=font_medium)
    
    return img

def create_login_form():
    """Create a screenshot showing a login form."""
    img = Image.new('RGB', (600, 700), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 28)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 600, 80], fill='#007bff')
    draw.text((200, 25), "🔐 Login", fill='white', font=font_large)
    
    # Form container
    draw.rectangle([50, 120, 550, 650], fill='#f8f9fa', outline='#dee2e6')
    
    # Username field
    draw.text((80, 150), "Username:", fill='#495057', font=font_medium)
    draw.rectangle([80, 180, 520, 210], fill='white', outline='#ced4da')
    draw.text((90, 190), "john.doe@example.com", fill='#6c757d', font=font_small)
    
    # Password field
    draw.text((80, 240), "Password:", fill='#495057', font=font_medium)
    draw.rectangle([80, 270, 520, 300], fill='white', outline='#ced4da')
    draw.text((90, 285), "••••••••", fill='#6c757d', font=font_small)
    
    # Remember me checkbox
    draw.rectangle([80, 330, 100, 350], fill='white', outline='#ced4da')
    draw.text((110, 330), "Remember me", fill='#495057', font=font_small)
    
    # Login button
    draw.rectangle([80, 400, 520, 440], fill='#28a745', outline='#1e7e34')
    draw.text((250, 410), "Sign In", fill='white', font=font_large)
    
    # Links
    draw.text((80, 480), "Forgot password?", fill='#007bff', font=font_small)
    draw.text((80, 510), "Don't have an account? Sign up", fill='#007bff', font=font_small)
    
    return img

def create_dashboard():
    """Create a screenshot showing a dashboard with charts."""
    img = Image.new('RGB', (1200, 800), color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 1200, 70], fill='#343a40')
    draw.text((30, 20), "📊 Analytics Dashboard", fill='white', font=font_large)
    draw.text((1000, 20), "👤 John Doe", fill='white', font=font_medium)
    
    # Sidebar
    draw.rectangle([0, 70, 250, 800], fill='#495057')
    menu_items = ["📈 Overview", "📊 Reports", "👥 Users", "⚙️ Settings", "❓ Help"]
    for i, item in enumerate(menu_items):
        y_pos = 100 + i * 50
        draw.text((20, y_pos), item, fill='white', font=font_medium)
    
    # Main content area
    # Stats cards
    stats = [("Total Users", "1,234", "#28a745"), ("Revenue", "$45,678", "#007bff"), ("Growth", "+12.5%", "#ffc107")]
    for i, (label, value, color) in enumerate(stats):
        x = 280 + i * 280
        draw.rectangle([x, 100, x + 250, 180], fill='white', outline='#dee2e6')
        draw.text((x + 20, 120), label, fill='#6c757d', font=font_small)
        draw.text((x + 20, 140), value, fill=color, font=font_large)
    
    # Chart area
    draw.rectangle([280, 200, 1000, 400], fill='white', outline='#dee2e6')
    draw.text((300, 220), "📈 Monthly Revenue Trend", fill='#495057', font=font_medium)
    
    # Simple bar chart
    chart_data = [30, 45, 60, 75, 90, 85, 95]
    bar_width = 80
    for i, height in enumerate(chart_data):
        x = 320 + i * 90
        y = 380 - height
        draw.rectangle([x, y, x + bar_width, 380], fill='#007bff')
        draw.text((x + 30, 390), f"${height}K", fill='#6c757d', font=font_small)
    
    # Recent activity
    draw.rectangle([280, 420, 1000, 600], fill='white', outline='#dee2e6')
    draw.text((300, 440), "🕒 Recent Activity", fill='#495057', font=font_medium)
    
    activities = [
        "New user registration: jane.smith@example.com",
        "Payment received: $299.99 from Premium Plan",
        "System backup completed successfully",
        "New report generated: Q4 Analytics"
    ]
    
    for i, activity in enumerate(activities):
        y_pos = 470 + i * 30
        draw.text((320, y_pos), activity, fill='#6c757d', font=font_small)
    
    return img

def create_mobile_app():
    """Create a screenshot showing a mobile app interface."""
    img = Image.new('RGB', (375, 812), color='#ffffff')  # iPhone dimensions
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Status bar
    draw.rectangle([0, 0, 375, 44], fill='#000000')
    draw.text((20, 12), "9:41", fill='white', font=font_small)
    draw.text((300, 12), "📶 📶 🔋", fill='white', font=font_small)
    
    # Header
    draw.rectangle([0, 44, 375, 100], fill='#007bff')
    draw.text((20, 60), "📱 MyApp", fill='white', font=font_large)
    draw.text((300, 60), "🔍", fill='white', font=font_large)
    
    # Search bar
    draw.rectangle([20, 120, 355, 150], fill='#f8f9fa', outline='#dee2e6')
    draw.text((35, 130), "🔍 Search for anything...", fill='#6c757d', font=font_small)
    
    # Menu items
    menu_items = ["🏠 Home", "📱 Profile", "⚙️ Settings", "💬 Messages", "📊 Stats"]
    for i, item in enumerate(menu_items):
        y_pos = 170 + i * 60
        draw.rectangle([20, y_pos, 355, y_pos + 50], fill='white', outline='#dee2e6')
        draw.text((40, y_pos + 15), item, fill='#495057', font=font_medium)
        draw.text((320, y_pos + 15), ">", fill='#6c757d', font=font_medium)
    
    # Bottom navigation
    draw.rectangle([0, 750, 375, 812], fill='#f8f9fa', outline='#dee2e6')
    nav_items = ["🏠", "🔍", "➕", "💬", "👤"]
    for i, item in enumerate(nav_items):
        x = 37 + i * 75
        draw.text((x, 770), item, fill='#6c757d', font=font_large)
    
    return img


def create_404_page():
    """Create a screenshot showing a 404 error page."""
    img = Image.new('RGB', (800, 600), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Large 404 text
    draw.text((250, 150), "404", fill='#dc3545', font=font_large)
    
    # Error message
    draw.text((200, 250), "Page Not Found", fill='#6c757d', font=font_medium)
    draw.text((150, 290), "The page you're looking for doesn't exist.", fill='#6c757d', font=font_small)
    
    # Illustration (simple shapes)
    draw.ellipse([350, 350, 450, 450], fill='#f8f9fa', outline='#dee2e6')
    draw.text((380, 400), "😕", fill='#6c757d', font=font_large)
    
    # Navigation options
    draw.text((200, 500), "Try these instead:", fill='#495057', font=font_small)
    
    links = ["🏠 Home", "🔍 Search", "📚 Help", "📞 Contact"]
    for i, link in enumerate(links):
        x = 200 + i * 120
        draw.text((x, 530), link, fill='#007bff', font=font_small)
    
    return img

def create_user_profile():
    """Create a screenshot showing a user profile page."""
    img = Image.new('RGB', (800, 700), color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 800, 100], fill='#007bff')
    draw.text((30, 30), "👤 User Profile", fill='white', font=font_large)
    draw.text((700, 30), "✏️", fill='white', font=font_large)
    
    # Profile picture area
    draw.ellipse([50, 120, 150, 220], fill='#6c757d')
    draw.text((85, 160), "👤", fill='white', font=font_large)
    
    # Profile info
    draw.text((180, 130), "John Doe", fill='#495057', font=font_large)
    draw.text((180, 160), "john.doe@example.com", fill='#6c757d', font=font_medium)
    draw.text((180, 185), "Software Developer", fill='#6c757d', font=font_medium)
    draw.text((180, 210), "📍 San Francisco, CA", fill='#6c757d', font=font_small)
    
    # Stats
    stats = [("Posts", "42"), ("Followers", "1,234"), ("Following", "567")]
    for i, (label, value) in enumerate(stats):
        x = 50 + i * 200
        draw.rectangle([x, 250, x + 150, 300], fill='white', outline='#dee2e6')
        draw.text((x + 20, 260), label, fill='#6c757d', font=font_small)
        draw.text((x + 20, 280), value, fill='#007bff', font=font_medium)
    
    # Bio section
    draw.rectangle([50, 320, 750, 400], fill='white', outline='#dee2e6')
    draw.text((70, 340), "📝 About Me", fill='#495057', font=font_medium)
    draw.text((70, 370), "Passionate software developer with 5+ years of experience", fill='#6c757d', font=font_small)
    draw.text((70, 390), "in web development, AI, and cloud technologies.", fill='#6c757d', font=font_small)
    
    # Skills
    draw.rectangle([50, 420, 750, 500], fill='white', outline='#dee2e6')
    draw.text((70, 440), "🛠️ Skills", fill='#495057', font=font_medium)
    
    skills = ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker"]
    for i, skill in enumerate(skills):
        x = 70 + i * 100
        draw.rectangle([x, 470, x + 80, 490], fill='#e9ecef', outline='#dee2e6')
        draw.text((x + 10, 475), skill, fill='#495057', font=font_small)
    
    # Recent activity
    draw.rectangle([50, 520, 750, 650], fill='white', outline='#dee2e6')
    draw.text((70, 540), "🕒 Recent Activity", fill='#495057', font=font_medium)
    
    activities = [
        "📝 Published new blog post: 'AI in Web Development'",
        "💬 Commented on Sarah's post about React hooks",
        "⭐ Liked Mike's tutorial on Docker containers",
        "🔄 Updated profile information"
    ]
    
    for i, activity in enumerate(activities):
        y_pos = 570 + i * 25
        draw.text((70, y_pos), activity, fill='#6c757d', font=font_small)
    
    return img

def create_ecommerce_product():
    """Create a screenshot showing an e-commerce product page."""
    img = Image.new('RGB', (1000, 800), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 1000, 80], fill='#2c3e50')
    draw.text((30, 25), "🛒 ShopStore", fill='white', font=font_large)
    draw.text((800, 25), "🔍", fill='white', font=font_medium)
    draw.text((850, 25), "🛒", fill='white', font=font_medium)
    draw.text((900, 25), "👤", fill='white', font=font_medium)
    
    # Product image placeholder
    draw.rectangle([50, 120, 450, 520], fill='#ecf0f1', outline='#bdc3c7')
    draw.text((200, 300), "📱 Product Image", fill='#7f8c8d', font=font_large)
    
    # Product info
    draw.text((500, 120), "iPhone 15 Pro Max", fill='#2c3e50', font=font_large)
    draw.text((500, 160), "Latest smartphone with advanced features", fill='#7f8c8d', font=font_medium)
    
    # Price
    draw.text((500, 220), "$1,199.99", fill='#e74c3c', font=font_large)
    draw.text((500, 250), "Free shipping • In stock", fill='#27ae60', font=font_small)
    
    # Add to cart button
    draw.rectangle([500, 300, 700, 350], fill='#e74c3c', outline='#c0392b')
    draw.text((580, 310), "Add to Cart", fill='white', font=font_medium)
    
    # Buy now button
    draw.rectangle([500, 370, 700, 420], fill='#f39c12', outline='#e67e22')
    draw.text((590, 380), "Buy Now", fill='white', font=font_medium)
    
    # Product details
    draw.text((500, 450), "Specifications:", fill='#2c3e50', font=font_medium)
    specs = ["• 6.7-inch Super Retina XDR display", "• A17 Pro chip", "• 48MP camera system", "• 5G capable"]
    for i, spec in enumerate(specs):
        draw.text((520, 480 + i * 25), spec, fill='#7f8c8d', font=font_small)
    
    # Reviews
    draw.rectangle([50, 550, 950, 750], fill='#f8f9fa', outline='#dee2e6')
    draw.text((70, 570), "⭐ Customer Reviews", fill='#2c3e50', font=font_medium)
    
    reviews = [
        "Amazing phone! Best iPhone ever! - John D.",
        "Great camera quality and performance - Sarah M.",
        "Worth every penny - Mike R."
    ]
    
    for i, review in enumerate(reviews):
        draw.text((70, 600 + i * 30), review, fill='#7f8c8d', font=font_small)
    
    return img

def create_social_media_feed():
    """Create a screenshot showing a social media news feed."""
    img = Image.new('RGB', (800, 1000), color='#f0f2f5')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 800, 70], fill='#1877f2')
    draw.text((30, 20), "📘 SocialBook", fill='white', font=font_large)
    draw.text((700, 20), "🔍", fill='white', font=font_medium)
    
    # Search bar
    draw.rectangle([30, 90, 770, 120], fill='white', outline='#e4e6eb')
    draw.text((50, 100), "🔍 What's on your mind?", fill='#65676b', font=font_small)
    
    # Post 1
    draw.rectangle([30, 140, 770, 300], fill='white', outline='#e4e6eb')
    draw.ellipse([50, 160, 80, 190], fill='#1877f2')
    draw.text((60, 165), "👤", fill='white', font=font_small)
    draw.text((100, 160), "Alice Johnson", fill='#1877f2', font=font_medium)
    draw.text((100, 180), "2 hours ago", fill='#65676b', font=font_small)
    draw.text((50, 210), "Just finished my morning workout! 💪 Feeling energized for the day ahead.", fill='#1c1e21', font=font_small)
    
    # Post actions
    draw.text((50, 250), "👍 24 💬 8 🔄 3", fill='#65676b', font=font_small)
    
    # Post 2
    draw.rectangle([30, 320, 770, 480], fill='white', outline='#e4e6eb')
    draw.ellipse([50, 340, 80, 370], fill='#42a5f5')
    draw.text((60, 345), "👤", fill='white', font=font_small)
    draw.text((100, 340), "Bob Smith", fill='#1877f2', font=font_medium)
    draw.text((100, 360), "5 hours ago", fill='#65676b', font=font_small)
    draw.text((50, 390), "Amazing sunset at the beach today! 🌅", fill='#1c1e21', font=font_small)
    
    # Post actions
    draw.text((50, 430), "👍 156 💬 23 🔄 12", fill='#65676b', font=font_small)
    
    # Post 3
    draw.rectangle([30, 500, 770, 660], fill='white', outline='#e4e6eb')
    draw.ellipse([50, 520, 80, 550], fill='#66bb6a')
    draw.text((60, 525), "👤", fill='white', font=font_small)
    draw.text((100, 520), "Carol Davis", fill='#1877f2', font=font_medium)
    draw.text((100, 540), "1 day ago", fill='#65676b', font=font_small)
    draw.text((50, 570), "New recipe for chocolate chip cookies! 🍪", fill='#1c1e21', font=font_small)
    
    # Post actions
    draw.text((50, 610), "👍 89 💬 15 🔄 7", fill='#65676b', font=font_small)
    
    # Bottom navigation
    draw.rectangle([0, 930, 800, 1000], fill='white', outline='#e4e6eb')
    nav_items = ["🏠", "🔍", "➕", "💬", "👤"]
    for i, item in enumerate(nav_items):
        x = 80 + i * 140
        draw.text((x, 950), item, fill='#65676b', font=font_large)
    
    return img

def create_gaming_interface():
    """Create a screenshot showing a gaming interface."""
    img = Image.new('RGB', (1200, 800), color='#1a1a1a')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Game title
    draw.text((500, 30), "🎮 SPACE WARRIORS", fill='#00ff88', font=font_large)
    
    # Health bar
    draw.rectangle([50, 80, 300, 100], fill='#2d2d2d', outline='#00ff88')
    draw.rectangle([50, 80, 250, 100], fill='#e74c3c')
    draw.text((320, 80), "HP: 75/100", fill='#00ff88', font=font_small)
    
    # Energy bar
    draw.rectangle([50, 110, 300, 130], fill='#2d2d2d', outline='#00ff88')
    draw.rectangle([50, 110, 200, 130], fill='#3498db')
    draw.text((320, 110), "Energy: 50/100", fill='#00ff88', font=font_small)
    
    # Score
    draw.text((50, 150), "Score: 15,420", fill='#f39c12', font=font_medium)
    draw.text((50, 180), "Level: 8", fill='#f39c12', font=font_medium)
    
    # Game area
    draw.rectangle([400, 80, 1100, 600], fill='#000033', outline='#00ff88')
    draw.text((700, 300), "🎯 GAME AREA", fill='#00ff88', font=font_large)
    
    # Mini-map
    draw.rectangle([50, 250, 300, 400], fill='#2d2d2d', outline='#00ff88')
    draw.text((150, 270), "🗺️ Mini-Map", fill='#00ff88', font=font_medium)
    
    # Player position
    draw.ellipse([170, 320, 180, 330], fill='#00ff88')
    draw.text((190, 320), "You", fill='#00ff88', font=font_small)
    
    # Enemies
    draw.ellipse([200, 350, 210, 360], fill='#e74c3c')
    draw.ellipse([220, 370, 230, 380], fill='#e74c3c')
    draw.ellipse([180, 390, 190, 400], fill='#e74c3c')
    
    # Controls
    draw.rectangle([50, 450, 300, 600], fill='#2d2d2d', outline='#00ff88')
    draw.text((150, 470), "🎮 Controls", fill='#00ff88', font=font_medium)
    
    controls = ["WASD - Move", "Space - Jump", "Shift - Run", "E - Interact", "Q - Special"]
    for i, control in enumerate(controls):
        draw.text((70, 500 + i * 25), control, fill='#ffffff', font=font_small)
    
    # Inventory
    draw.rectangle([50, 620, 300, 750], fill='#2d2d2d', outline='#00ff88')
    draw.text((150, 640), "🎒 Inventory", fill='#00ff88', font=font_medium)
    
    items = ["⚔️ Sword", "🛡️ Shield", "🧪 Health Potion", "💎 Gem"]
    for i, item in enumerate(items):
        draw.text((70, 670 + i * 25), item, fill='#ffffff', font=font_small)
    
    # Chat
    draw.rectangle([1100, 80, 1200, 600], fill='#2d2d2d', outline='#00ff88')
    draw.text((1120, 100), "💬 Chat", fill='#00ff88', font=font_small)
    
    messages = ["Player1: GG!", "Player2: Nice shot!", "Player3: Team up?"]
    for i, msg in enumerate(messages):
        draw.text((1120, 130 + i * 20), msg, fill='#ffffff', font=font_small)
    
    return img

def create_email_client():
    """Create a screenshot showing an email client interface."""
    img = Image.new('RGB', (1000, 700), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 1000, 60], fill='#4285f4')
    draw.text((30, 20), "📧 MailApp", fill='white', font=font_large)
    draw.text((900, 20), "🔍", fill='white', font=font_medium)
    draw.text((930, 20), "⚙️", fill='white', font=font_medium)
    
    # Sidebar
    draw.rectangle([0, 60, 200, 700], fill='#f8f9fa', outline='#dee2e6')
    
    # Compose button
    draw.rectangle([20, 80, 180, 110], fill='#34a853', outline='#2d8f47')
    draw.text((70, 85), "✏️ Compose", fill='white', font=font_medium)
    
    # Folders
    folders = ["📥 Inbox (12)", "📤 Sent", "📁 Drafts", "🗑️ Trash", "📌 Important", "🏷️ Labels"]
    for i, folder in enumerate(folders):
        y_pos = 130 + i * 40
        draw.text((20, y_pos), folder, fill='#5f6368', font=font_medium)
    
    # Main content area
    # Search bar
    draw.rectangle([220, 80, 980, 110], fill='#f8f9fa', outline='#dee2e6')
    draw.text((240, 90), "🔍 Search emails...", fill='#9aa0a6', font=font_small)
    
    # Email list
    emails = [
        ("John Smith", "Project Update - Q4 Results", "2 hours ago", "📎"),
        ("Sarah Johnson", "Meeting Tomorrow at 10 AM", "4 hours ago", ""),
        ("Mike Davis", "Weekly Report", "1 day ago", "📎"),
        ("Lisa Wilson", "Client Feedback", "2 days ago", ""),
        ("Tom Brown", "New Feature Request", "3 days ago", "📎")
    ]
    
    for i, (sender, subject, time, attachment) in enumerate(emails):
        y_pos = 130 + i * 80
        
        # Email row
        if i == 0:  # Selected email
            draw.rectangle([220, y_pos, 980, y_pos + 70], fill='#e8f0fe', outline='#4285f4')
        else:
            draw.rectangle([220, y_pos, 980, y_pos + 70], fill='white', outline='#dee2e6')
        
        # Sender
        draw.text((240, y_pos + 10), sender, fill='#202124', font=font_medium)
        
        # Subject
        draw.text((240, y_pos + 30), subject, fill='#5f6368', font=font_small)
        
        # Time
        draw.text((800, y_pos + 10), time, fill='#9aa0a6', font=font_small)
        
        # Attachment
        if attachment:
            draw.text((900, y_pos + 10), attachment, fill='#9aa0a6', font=font_small)
    
    # Email content (for selected email)
    draw.rectangle([220, 450, 980, 650], fill='white', outline='#dee2e6')
    draw.text((240, 470), "From: John Smith <john.smith@company.com>", fill='#5f6368', font=font_small)
    draw.text((240, 490), "To: me@company.com", fill='#5f6368', font=font_small)
    draw.text((240, 510), "Subject: Project Update - Q4 Results", fill='#202124', font=font_medium)
    draw.text((240, 540), "Hi team,", fill='#202124', font=font_small)
    draw.text((240, 560), "Here's the Q4 project update. We've made significant progress...", fill='#202124', font=font_small)
    
    # Action buttons
    draw.rectangle([240, 600, 320, 630], fill='#4285f4', outline='#3367d6')
    draw.text((260, 605), "Reply", fill='white', font=font_small)
    
    draw.rectangle([340, 600, 420, 630], fill='#ea4335', outline='#d93025')
    draw.text((360, 605), "Delete", fill='white', font=font_small)
    
    draw.rectangle([440, 600, 520, 630], fill='#34a853', outline='#2d8f47')
    draw.text((460, 605), "Forward", fill='white', font=font_small)
    
    return img

def create_weather_app():
    """Create a screenshot showing a weather app interface."""
    img = Image.new('RGB', (400, 800), color='#87ceeb')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, 400, 100], fill='#4a90e2')
    draw.text((30, 30), "🌤️ WeatherApp", fill='white', font=font_large)
    draw.text((300, 30), "📍", fill='white', font=font_medium)
    draw.text((330, 30), "🔍", fill='white', font=font_medium)
    
    # Current weather
    draw.rectangle([20, 120, 380, 300], fill='white', outline='#e0e0e0')
    draw.text((180, 140), "San Francisco", fill='#333333', font=font_medium)
    draw.text((180, 170), "☀️", fill='#f39c12', font=font_large)
    draw.text((150, 200), "72°F", fill='#333333', font=font_large)
    draw.text((160, 230), "Sunny", fill='#666666', font=font_medium)
    draw.text((140, 260), "Feels like 75°F", fill='#999999', font=font_small)
    
    # Hourly forecast
    draw.rectangle([20, 320, 380, 420], fill='white', outline='#e0e0e0')
    draw.text((30, 340), "Hourly Forecast", fill='#333333', font=font_medium)
    
    hours = ["Now", "1PM", "2PM", "3PM", "4PM", "5PM"]
    temps = ["72°", "74°", "76°", "78°", "77°", "75°"]
    icons = ["☀️", "☀️", "⛅", "⛅", "☀️", "☀️"]
    
    for i, (hour, temp, icon) in enumerate(zip(hours, temps, icons)):
        x = 30 + i * 55
        draw.text((x, 370), hour, fill='#666666', font=font_small)
        draw.text((x, 390), icon, fill='#f39c12', font=font_small)
        draw.text((x, 410), temp, fill='#333333', font=font_small)
    
    # Daily forecast
    draw.rectangle([20, 440, 380, 600], fill='white', outline='#e0e0e0')
    draw.text((30, 460), "7-Day Forecast", fill='#333333', font=font_medium)
    
    days = ["Today", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    high_temps = ["72°", "75°", "78°", "80°", "77°", "74°", "71°"]
    low_temps = ["58°", "60°", "63°", "65°", "62°", "59°", "57°"]
    day_icons = ["☀️", "⛅", "🌤️", "☀️", "🌤️", "⛅", "☀️"]
    
    for i, (day, high, low, icon) in enumerate(zip(days, high_temps, low_temps, day_icons)):
        y_pos = 490 + i * 15
        draw.text((30, y_pos), day, fill='#333333', font=font_small)
        draw.text((120, y_pos), icon, fill='#f39c12', font=font_small)
        draw.text((300, y_pos), f"{high}/{low}", fill='#666666', font=font_small)
    
    # Weather details
    draw.rectangle([20, 620, 380, 750], fill='white', outline='#e0e0e0')
    draw.text((30, 640), "Weather Details", fill='#333333', font=font_medium)
    
    details = [
        ("💨 Wind", "12 mph"),
        ("💧 Humidity", "45%"),
        ("👁️ Visibility", "10 mi"),
        ("🌅 Sunrise", "6:45 AM"),
        ("🌇 Sunset", "7:30 PM")
    ]
    
    for i, (label, value) in enumerate(details):
        y_pos = 670 + i * 15
        draw.text((50, y_pos), label, fill='#666666', font=font_small)
        draw.text((250, y_pos), value, fill='#333333', font=font_small)
    
    return img

def generate_all_screenshots():
    """Generate all test screenshots and return count of successful generations."""
    try:
        # Create test_screenshots directory if it doesn't exist
        os.makedirs("test_screenshots", exist_ok=True)
        
        # Define all screenshots to generate
        screenshots = [
            ("error_auth.png", create_error_screenshot, "Authentication error page"),
            ("login_form.png", create_login_form, "Login form"),
            ("dashboard_charts.png", create_dashboard, "Dashboard with charts"),
            ("mobile_app.png", create_mobile_app, "Mobile app interface"),
            ("404_page.png", create_404_page, "404 error page"),
            ("user_profile.png", create_user_profile, "User profile page"),
            ("ecommerce_product.png", create_ecommerce_product, "E-commerce product page"),
            ("social_media_feed.png", create_social_media_feed, "Social media news feed"),
            ("gaming_interface.png", create_gaming_interface, "Gaming interface"),
            ("email_client.png", create_email_client, "Email client interface"),
            ("weather_app.png", create_weather_app, "Weather app interface")
        ]
        
        print("🎨 Generating test dataset...")
        print(f"📁 Output directory: {os.path.abspath('test_screenshots')}")
        print()
        
        success_count = 0
        for filename, create_func, description in screenshots:
            try:
                print(f"🖼️  Creating {filename}...")
                img = create_func()
                filepath = os.path.join("test_screenshots", filename)
                img.save(filepath, "PNG")
                print(f"   ✅ Saved: {description}")
                success_count += 1
            except Exception as e:
                print(f"   ❌ Error creating {filename}: {e}")
        
        print()
        print("🎉 Test dataset generation complete!")
        print(f"📊 Total screenshots generated: {success_count}")
        
        return success_count
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return 0

def main():
    """Generate all test screenshots."""
    success_count = generate_all_screenshots()
    
    if success_count > 0:
        print()
        print("🧪 Test queries you can try:")
        print("   • 'blue button' - Find images with blue buttons")
        print("   • 'login form' - Find authentication interfaces")
        print("   • 'chart' - Find dashboard charts")
        print("   • 'mobile app' - Find mobile interfaces")
        print("   • 'dark theme' - Find dark themed interfaces")
        print("   • 'error page' - Find error pages")
        print("   • 'user profile' - Find profile interfaces")
        print("   • 'shopping cart' - Find e-commerce elements")
        print("   • 'social media' - Find social interfaces")
        print("   • 'gaming' - Find game interfaces")
        print("   • 'email' - Find email interfaces")
        print("   • 'weather' - Find weather app elements")
        print()
        print("🚀 Run the search to test:")
        print("   python main.py test_screenshots --query 'your search term'")
    else:
        print("❌ No screenshots were generated successfully")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Generation interrupted by user")
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
        print("💡 Make sure you have Pillow installed: pip install Pillow") 