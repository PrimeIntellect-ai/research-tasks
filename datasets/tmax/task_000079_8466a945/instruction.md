You are a security engineer tasked with recovering the admin credential rotation system. 

An automated, locally-running C binary called `rotator` parses raw HTTP requests from a legacy offline system to rotate credentials. Unfortunately, the admin token used to trigger the rotation has been lost. 

However, you've obtained the source code for the tool at `/home/user/rotator.c`. Preliminary analysis suggests a vulnerability in how the tool processes HTTP cookies and decodes payloads.

Your objective is to:
1. Identify the vulnerability in `/home/user/rotator.c`.
2. Craft a malicious HTTP request that exploits the vulnerability to overwrite internal state and bypass the authorization check. The payload must be correctly hex-encoded according to the custom logic in the C file.
3. Save your crafted HTTP request to `/home/user/payload.http`.
4. Run the exploit against the binary to successfully rotate the credentials: `./rotator < /home/user/payload.http`. If successful, the tool will create `/home/user/rotated_password.txt`.
5. Provide a secure version of the source code. Save the patched source code to `/home/user/rotator_fixed.c`. Ensure that the vulnerability is mitigated (e.g., prevent the buffer overflow when decoding) while maintaining the original functionality for valid, smaller tokens.

The tool expects standard HTTP headers, specifically looking for a `Cookie: session=<hex_encoded_value>` line.

Ensure that:
- `/home/user/payload.http` is a valid text file containing the headers necessary to trigger the exploit.
- `/home/user/rotated_password.txt` is generated successfully.
- `/home/user/rotator_fixed.c` compiles without errors and no longer yields admin access when subjected to the same payload.