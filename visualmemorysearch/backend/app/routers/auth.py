"""Authentication routes for the API."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from app.services.auth_service import get_auth_service
from app.services.recaptcha_service import get_recaptcha_service
from app.models.auth_schemas import UserLogin, UserRegister, UserResponse, Token, OAuthLogin
from app.core.auth import get_current_active_user
import os
# RBAC service removed - using simple admin flags
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - Visual Memory Search</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { text-align: center; color: #333; margin-bottom: 30px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; color: #555; }
            input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #0056b3; }
            .oauth-buttons { margin-top: 20px; text-align: center; }
            .oauth-btn { display: inline-block; margin: 5px; padding: 10px 20px; text-decoration: none; border-radius: 5px; color: white; }
            .google-btn { background: #db4437; }
            .github-btn { background: #333; }
            .register-link { text-align: center; margin-top: 20px; }
            .error { color: red; margin-top: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Visual Memory Search</h1>
            <form id="loginForm">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit">Login</button>
                <div id="error" class="error"></div>
            </form>
            
            <div class="oauth-buttons">
                <a href="/auth/google" class="oauth-btn google-btn">Sign in with Google</a>
                <a href="/auth/github" class="oauth-btn github-btn">Sign in with GitHub</a>
            </div>
            
            <div class="register-link">
                <a href="/auth/register">Don't have an account? Register</a>
            </div>
        </div>
        
        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                try {
                    const response = await fetch('/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        localStorage.setItem('access_token', data.access_token);
                        window.location.href = '/';
                    } else {
                        const error = await response.json();
                        document.getElementById('error').textContent = error.detail || 'Login failed';
                    }
                } catch (error) {
                    document.getElementById('error').textContent = 'Network error';
                }
            });
        </script>
    </body>
    </html>
    """

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register - Visual Memory Search</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { text-align: center; color: #333; margin-bottom: 30px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; color: #555; }
            input[type="text"], input[type="email"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #218838; }
            .login-link { text-align: center; margin-top: 20px; }
            .error { color: red; margin-top: 10px; text-align: center; }
            .success { color: green; margin-top: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Create Account</h1>
            <form id="registerForm">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="full_name">Full Name:</label>
                    <input type="text" id="full_name" name="full_name">
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit">Register</button>
                <div id="error" class="error"></div>
                <div id="success" class="success"></div>
            </form>
            
            <div class="login-link">
                <a href="/auth/login">Already have an account? Login</a>
            </div>
        </div>
        
        <script>
            document.getElementById('registerForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const username = document.getElementById('username').value;
                const email = document.getElementById('email').value;
                const full_name = document.getElementById('full_name').value;
                const password = document.getElementById('password').value;
                
                try {
                    const response = await fetch('/auth/register', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, email, full_name, password })
                    });
                    
                    if (response.ok) {
                        document.getElementById('success').textContent = 'Registration successful! Redirecting to login...';
                        setTimeout(() => {
                            window.location.href = '/auth/login';
                        }, 2000);
                    } else {
                        const error = await response.json();
                        document.getElementById('error').textContent = error.detail || 'Registration failed';
                    }
                } catch (error) {
                    document.getElementById('error').textContent = 'Network error';
                }
            });
        </script>
    </body>
    </html>
    """

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Login with username and password."""
    try:
        auth_service = get_auth_service()
        token = auth_service.login_user(user_data)
        return token
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/register")
async def register(user_data: UserRegister, request: Request):
    """Register a new user with RBAC profile."""
    try:
        print(f"Registration attempt for user: {user_data.username}, email: {user_data.email}")
        
        # Verify reCAPTCHA if token is provided
        if user_data.recaptcha_token:
            recaptcha_service = get_recaptcha_service()
            client_ip = request.client.host if request.client else None
            
            is_valid = await recaptcha_service.verify_token(
                user_data.recaptcha_token, 
                client_ip
            )
            
            if not is_valid:
                print("Registration failed: reCAPTCHA verification failed")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="reCAPTCHA verification failed. Please try again."
                )
        
        auth_service = get_auth_service()
        profile = auth_service.register_user(user_data)
        if not profile:
            print("Registration failed: Username or email already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )
        print(f"Registration successful for user: {profile.username}")
        return {"message": "User registered successfully", "user_id": profile.id}
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_active_user)):
    """Get current user's profile with RBAC information."""
    try:
        auth_service = get_auth_service()
        profile = auth_service.get_user_profile(current_user["id"])
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/profile/openai-key")
async def update_openai_key(
    api_key_data: dict,
    current_user: dict = Depends(get_current_active_user)
):
    """Update user's OpenAI API key."""
    try:
        auth_service = get_auth_service()
        success = auth_service.set_user_openai_key(
            current_user["id"], 
            api_key_data.get("api_key", "")
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update OpenAI API key"
            )
        return {"message": "OpenAI API key updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/profile/openai-key")
