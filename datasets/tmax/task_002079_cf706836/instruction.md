You are an artifact manager for a robotics laboratory. Your job is to curate, verify, and host a set of binary GCode repositories. Recently, the storage system corrupted some files, and the compression key used for the artifacts was lost. 

However, a backup of the key was encoded into a diagnostic video feed.

Your tasks are as follows:

1. **Extract the Key from Video:**
   Analyze the video file located at `/app/key_feed.mp4`. The video contains exactly 128 frames. 
   Convert each frame to grayscale and calculate its average pixel intensity. 
   If the average intensity is greater than 128, the corresponding bit is `1`. Otherwise, the bit is `0`.
   Pack these 128 bits into a 16-byte sequence. Frame 0 represents the Most Significant Bit (MSB) of Byte 0, Frame 7 is the LSB of Byte 0, Frame 8 is the MSB of Byte 1, and so on. This 16-byte sequence is your `XOR_KEY`.

2. **Process and Verify Artifacts:**
   In the directory `/home/user/artifacts/`, you will find several `.gcode.enc` files.
   These files were compressed using `zlib` and then encrypted using a repeating XOR cipher with the `XOR_KEY`. 
   For each `.gcode.enc` file:
   - XOR each byte of the file with the `XOR_KEY`. (The i-th byte of the file is XORed with the `i % 16`-th byte of the key).
   - Decompress the resulting bytes using standard `zlib` decompression.
   - Verify the archive integrity: A valid artifact must successfully decompress AND its decoded plaintext must begin exactly with the string `; BEGIN GCODE`. If a file fails zlib decompression or does not start with this header, it is considered corrupt and must be discarded.

3. **Host the Verified Artifacts:**
   Create an HTTP server listening on `127.0.0.1:8080`.
   For every valid artifact, expose it at the endpoint `GET /artifacts/<filename>`, where `<filename>` is the original filename stripped of the `.enc` extension (e.g., `part1.gcode.enc` becomes `part1.gcode`).
   The response must be the raw decrypted plaintext of the valid GCode file with a `200 OK` status.
   Any requests for corrupt, discarded, or non-existent files must return a `404 Not Found` status.
   
Keep this server running in the foreground or background so the verification system can query it.