import pytest
from .crypto import encrypt, decrypt

def test_encryption_roundtrip():
    """
    Tests that a string can be encrypted and then decrypted back to its
    original value.
    """
    original_text = "this is a top secret password"

    encrypted_token = encrypt(original_text)

    # Assert that the encrypted token is not the same as the original
    assert encrypted_token != original_text
    assert isinstance(encrypted_token, str)

    decrypted_text = decrypt(encrypted_token)

    # Assert that the decrypted text matches the original
    assert decrypted_text == original_text

def test_decrypt_invalid_token():
    """
    Tests that decrypting a malformed or invalid token returns an empty string
    for safety.
    """
    invalid_token = "this-is-not-a-valid-fernet-token"
    decrypted_text = decrypt(invalid_token)
    assert decrypted_text == ""

def test_decrypt_non_string_input():
    """
    Tests that decrypt handles non-string input gracefully.
    """
    assert decrypt(None) == ""
    assert decrypt(12345) == ""
