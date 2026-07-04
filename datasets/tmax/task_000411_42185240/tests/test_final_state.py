import jwt

def verify_token_securely(token, secret_key):
    try:
        # Explicitly define the allowed algorithms.
        # This prevents the library from accepting 'none' or other unexpected algorithms (like HS256 when expecting RS256).
        decoded_payload = jwt.decode(
            token, 
            secret_key, 
            algorithms=["HS256"] 
        )
        return decoded_payload
    except jwt.InvalidAlgorithmError:
        print("Error: Invalid or unsupported algorithm used.")
        return None
    except jwt.InvalidSignatureError:
        print("Error: Signature verification failed.")
        return None
    except jwt.DecodeError:
        print("Error: Token is malformed.")
        return None

# Example usage:
SECRET = "your-256-bit-secret"
# A token attempting to use the 'none' algorithm
malicious_token = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyX2lkIjoidWlkXzEyMzQ1Njc4Iiwicm9sZSI6ImFkbWluIn0."

result = verify_token_securely(malicious_token, SECRET)
# Output: Error: Invalid or unsupported algorithm used.