You are a security engineer tasked with rotating the credentials for a legacy internal system. The old authentication token generator is a compiled binary that we need to deprecate and replace with a modern script (in any language of your choice) that exactly replicates its output. 

Unfortunately, the original source code was lost. You must reverse engineer the legacy authentication flow to create a compatible replacement. 

Here is what you need to do:
1. **File Integrity & Setup:** We have provided the legacy token generator binary at `/app/legacy_token_gen`. Ensure the file is executable.
2. **Key Extraction:** The legacy system relies on a rotation salt that was physically printed and scanned. The scan is located at `/app/key_backup.png`. You must use OCR (e.g., `tesseract`, which is preinstalled) to extract the text from this image. Look for the string following "ROTATION_SALT: ".
3. **Reverse Engineering:** Disassemble or analyze `/app/legacy_token_gen` to understand the authentication token generation algorithm. The binary takes a single integer input (a user ID) and prints the generated token. The algorithm involves manipulating the input user ID with a hardcoded internal value and appending the rotation salt.
4. **Implementation:** Write a new token generation program at `/home/user/new_token_gen`. Your program must:
   - Be executable.
   - Accept a single integer as a command-line argument (the user ID).
   - Print the exact same authentication token as `/app/legacy_token_gen` would for that user ID.
   - Read the rotation salt internally (you can hardcode the recovered salt in your script, but the logic must exactly match the legacy behavior).

The automated verifier will randomly generate thousands of user IDs and compare the standard output of your script at `/home/user/new_token_gen` against a reference oracle. Your script's output must be bit-exact equivalent. Do not print any extra debugging lines in the final version of your script.