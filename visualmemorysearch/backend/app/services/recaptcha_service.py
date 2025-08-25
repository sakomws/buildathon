"""reCAPTCHA verification service for the Visual Memory Search API."""

import httpx
from typing import Optional
from app.core.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class RecaptchaService:
    """Service for verifying Google reCAPTCHA tokens."""
    
    def __init__(self):
        self.settings = get_settings()
        self.verification_url = "https://www.google.com/recaptcha/api/siteverify"
    
    async def verify_token(self, token: str, remote_ip: Optional[str] = None) -> bool:
        """Verify a reCAPTCHA token."""
        try:
            if not self.settings.recaptcha_secret_key:
                logger.warning("reCAPTCHA secret key not configured, skipping verification")
                return True  # Skip verification if not configured
            
            if not token:
                logger.warning("No reCAPTCHA token provided")
                return False
            
            # Handle development skip token
            if token == 'development-skip-token':
                logger.info("Development skip token detected, allowing registration")
                return True
            
            # Prepare verification data
            data = {
                "secret": self.settings.recaptcha_secret_key,
                "response": token
            }
            
            if remote_ip:
                data["remoteip"] = remote_ip
            
            # Verify with Google
            async with httpx.AsyncClient() as client:
                response = await client.post(self.verification_url, data=data)
                response.raise_for_status()
                
                result = response.json()
                
                if result.get("success"):
                    logger.info("reCAPTCHA verification successful")
                    return True
                else:
                    error_codes = result.get("error-codes", [])
                    logger.warning(f"reCAPTCHA verification failed: {error_codes}")
                    return False
                    
        except Exception as e:
            logger.error(f"reCAPTCHA verification error: {e}")
            return False
    
    def is_enabled(self) -> bool:
        """Check if reCAPTCHA is enabled (has secret key configured)."""
        return bool(self.settings.recaptcha_secret_key)


# Global reCAPTCHA service instance
_recaptcha_service: Optional[RecaptchaService] = None


def get_recaptcha_service() -> RecaptchaService:
    """Get the global reCAPTCHA service instance."""
    global _recaptcha_service
    if _recaptcha_service is None:
        _recaptcha_service = RecaptchaService()
    return _recaptcha_service
