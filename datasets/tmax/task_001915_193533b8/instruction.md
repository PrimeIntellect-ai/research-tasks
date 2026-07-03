You are a compliance analyst tasked with generating validated audit trails from a legacy authentication system. We recently discovered a batch of old access logs containing user tokens, but we suspect an attacker has injected forged tokens into the logs to cover their tracks.

Your objective is to create a Bash script that acts as an audit filter. It will classify token files as either "legitimate" (clean) or "forged" (evil).

Here is what we know about the legacy system:
1.  **The Master Salt:** The system used a globally shared master salt. A screenshot of the original architecture notes was recovered and placed at `/app/arch_notes.png`. You must extract the master salt from this image (e.g., using `tesseract`).
2.  **Token Generation:** A legitimate token is an all-lowercase SHA-256 hash generated from the concatenated string of the `SALT`, the `USERNAME`, and a 4-digit `PIN` (from `0000` to `9999`). 
    *   Format before hashing: `<SALT><USERNAME><PIN>` (no spaces or delimiters).
3.  **Log File Format:** Each log snippet is a text file containing exactly one line in the format: `USERNAME:TOKEN` (e.g., `alice:a1b2c3d4...`).

**Your Tasks:**
1. Determine the master salt from the image at `/app/arch_notes.png`.
2. Write a Bash script at `/home/user/audit_filter.sh`.
3. Ensure your script has executable permissions.
4. Your script must accept exactly one argument: the path to a log snippet file.
    *   Example invocation: `/home/user/audit_filter.sh /tmp/sample.log`
5. The script must parse the file, read the `USERNAME` and `TOKEN`, and perform a brute-force search over all possible 4-digit PINs.
6. If a PIN exists that produces the correct token hash, the script must exit with status `0` (clean/legitimate).
7. If no such PIN exists (the token is forged), the script must exit with status `1` (evil/forged).

You can create temporary sample files in your home directory to test your script. The final automated evaluation will run your script against a hidden directory of hundreds of forged and legitimate token files.