async def get_openai_key(current_user: dict = Depends(get_current_active_user)):
    """Get user's OpenAI API key (masked)."""
    try:
        auth_service = get_auth_service()
        api_key = auth_service.get_user_openai_key(current_user["id"])
        if api_key:
            # Return masked version for security
            masked_key = api_key[:7] + "*" * (len(api_key) - 10) + api_key[-3:]
            return {"api_key": masked_key, "has_key": True}
        return {"api_key": None, "has_key": False}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/google")
async def google_oauth_start():
    """Start Google OAuth flow."""
    try:
        auth_service = get_auth_service()
        if not auth_service.google_client_id or auth_service.google_client_id == "your-google-client-id":
            return HTMLResponse("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>OAuth Not Configured</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                    .container { max-width: 500px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
                    h1 { color: #dc3545; }
                    .warning { color: #856404; background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }
                    .info { color: #0c5460; background: #d1ecf1; padding: 15px; border-radius: 5px; margin: 20px 0; }
                    .code { background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0; font-family: monospace; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>⚠️ Google OAuth Not Configured</h1>
                    <div class="warning">
                        <strong>Google OAuth is not configured for this application.</strong>
                    </div>
                    <div class="info">
                        <p><strong>To enable Google OAuth:</strong></p>
                        <ol style="text-align: left;">
                            <li>Go to <a href="https://console.developers.google.com/" target="_blank">Google Cloud Console</a></li>
                            <li>Create a new project or select existing one</li>
                            <li>Enable Google+ API</li>
                            <li>Create OAuth 2.0 credentials</li>
                            <li>Add authorized redirect URI: <span class="code">http://localhost:3000/auth/google/callback</span></li>
                            <li>Update your .env file with the credentials</li>
                        </ol>
                    </div>
                    <p>For now, you can use the traditional login method.</p>
                    <button onclick="window.location.href='http://localhost:3000/auth/login'" style="background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Back to Login</button>
                </div>
            </body>
            </html>
            """)
        
        # Use the frontend redirect URI for the OAuth flow
        frontend_redirect_uri = "http://localhost:3000/auth/google/callback"
        google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={auth_service.google_client_id}&redirect_uri={frontend_redirect_uri}&scope=openid%20email%20profile"
        return RedirectResponse(url=google_auth_url)
    except Exception as e:
        print(f"Google OAuth start error: {e}")
        raise HTTPException(status_code=500, detail="OAuth configuration error")

@router.get("/google/callback")
async def google_oauth_callback(code: str = Query(None, description="Authorization code from Google")):
    """Handle Google OAuth callback."""
    print(f"Google OAuth callback called with code: {code}")
    
    if not code:
        print("No code provided in Google OAuth callback")
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OAuth Error</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
                h1 { color: #dc3545; }
                .error { color: #dc3545; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ OAuth Error</h1>
                <p class="error">Authorization code is missing. Please try signing in again.</p>
                <button onclick="window.location.href='http://localhost:3000/auth/login'">Back to Login</button>
            </div>
        </body>
        </html>
        """)
    
    try:
        print(f"Processing Google OAuth with code: {code}")
        auth_service = get_auth_service()
        token = await auth_service.handle_google_oauth(code)
        print(f"Google OAuth successful, token: {token.access_token[:20]}...")
        
        # Return HTML that stores the token and redirects to frontend
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Successful</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
                h1 {{ color: #28a745; }}
                .success {{ color: #28a745; margin: 20px 0; }}
                .token {{ background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 20px 0; font-family: monospace; word-break: break-all; }}
            </style>
            <script>
                // Store the token in localStorage
                localStorage.setItem('access_token', '{token.access_token}');
                localStorage.setItem('auth_token', '{token.access_token}');
                
                // Redirect to frontend
                window.location.href = 'http://localhost:3000/';
            </script>
        </head>
        <body>
            <div class="container">
                <h1>✅ Authentication Successful!</h1>
                <p class="success">You have been successfully authenticated.</p>
                <p>Redirecting to the application...</p>
                <div class="token">Token: {token.access_token[:20]}...</div>
            </div>
        </body>
        </html>
        """)
    except ValueError as e:
        print(f"Google OAuth failed with error: {e}")
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OAuth Error</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
                h1 {{ color: #dc3545; }}
                .error {{ color: #dc3545; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ OAuth Error</h1>
                <p class="error">Authentication failed: {str(e)}</p>
                <button onclick="window.location.href='http://localhost:3000/auth/login'">Back to Login</button>
            </div>
        </body>
        </html>
        """)
    except Exception as e:
        print(f"Google OAuth failed with unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OAuth Error</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
                h1 {{ color: #dc3545; }}
                .error {{ color: #dc3545; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ OAuth Error</h1>
                <p class="error">Authentication failed with unexpected error: {str(e)}</p>
                <button onclick="window.location.href='http://localhost:3000/auth/login'">Back to Login</button>
            </div>
        </body>
        </html>
        """)

@router.get("/github")
async def github_oauth_start():
    """Start GitHub OAuth flow."""
    try:
        auth_service = get_auth_service()
        if not auth_service.github_client_id or auth_service.github_client_id == "your-github-client-id":
            return HTMLResponse("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>OAuth Not Configured</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                    .container { max-width: 500px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
                    h1 { color: #dc3545; }
                    .warning { color: #856404; background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }
                    .info { color: #0c5460; background: #d1ecf1; padding: 15px; border-radius: 5px; margin: 20px 0; }
                    .code { background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0; font-family: monospace; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>⚠️ GitHub OAuth Not Configured</h1>
                    <div class="warning">
                        <strong>GitHub OAuth is not configured for this application.</strong>
                    </div>
                    <div class="info">
                        <p><strong>To enable GitHub OAuth:</strong></p>
                        <ol style="text-align: left;">
                            <li>Go to <a href="https://github.com/settings/developers" target="_blank">GitHub Developer Settings</a></li>
                            <li>Click "New OAuth App"</li>
                            <li>Fill in the application details</li>
                            <li>Set Authorization callback URL to: <span class="code">http://localhost:3000/auth/github/callback</span></li>
                            <li>Update your .env file with the credentials</li>
                        </ol>
                    </div>
                    <p>For now, you can use the traditional login method.</p>
                    <button onclick="window.location.href='http://localhost:3000/auth/login'" style="background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Back to Login</button>
                </div>
            </body>
            </html>
            """)
        
        # Use the frontend redirect URI for the OAuth flow
        frontend_redirect_uri = "http://localhost:3000/auth/github/callback"
        github_auth_url = f"https://github.com/login/oauth/authorize?client_id={auth_service.github_client_id}&redirect_uri={frontend_redirect_uri}&scope=user:email"
        return RedirectResponse(url=github_auth_url)
    except Exception as e:
        print(f"GitHub OAuth start error: {e}")
        raise HTTPException(status_code=500, detail="OAuth configuration error")

@router.get("/github/callback")
async def github_oauth_callback(code: str = Query(None, description="Authorization code from GitHub")):
    """Handle GitHub OAuth callback."""
    if not code:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OAuth Error</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
                h1 { color: #dc3545; }
                .error { color: #dc3545; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ OAuth Error</h1>
                <p class="error">Authorization code is missing. Please try signing in again.</p>
                <button onclick="window.location.href='http://localhost:3000/auth/login'">Back to Login</button>
            </div>
        </body>
        </html>
        """)
    
    try:
        auth_service = get_auth_service()
        token = await auth_service.handle_github_oauth(code)
        
        # Return HTML that stores the token and redirects to frontend
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication Successful</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
                h1 {{ color: #28a745; }}
                .success {{ color: #28a745; margin: 20px 0; }}
                .token {{ background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 20px 0; font-family: monospace; word-break: break-all; }}
            </style>
            <script>
                // Store the token in localStorage
                localStorage.setItem('access_token', '{token.access_token}');
                localStorage.setItem('auth_token', '{token.access_token}');
                
                // Redirect to frontend
                window.location.href = 'http://localhost:3000/';
            </script>
        </head>
        <body>
            <div class="container">
                <h1>✅ Authentication Successful!</h1>
                <p class="success">You have been successfully authenticated.</p>
                <p>Redirecting to the application...</p>
                <div class="token">Token: {token.access_token[:20]}...</div>
            </div>
        </body>
        </html>
        """)
    except ValueError as e:
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OAuth Error</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
                h1 {{ color: #dc3545; }}
                .error {{ color: #dc3545; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ OAuth Error</h1>
                <p class="error">Authentication failed: {str(e)}</p>
                <button onclick="window.location.href='http://localhost:3000/auth/login'">Back to Login</button>
            </div>
        </body>
        </html>
        """)
    except Exception as e:
        print(f"GitHub OAuth failed with unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OAuth Error</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
                h1 {{ color: #dc3545; }}
                .error {{ color: #dc3545; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ OAuth Error</h1>
                <p class="error">Authentication failed with unexpected error: {str(e)}</p>
                <button onclick="window.location.href='http://localhost:3000/auth/login'">Back to Login</button>
            </div>
        </body>
        </html>
        """)

@router.get("/success")
async def oauth_success(token: str = Query(..., description="Access token")):
    """OAuth success page - redirects to frontend with token."""
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Authentication Successful</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
            h1 {{ color: #28a745; }}
            .success {{ color: #28a745; margin: 20px 0; }}
            .token {{ background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 20px 0; font-family: monospace; word-break: break-all; }}
            .btn {{ display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            .btn:hover {{ background: #0056b3; }}
            .btn-primary {{ background: #28a745; }}
            .btn-primary:hover {{ background: #1e7e34; }}
        </style>
        <script>
            // Store the token in localStorage
            localStorage.setItem('access_token', '{token}');
            localStorage.setItem('auth_token', '{token}');
            
            // Try to redirect to frontend
            const frontendUrl = 'http://localhost:3000/'; // TODO: Make this configurable
            
            // Check if frontend is accessible
            fetch(frontendUrl, {{ method: 'HEAD', mode: 'no-cors' }})
                .then(() => {{
                    // Frontend is accessible, redirect
                    window.location.href = frontendUrl;
                }})
                .catch(() => {{
                    // Frontend not accessible, show manual redirect
                    document.getElementById('manual-redirect').style.display = 'block';
                    document.getElementById('auto-redirect').style.display = 'none';
                }});
        </script>
    </head>
    <body>
        <div class="container">
            <h1>✅ Authentication Successful!</h1>
            <p class="success">You have been successfully authenticated.</p>
            
            <div id="auto-redirect">
                <p>Redirecting to the application...</p>
                <div class="token">Token: {token[:20]}...</div>
            </div>
            
            <div id="manual-redirect" style="display: none;">
                <p>Please manually navigate to the frontend application.</p>
                <div class="token">Token: {token[:20]}...</div>
                <p><strong>Your token has been stored in the browser.</strong></p>
                <a href="http://localhost:3000/" class="btn btn-primary">Go to Application</a>
            </div>
            
            <p><small>If you are not redirected automatically, <a href="/">click here</a>.</small></p>
        </div>
    </body>
    </html>
    """)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """Get current user information."""
    return UserResponse(**current_user)

@router.get("/me/with-permissions")
async def get_current_user_with_permissions(current_user: dict = Depends(get_current_active_user)):
    """Get current user information with roles and permissions."""
    try:
        auth_service = get_auth_service()
        # Get user profile (simplified without RBAC)
        profile = auth_service.get_user_profile(current_user["id"])
        
        # Check if user has admin permissions (simplified)
        has_admin_permission = auth_service.has_permission(current_user["id"], "admin:manage")
        
        return {
            **current_user,
            "roles": ["admin"] if current_user.get("is_admin") else [],
            "permissions": ["admin:manage"] if current_user.get("is_admin") else [],
            "has_admin_access": has_admin_permission,
            "profile": profile if profile else None
        }
    except Exception as e:
        logger.error(f"Failed to get user permissions: {e}")
        return {
            **current_user,
            "roles": [],
            "permissions": [],
            "has_admin_access": False,
            "profile": None
        }

@router.get("/debug/env")
async def debug_environment():
    """Debug endpoint to check environment variables."""
    return {
        "SECRET_KEY": "***" if os.getenv("SECRET_KEY") else "Not set",
        "GOOGLE_CLIENT_ID": "***" if os.getenv("GOOGLE_CLIENT_ID") else "Not set",
        "GOOGLE_CLIENT_SECRET": "***" if os.getenv("GOOGLE_CLIENT_SECRET") else "Not set",
        "GOOGLE_REDIRECT_URI": os.getenv("GOOGLE_REDIRECT_URI", "Not set"),
        "GITHUB_CLIENT_ID": "***" if os.getenv("GITHUB_CLIENT_ID") else "Not set",
        "GITHUB_CLIENT_SECRET": "***" if os.getenv("GITHUB_CLIENT_SECRET") else "Not set",
        "GITHUB_REDIRECT_URI": os.getenv("GITHUB_REDIRECT_URI", "Not set"),
    }

@router.get("/debug/oauth-config")
async def debug_oauth_config():
    """Debug endpoint to check OAuth configuration."""
    try:
        auth_service = get_auth_service()
        config_status = {
            "google_oauth_configured": bool(auth_service.google_client_id and auth_service.google_client_secret),
            "google_client_id": auth_service.google_client_id[:10] + "..." if auth_service.google_client_id else "Not set",
            "google_redirect_uri": auth_service.google_redirect_uri,
            "github_oauth_configured": bool(auth_service.github_client_id and auth_service.github_client_secret),
            "github_redirect_uri": auth_service.github_redirect_uri,
            "secret_key_configured": bool(auth_service.secret_key and auth_service.secret_key != "your-secret-key-change-in-production")
        }
        return config_status
    except Exception as e:
        return {"error": str(e)}

@router.get("/logout")
async def logout():
    """Logout user (client should remove token)."""
    return {"message": "Successfully logged out"}

@router.get("/test-oauth", response_class=HTMLResponse)
async def test_oauth_page():
    """Test page to verify OAuth configuration."""
    auth_service = get_auth_service()
    google_configured = bool(auth_service.google_client_id and auth_service.google_client_secret)
    github_configured = bool(auth_service.github_client_id and auth_service.github_client_secret)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OAuth Test Page</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .status {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .success {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
            .button {{ display: inline-block; padding: 10px 20px; margin: 5px; text-decoration: none; border-radius: 5px; color: white; }}
            .google {{ background: #db4437; }}
            .github {{ background: #333; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>OAuth Configuration Test</h1>
            
            <h2>Configuration Status:</h2>
            <div class="status {'success' if google_configured else 'error'}">
                Google OAuth: {'✅ Configured' if google_configured else '❌ Not configured'}
            </div>
            <div class="status {'success' if github_configured else 'error'}">
                GitHub OAuth: {'✅ Configured' if github_configured else '❌ Not configured'}
            </div>
            
            <h2>Test OAuth Flows:</h2>
            {f'<a href="/auth/google" class="button google">Test Google Sign-In</a>' if google_configured else '<button disabled class="button google" style="opacity: 0.5;">Google Sign-In (Not Configured)</button>'}
            {f'<a href="/auth/github" class="button github">Test GitHub Sign-In</a>' if github_configured else '<button disabled class="button github" style="opacity: 0.5;">GitHub Sign-In (Not Configured)</button>'}
            
            <h2>Debug Info:</h2>
            <p><a href="/auth/debug/oauth-config">View OAuth Configuration Details</a></p>
            
            <h2>Back to Login:</h2>
            <p><a href="/auth/login">Return to Login Page</a></p>
        </div>
    </body>
    </html>
    """

# User Merging and OAuth Management Endpoints
@router.post("/merge-users")
async def merge_users_by_email(
    email: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Merge all users with the same email address."""
    try:
        auth_service = get_auth_service()
        merged_user = auth_service.merge_users_by_email(email)
        
        if merged_user:
            return {
                "message": f"Successfully merged users for email: {email}",
                "merged_user": {
                    "id": merged_user["id"],
                    "username": merged_user["username"],
                    "email": merged_user["email"],
                    "full_name": merged_user.get("full_name"),
                    "oauth_providers": merged_user.get("oauth_providers", [])
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No users found with email: {email}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/oauth-providers/{user_id}")
async def get_user_oauth_providers(
    user_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Get all OAuth providers linked to a user."""
    try:
        auth_service = get_auth_service()
        providers = auth_service.get_user_oauth_providers(user_id)
        
        return {
            "user_id": user_id,
            "oauth_providers": providers
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/link-oauth")
async def link_oauth_account(
    provider: str,
    provider_user_id: str,
    email: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Link an OAuth account to an existing user with the same email."""
    try:
        auth_service = get_auth_service()
        linked_user = auth_service.link_oauth_to_existing_user(provider, provider_user_id, email)
        
        if linked_user:
            return {
                "message": f"Successfully linked {provider} OAuth account",
                "linked_user": {
                    "id": linked_user["id"],
                    "username": linked_user["username"],
                    "email": linked_user["email"],
                    "oauth_providers": linked_user.get("oauth_providers", [])
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No user found with email: {email}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/unlink-oauth/{provider}")
async def unlink_oauth_provider(
    provider: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Unlink an OAuth provider from the current user."""
    try:
        auth_service = get_auth_service()
        success = auth_service.unlink_oauth_provider(current_user["id"], provider)
        
        if success:
            return {
                "message": f"Successfully unlinked {provider} OAuth account"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to unlink {provider} OAuth account"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/user-accounts")
async def get_user_accounts(current_user: dict = Depends(get_current_active_user)):
    """Get all accounts (regular and OAuth) for the current user."""
    try:
        auth_service = get_auth_service()
        
        # Get OAuth providers
        oauth_providers = auth_service.get_user_oauth_providers(current_user["id"])
        
        # Check if user has password (regular account)
        has_password = bool(current_user.get("hashed_password"))
        
        return {
            "user_id": current_user["id"],
            "username": current_user["username"],
            "email": current_user["email"],
            "accounts": {
                "regular": has_password,
                "oauth_providers": oauth_providers
            },
            "total_accounts": len(oauth_providers) + (1 if has_password else 0)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
