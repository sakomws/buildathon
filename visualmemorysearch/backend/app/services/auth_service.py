"""Authentication service for the Visual Memory Search API."""

import os
import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import httpx
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.models.auth_schemas import UserLogin, UserRegister, UserResponse, Token, OAuthUserInfo, UserProfile
# RBAC removed - no longer needed

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__default_rounds=12)

# JWT Configuration
# Use a persistent secret key to avoid token invalidation on restart
SECRET_KEY = os.getenv("SECRET_KEY", "persistent-secret-key-for-development-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/google/callback")

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:3000/auth/github/callback")

# In-memory user storage (replace with database in production)
users_db: Dict[str, Dict[str, Any]] = {}
oauth_users_db: Dict[str, Dict[str, Any]] = {}

# Default admin user
DEFAULT_ADMIN = {
    "id": "admin-001",
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "System Administrator",
    "hashed_password": pwd_context.hash("admin123"),
    "is_active": True,
    "created_at": datetime.utcnow(),
    "last_login": None,
    "is_admin": True
}
users_db["admin"] = DEFAULT_ADMIN


class AuthService:
    """Authentication service for user management and OAuth."""
    
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        # Store OAuth config as instance variables for easy access
        self.google_client_id = GOOGLE_CLIENT_ID
        self.google_client_secret = GOOGLE_CLIENT_SECRET
        self.google_redirect_uri = GOOGLE_REDIRECT_URI
        self.github_client_id = GITHUB_CLIENT_ID
        self.github_client_secret = GITHUB_CLIENT_SECRET
        self.github_redirect_uri = GITHUB_REDIRECT_URI
        
        # Initialize RBAC service
        # RBAC removed - using simple admin flag
        
        # Debug logging
        print(f"AuthService initialized:")
        print(f"  Google OAuth: {'Configured' if self.google_client_id and self.google_client_secret else 'Not configured'}")
        print(f"  Google Client ID: {self.google_client_id[:10] + '...' if self.google_client_id else 'None'}")
        print(f"  Google Redirect URI: {self.google_redirect_uri}")
        print(f"  GitHub OAuth: {'Configured' if self.github_client_id and self.github_client_secret else 'Not configured'}")
        print(f"  Secret Key: {'Configured' if self.secret_key and self.secret_key != 'your-secret-key-change-in-production' else 'Not configured'}")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token."""
        try:
            print(f"Verifying token: {token[:20]}...")
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            print(f"Token payload: {payload}")
            username: str = payload.get("sub")
            if username is None:
                print("No username in token payload")
                return None
            print(f"Username from token: {username}")
            return payload
        except JWTError as e:
            print(f"JWT decode error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in token verification: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with username and password."""
        user = users_db.get(username)
        if not user:
            return None
        if not self.verify_password(password, user["hashed_password"]):
            return None
        return user
    
    def create_user(self, user_data: UserRegister) -> UserResponse:
        """Create a new user."""
        try:
            # Check if username already exists
            if user_data.username in users_db:
                raise ValueError("Username already exists")
            
            # Check if email already exists
            for user in users_db.values():
                if user.get("email") == user_data.email:
                    raise ValueError("Email already exists")
            
            # Generate user ID
            user_id = str(uuid.uuid4())
            
            # Check if this is the first user (make them admin)
            is_first_user = len(users_db) == 0 and len(oauth_users_db) == 0
            
            # Create user
            user = {
                "id": user_id,
                "username": user_data.username,
                "email": user_data.email,
                "full_name": user_data.full_name,
                "hashed_password": self.get_password_hash(user_data.password),
                "is_active": True,
                "is_admin": is_first_user,  # First user becomes admin
                "created_at": datetime.utcnow(),
                "last_login": None,
                "oauth_providers": []
            }
            
            # Add to users_db
            users_db[user_data.username] = user
            
            # If this is the first user, they're already admin (no RBAC needed)
            if is_first_user:
                print(f"First user {user_data.username} automatically set as admin (RBAC disabled)")
            
            print(f"Created user: {user_data.username} (Admin: {is_first_user})")
            return UserResponse(**user)
            
        except Exception as e:
            print(f"Error creating user: {e}")
            raise ValueError(str(e))
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        print(f"Looking up user by username: {username}")
        
        # First check regular users
        user = users_db.get(username)
        if user:
            print(f"User found in users_db: {user}")
            return user
        
        # If not found in regular users, check OAuth users
        print(f"User not found in users_db, checking OAuth users...")
        for oauth_key, oauth_user in oauth_users_db.items():
            if oauth_user.get("username") == username:
                print(f"User found in oauth_users_db: {oauth_user}")
                return oauth_user
        
        print(f"User not found in either database")
        return None

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        print(f"Looking up user by ID: {user_id}")
        
        # First check regular users
        for user in users_db.values():
            if user.get("id") == user_id:
                print(f"User found in users_db: {user}")
                return user
        
        # If not found in regular users, check OAuth users
        print(f"User not found in users_db, checking OAuth users...")
        for oauth_key, oauth_user in oauth_users_db.items():
            if oauth_user.get("id") == user_id:
                print(f"User found in oauth_users_db: {oauth_user}")
                return oauth_user
        
        print(f"User not found in either database")
        return None
    
    def merge_users_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Merge all users with the same email address across different authentication providers.
        Returns the merged user profile or None if no users found.
        """
        try:
            # Find all users with the same email
            users_to_merge = []
            
            # Check regular users
            for username, user in users_db.items():
                if user.get("email") == email:
                    users_to_merge.append({
                        "type": "regular",
                        "username": username,
                        "user": user
                    })
            
            # Check OAuth users
            for oauth_key, user in oauth_users_db.items():
                if user.get("email") == email:
                    provider = oauth_key.split(":")[0] if ":" in oauth_key else "unknown"
                    users_to_merge.append({
                        "type": "oauth",
                        "provider": provider,
                        "oauth_key": oauth_key,
                        "user": user
                    })
            
            if not users_to_merge:
                return None
            
            if len(users_to_merge) == 1:
                # Only one user found, return it
                return users_to_merge[0]["user"]
            
            # Multiple users found, merge them
            print(f"Merging {len(users_to_merge)} users with email: {email}")
            
            # Choose the primary user (prefer regular user, then most recent)
            primary_user = None
            primary_user_data = None
            
            # First, try to find a regular user
            for user_data in users_to_merge:
                if user_data["type"] == "regular":
                    primary_user_data = user_data
                    primary_user = user_data["user"]
                    break
            
            # If no regular user, choose the most recent one
            if not primary_user:
                primary_user_data = max(users_to_merge, key=lambda x: x["user"].get("created_at", datetime.min))
                primary_user = primary_user_data["user"]
            
            # Merge user data
            merged_user = primary_user.copy()
            
            # Collect all OAuth providers
            oauth_providers = []
            for user_data in users_to_merge:
                if user_data["type"] == "oauth":
                    oauth_providers.append(user_data["provider"])
            
            # Update merged user with OAuth providers
            if oauth_providers:
                merged_user["oauth_providers"] = oauth_providers
            
            # Use the most complete profile information
            for user_data in users_to_merge:
                user = user_data["user"]
                if user.get("full_name") and not merged_user.get("full_name"):
                    merged_user["full_name"] = user["full_name"]
                if user.get("avatar_url") and not merged_user.get("avatar_url"):
                    merged_user["avatar_url"] = user["avatar_url"]
                if user.get("is_admin") and not merged_user.get("is_admin"):
                    merged_user["is_admin"] = user["is_admin"]
            
            # Update all references to point to the merged user
            merged_username = merged_user["username"]
            merged_user_id = merged_user["id"]
            
            # Update users_db
            for user_data in users_to_merge:
                if user_data["type"] == "regular":
                    old_username = user_data["username"]
                    if old_username != merged_username:
                        # Remove old user entry
                        if old_username in users_db:
                            del users_db[old_username]
            
            # Update oauth_users_db
            for user_data in users_to_merge:
                if user_data["type"] == "oauth":
                    oauth_key = user_data["oauth_key"]
                    oauth_users_db[oauth_key] = merged_user
            
            # Ensure the merged user is in users_db
            users_db[merged_username] = merged_user
            
            # Update user profile (simplified without RBAC)
            try:
                # Ensure merged user has basic profile data
                if "full_name" not in merged_user:
                    merged_user["full_name"] = merged_user.get("full_name", "Merged User")
                print(f"Updated profile for merged user: {merged_user['username']}")
            except Exception as e:
                print(f"Warning: Could not update profile for merged user: {e}")
            
            print(f"Successfully merged users for email: {email}")
            return merged_user
            
        except Exception as e:
            print(f"Error merging users for email {email}: {e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email, including merged users."""
        # First try to get a merged user
        merged_user = self.merge_users_by_email(email)
        if merged_user:
            return merged_user
        
        # Fallback to direct lookup
        for user in users_db.values():
            if user.get("email") == email:
                return user
        
        for user in oauth_users_db.values():
            if user.get("email") == email:
                return user
        
        return None

    def get_user_by_oauth(self, provider: str, provider_user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by OAuth provider and provider user ID."""
        oauth_key = f"{provider}:{provider_user_id}"
        return oauth_users_db.get(oauth_key)

    def link_oauth_to_existing_user(self, provider: str, provider_user_id: str, email: str) -> Optional[Dict[str, Any]]:
        """
        Link an OAuth account to an existing user with the same email.
        Returns the linked user or None if no matching user found.
        """
        try:
            # Find existing user by email
            existing_user = self.get_user_by_email(email)
            if not existing_user:
                return None
            
            # Create OAuth key
            oauth_key = f"{provider}:{provider_user_id}"
            
            # Link OAuth account to existing user
            oauth_users_db[oauth_key] = existing_user
            
            # Update user with OAuth provider info
            if "oauth_providers" not in existing_user:
                existing_user["oauth_providers"] = []
            if provider not in existing_user["oauth_providers"]:
                existing_user["oauth_providers"].append(provider)
            
            print(f"Linked {provider} OAuth account to existing user: {existing_user['username']}")
            return existing_user
            
        except Exception as e:
            print(f"Error linking OAuth account: {e}")
            return None

    def get_user_oauth_providers(self, user_id: str) -> list:
        """Get all OAuth providers linked to a user."""
        providers = []
        for oauth_key, user in oauth_users_db.items():
            if user.get("id") == user_id:
                provider = oauth_key.split(":")[0] if ":" in oauth_key else "unknown"
                providers.append(provider)
        return providers

    def unlink_oauth_provider(self, user_id: str, provider: str) -> bool:
        """Unlink an OAuth provider from a user."""
        try:
            keys_to_remove = []
            for oauth_key, user in oauth_users_db.items():
                if user.get("id") == user_id and oauth_key.startswith(f"{provider}:"):
                    keys_to_remove.append(oauth_key)
            
            for key in keys_to_remove:
                del oauth_users_db[key]
            
            # Update user's oauth_providers list
            for user in users_db.values():
                if user.get("id") == user_id and "oauth_providers" in user:
                    if provider in user["oauth_providers"]:
                        user["oauth_providers"].remove(provider)
            
            return True
        except Exception as e:
            print(f"Error unlinking OAuth provider: {e}")
            return False
    
    def update_last_login(self, username: str):
        """Update user's last login time."""
        if username in users_db:
            users_db[username]["last_login"] = datetime.utcnow()
    
    def login_user(self, user_data: UserLogin) -> Token:
        """Login a user and return access token."""
        user = self.authenticate_user(user_data.username, user_data.password)
        if not user:
            raise ValueError("Invalid username or password")
        
        if not user["is_active"]:
            raise ValueError("User account is disabled")
        
        # Update last login
        self.update_last_login(user_data.username)
        
        # Create access token
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={"sub": user["username"], "user_id": user["id"]},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            expires_in=self.access_token_expire_minutes * 60
        )
    
    async def handle_google_oauth(self, code: str) -> Token:
        """Handle Google OAuth authentication."""
        if not self.google_client_id or not self.google_client_secret:
            raise ValueError("Google OAuth not configured")
        
        print(f"Starting Google OAuth with client_id: {self.google_client_id[:10]}...")
        print(f"Redirect URI: {self.google_redirect_uri}")
        
        # Exchange code for access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": self.google_client_id,
            "client_secret": self.google_client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.google_redirect_uri
        }
        
        print(f"Token exchange data: {token_data}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=token_data)
            print(f"Token exchange response status: {response.status_code}")
            print(f"Token exchange response: {response.text}")
            
            if response.status_code != 200:
                error_detail = f"Failed to exchange code for token. Status: {response.status_code}, Response: {response.text}"
                print(error_detail)
                raise ValueError(error_detail)
            
            token_info = response.json()
            access_token = token_info["access_token"]
            print(f"Successfully got access token: {access_token[:20]}...")
        
        # Get user info from Google
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(user_info_url, headers=headers)
            if response.status_code != 200:
                raise ValueError("Failed to get user info from Google")
            
            google_user = response.json()
            print(f"Got user info: {google_user.get('email', 'No email')}")
        
        # Create or get user
        user = await self._get_or_create_oauth_user(
            provider="google",
            provider_user_id=google_user["id"],
            email=google_user["email"],
            username=google_user.get("given_name", "").lower(),
            full_name=google_user.get("name"),
            avatar_url=google_user.get("picture")
        )
        
        # Create access token
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        jwt_token = self.create_access_token(
            data={"sub": user["username"], "user_id": user["id"]},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=jwt_token,
            expires_in=self.access_token_expire_minutes * 60
        )
    
    async def handle_github_oauth(self, code: str) -> Token:
        """Handle GitHub OAuth authentication."""
        if not self.github_client_id or not self.github_client_secret:
            raise ValueError("GitHub OAuth not configured")
        
        # Exchange code for access token
        token_url = "https://github.com/login/oauth/access_token"
        token_data = {
            "client_id": self.github_client_id,
            "client_secret": self.github_client_secret,
            "code": code
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=token_data, headers={"Accept": "application/json"})
            if response.status_code != 200:
                raise ValueError("Failed to exchange code for token")
            
            token_info = response.json()
            access_token = token_info.get("access_token")
            if not access_token:
                raise ValueError("Failed to get access token from GitHub")
        
        # Get user info from GitHub
        user_info_url = "https://api.github.com/user"
        headers = {"Authorization": f"token {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(user_info_url, headers=headers)
            if response.status_code != 200:
                raise ValueError("Failed to get user info from GitHub")
            
            github_user = response.json()
        
        # Create or get user
        user = await self._get_or_create_oauth_user(
            provider="github",
            provider_user_id=str(github_user["id"]),
            email=github_user.get("email", f"{github_user['login']}@github.com"),
            username=github_user["login"],
            full_name=github_user.get("name"),
            avatar_url=github_user.get("avatar_url")
        )
        
        # Create access token
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        jwt_token = self.create_access_token(
            data={"sub": user["username"], "user_id": user["id"]},
            expires_delta=access_token_expires
        )
        
        # Debug: print what we're creating
        token_data = {
            "access_token": jwt_token,
            "expires_in": self.access_token_expire_minutes * 60
        }
        print(f"Creating GitHub Token with data: {token_data}")
        
        return Token(
            access_token=jwt_token,
            expires_in=self.access_token_expire_minutes * 60
        )
    
    async def _get_or_create_oauth_user(
        self,
        provider: str,
        provider_user_id: str,
        email: str,
        username: str,
        full_name: Optional[str] = None,
        avatar_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get existing OAuth user or create a new one with email-based merging."""
        oauth_key = f"{provider}:{provider_user_id}"
        
        # Check if OAuth account already exists
        if oauth_key in oauth_users_db:
            # User exists, return it
            return oauth_users_db[oauth_key]
        
        # Try to merge with existing users by email
        merged_user = self.merge_users_by_email(email)
        if merged_user:
            # Link this OAuth account to the merged user
            oauth_users_db[oauth_key] = merged_user
            
            # Update user with OAuth provider info
            if "oauth_providers" not in merged_user:
                merged_user["oauth_providers"] = []
            if provider not in merged_user["oauth_providers"]:
                merged_user["oauth_providers"].append(provider)
            
            print(f"Linked {provider} OAuth to merged user: {merged_user['username']}")
            return merged_user
        
        # No existing user found, create new user
        user_id = str(uuid.uuid4())
        new_username = username
        counter = 1
        
        # Ensure unique username
        while new_username in users_db:
            new_username = f"{username}{counter}"
            counter += 1
        
        # Check if this is the first user (make them admin)
        is_first_user = len(users_db) == 0 and len(oauth_users_db) == 0
        
        user = {
            "id": user_id,
            "username": new_username,
            "email": email,
            "full_name": full_name or username,
            "hashed_password": "",  # OAuth users don't have passwords
            "is_active": True,
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "is_admin": is_first_user,  # First user becomes admin
            "oauth_providers": [provider],
            "avatar_url": avatar_url
        }
        
        users_db[new_username] = user
        oauth_users_db[oauth_key] = user
        
        # OAuth user created (RBAC disabled)
        if is_first_user:
            print(f"First OAuth user {new_username} automatically set as admin (RBAC disabled)")
        
        print(f"Created new OAuth user: {new_username} with {provider} (Admin: {is_first_user})")
        return user
    
    # RBAC Integration Methods
    def register_user(self, user_data: UserRegister) -> Optional[UserProfile]:
        """Register a new user with RBAC profile."""
        # Check if username or email already exists
        if self.get_user_by_username(user_data.username):
            return None
        
        if self.get_user_by_email(user_data.email):
            return None
        
        # Create user record
        user_id = str(uuid.uuid4())
        
        # Check if this is the first user (make them admin)
        is_first_user = len(users_db) == 0 and len(oauth_users_db) == 0
        
        user_record = {
            "id": user_id,
            "username": user_data.username,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "hashed_password": self.get_password_hash(user_data.password),
            "is_active": True,
            "created_at": datetime.utcnow(),
            "last_login": None,
            "is_admin": is_first_user  # First user becomes admin
        }
        
        # Save to users_db
        users_db[user_data.username] = user_record
        
        # Return the created user record (simplified without RBAC)
        return user_record
    
    def get_user_profile(self, user_id: str) -> Optional[dict]:
        """Get user profile (simplified without RBAC)."""
        user = self.get_user_by_id(user_id)
        return user if user else None
    
    def update_user_profile(self, user_id: str, **kwargs) -> Optional[dict]:
        """Update user profile (simplified without RBAC)."""
        user = self.get_user_by_id(user_id)
        if user:
            user.update(kwargs)
            return user
        return None
    
    def get_user_storage_path(self, user_id: str):
        """Get user's storage path for screenshots (simplified without RBAC)."""
        user = self.get_user_by_id(user_id)
        if user and "storage_path" in user:
            storage_path = Path(user["storage_path"])
            storage_path.mkdir(parents=True, exist_ok=True)
            return storage_path
        # Fallback: create default path
        storage_path = Path(f"data/screenshots/user_{user_id}")
        storage_path.mkdir(parents=True, exist_ok=True)
        return storage_path
    
    def get_user_openai_key(self, user_id: str) -> Optional[str]:
        """Get user's OpenAI API key (simplified without RBAC)."""
        user = self.get_user_by_id(user_id)
        return user.get("openai_api_key") if user else None
    
    def set_user_openai_key(self, user_id: str, api_key: str) -> bool:
        """Set user's OpenAI API key (simplified without RBAC)."""
        user = self.get_user_by_id(user_id)
        if user:
            user["openai_api_key"] = api_key
            return True
        return False

    def delete_user(self, user_id: str) -> bool:
        """Delete a user completely from the system."""
        try:
            # Remove from users_db
            username_to_remove = None
            for username, user_data in users_db.items():
                if user_data.get("id") == user_id:
                    username_to_remove = username
                    break
            
            if username_to_remove:
                del users_db[username_to_remove]
                print(f"Removed user {username_to_remove} from users_db")
            
            # Remove from OAuth users if exists
            oauth_keys_to_remove = []
            for oauth_key, oauth_user in oauth_users_db.items():
                if oauth_user.get("id") == user_id:
                    oauth_keys_to_remove.append(oauth_key)
            
            for oauth_key in oauth_keys_to_remove:
                del oauth_users_db[oauth_key]
                print(f"Removed OAuth user {oauth_key}")
            
            return True
        except Exception as e:
            print(f"Error deleting user {user_id}: {e}")
            return False

    # Cookie preferences
    def get_cookie_preferences(self, user_id: str) -> Optional[dict[str, bool]]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        prefs = user.get("cookie_preferences", {})
        return {
            "essential": bool(prefs.get("essential", True)),
            "functional": bool(prefs.get("functional", False)),
            "analytics": bool(prefs.get("analytics", False)),
            "marketing": bool(prefs.get("marketing", False)),
        }

    def set_cookie_preferences(self, user_id: str, prefs: dict) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            user["cookie_preferences"] = prefs
            return True
        return False
    
    # Getter methods for user databases
    def get_users_db(self):
        """Get the users database."""
        return users_db
    
    def get_oauth_users_db(self):
        """Get the OAuth users database."""
        return oauth_users_db
    
    def has_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has a specific permission (simplified - just check admin status)."""
        try:
            # Simplified: just check if user is admin
            user = self.get_user_by_id(user_id)
            if user and user.get("is_admin", False):
                return True
            return False
        except Exception as e:
            print(f"Error checking permission: {e}")
            return False
    
    def has_role(self, user_id: str, role_name: str) -> bool:
        """Check if user has a specific role (simplified - only admin role)."""
        if role_name == "admin":
            user = self.get_user_by_id(user_id)
            return user and user.get("is_admin", False)
        return False


# Global auth service instance - lazy initialization
_auth_service_instance = None

def get_auth_service() -> AuthService:
    """Get the global auth service instance, creating it if necessary."""
    global _auth_service_instance
    if _auth_service_instance is None:
        _auth_service_instance = AuthService()
    return _auth_service_instance
