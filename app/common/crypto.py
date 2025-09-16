import base64
import hashlib
from django.conf import settings
from cryptography.fernet import Fernet, InvalidToken

# --- Fernet Key Generation ---
# It's crucial that the key is 32 bytes and remains consistent.
# We derive it from the Django SECRET_KEY for simplicity.
# In a high-security environment, this should be a separate, managed key.
try:
    # Use SHA-256 to hash the secret key to a 32-byte value
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(key)
    cipher_suite = Fernet(fernet_key)
except Exception:
    # This might happen if settings are not configured, e.g., during startup.
    # We'll set it to None and let applications handle it gracefully if needed.
    cipher_suite = None

def encrypt(text: str) -> str:
    """
    Encrypts a string using the application's Fernet cipher suite.
    Returns the encrypted text as a string.
    """
    if cipher_suite is None:
        raise ValueError("Cipher suite is not initialized. Check Django SECRET_KEY.")
    if not isinstance(text, str):
        raise TypeError("encrypt() requires a string argument.")

    encrypted_text = cipher_suite.encrypt(text.encode('utf-8'))
    return encrypted_text.decode('utf-8')

def decrypt(token: str) -> str:
    """
    Decrypts a Fernet token using the application's cipher suite.
    Returns the original string.
    Returns an empty string if the token is invalid or decryption fails.
    """
    if cipher_suite is None:
        raise ValueError("Cipher suite is not initialized. Check Django SECRET_KEY.")
    if not isinstance(token, str):
        return "" # Or raise an error, returning empty is safer for display.

    try:
        decrypted_text = cipher_suite.decrypt(token.encode('utf-8'))
        return decrypted_text.decode('utf-8')
    except (InvalidToken, TypeError, ValueError):
        # This can happen if the token is malformed, not a string, or invalid.
        # We return an empty string to avoid showing garbage or raising an error.
        return ""
