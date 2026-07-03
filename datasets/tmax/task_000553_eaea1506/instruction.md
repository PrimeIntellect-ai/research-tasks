You are an AI assistant acting as a storage administrator. Disk space on our server is filling up due to legacy application logs stored in `/home/user/app_logs/`. These logs are written in a custom binary-wrapped format and are scattered deeply across various subdirectories. 

Furthermore, the application is still actively writing to some of these files. We need to reclaim space by extracting the log text from the *finished* files, filtering out sensitive and useless information, and consolidating them into a single structured JSON file.

You must write a **Rust** program (you may use shell scripts to orchestrate or assist) to accomplish the following:

1. **Navigate and Find:** Recursively traverse `/home/user/app_logs/` to find all `.dat` files.
2. **Binary Header Extraction:** Each `.dat` file has a 10-byte binary header:
   - Bytes 0-3: Magic string `LOG\x00`
   - Byte 4: Version byte (always `\x01`)
   - Byte 5: Status byte. `\x00` means the file is finished writing. `\x01` means the file is actively being written to.
   - Bytes 6-9: A 32-bit unsigned integer (Little-Endian) specifying the length of the text payload in bytes.
3. **Avoid Race Conditions:** If the Status byte is `\x01` (active), you MUST completely ignore and skip the file.
4. **Text Transformation:** For finished files (`\x00`), read the text payload based on the length specified. 
   - Remove any line that begins with the exact string `DEBUG: `.
   - Redact all IPv4 addresses (e.g., `192.168.1.50`) by replacing them with the string `[REDACTED]`.
5. **Format Conversion:** Consolidate the processed text from all finished logs into a single JSON array file located at `/home/user/cleaned_logs.json`.
   - The JSON must be an array of objects.
   - Each object must have two keys: 
     - `"file"`: The relative path of the file starting from inside the `app_logs` directory (e.g., `"server1/sys.dat"`).
     - `"contents"`: The fully filtered and redacted text payload as a single string (preserving the remaining newlines).

Create and run your Rust project in `/home/user/log_processor/`. Make sure your final JSON file is strictly formatted and valid.