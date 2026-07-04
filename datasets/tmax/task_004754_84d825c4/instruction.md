You are a security engineer responding to a recent breach. An attacker managed to exfiltrate credentials and deliver a cross-site scripting (XSS) payload that bypassed our weak Content Security Policy (CSP). 

We managed to intercept a video recording (`/app/attack_recording.mp4`) of the attacker's exfiltration tool. The tool transmits data visually by flashing the screen. 

Your tasks are as follows:

1. **Payload Decoding & Extraction:**
   Analyze `/app/attack_recording.mp4`. The video plays at 30 FPS. The data transmission begins immediately after a single solid BLUE frame. Each subsequent frame encodes exactly one bit of data:
   - A solid WHITE frame represents a `1`.
   - A solid BLACK frame represents a `0`.
   The transmission is exactly 256 bits long (32 bytes). Convert this binary sequence into ASCII text. The resulting text contains the compromised secret key and the exploit payload in the format `KEY|PAYLOAD`.
   Write the exactly recovered `KEY` (the part before the `|`) to `/home/user/compromised_key.txt`.

2. **Credential Rotation:**
   Generate a new 16-character securely random alphanumeric key to replace the compromised one. Save this new key to `/home/user/new_key.txt`.

3. **Content Security Policy Enforcement:**
   The attacker's payload was able to execute because our previous CSP allowed inline scripts and lacked proper object restrictions. 
   Draft a new, hardened CSP header string that:
   - Restricts default resources to `'self'`.
   - Allows scripts only from `'self'` and a specific trusted domain: `https://scripts.trusted.internal`.
   - Explicitly disables `unsafe-inline` and `unsafe-eval` for scripts.
   - Restricts object sources to `'none'`.
   Save your final CSP header string to `/home/user/strict_csp.txt`.

Ensure your extraction is as accurate as possible and your CSP is properly formatted according to W3C specifications. An automated metric will score your accuracy in decoding the video payload and the robust enforcement of your CSP.