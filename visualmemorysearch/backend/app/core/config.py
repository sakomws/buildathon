"""Configuration management for the Visual Memory Search API."""

from pathlib import Path
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation and defaults."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application settings
    app_name: str = Field(default="Visual Memory Search", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    
    # File storage settings
    screenshot_dir: Path = Field(default=Path("test_screenshots"), description="Screenshot storage directory")
    max_file_size: int = Field(default=16 * 1024 * 1024, description="Maximum file size in bytes")
    allowed_extensions: List[str] = Field(
        default=["png", "jpg", "jpeg", "gif", "bmp"],
        description="Allowed image file extensions"
    )
    
    # AI/ML settings
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-3.5-turbo", description="OpenAI model name")
    embedding_model: str = Field(default="all-MiniLM-L6-v2", description="Text embedding model")
    vision_model: str = Field(default="microsoft/git-base", description="Vision model for feature extraction")
    
    # Search settings
    max_search_results: int = Field(default=10, description="Maximum search results")
    similarity_threshold: float = Field(default=0.7, description="Search similarity threshold")
    
    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[Path] = Field(default=None, description="Log file path")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    
    # Authentication settings
    secret_key: str = Field(default="your-secret-key-change-in-production", description="Secret key for JWT tokens")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration time in minutes")
    
    # Google OAuth settings
    google_client_id: Optional[str] = Field(default=None, description="Google OAuth client ID")
    google_client_secret: Optional[str] = Field(default=None, description="Google OAuth client secret")
    google_redirect_uri: Optional[str] = Field(default="http://localhost:3000/auth/google/callback", description="Google OAuth redirect URI")
    
    # GitHub OAuth settings
    github_client_id: Optional[str] = Field(default=None, description="GitHub OAuth client ID")
    github_client_secret: Optional[str] = Field(default=None, description="GitHub OAuth client secret")
    github_redirect_uri: Optional[str] = Field(default="http://localhost:3000/auth/github/callback", description="GitHub OAuth redirect URI")
    
    # reCAPTCHA settings
    recaptcha_secret_key: Optional[str] = Field(default=None, description="Google reCAPTCHA secret key")
    recaptcha_site_key: Optional[str] = Field(default=None, description="Google reCAPTCHA site key")
    
    @field_validator("screenshot_dir")
    @classmethod
    def validate_screenshot_dir(cls, v: Path) -> Path:
        """Ensure screenshot directory exists and is writable."""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @field_validator("allowed_extensions")
    @classmethod
    def validate_extensions(cls, v: List[str]) -> List[str]:
        """Ensure all extensions are lowercase and valid."""
        return [ext.lower().lstrip('.') for ext in v]
    
    @field_validator("similarity_threshold")
    @classmethod
    def validate_similarity_threshold(cls, v: float) -> float:
        """Ensure similarity threshold is between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError("Similarity threshold must be between 0 and 1")
        return v
    
    @field_validator("max_file_size")
    @classmethod
    def validate_max_file_size(cls, v: int) -> int:
        """Ensure max file size is positive."""
        if v <= 0:
            raise ValueError("Max file size must be positive")
        return v


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset the global settings instance (useful for testing)."""
    global _settings
    _settings = None
