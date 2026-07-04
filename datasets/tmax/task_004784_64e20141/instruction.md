You are a storage administrator managing a massive ingress of user-uploaded storage manifest files and monitoring automated storage arrays. You need to analyze a dashboard video for failures and build a robust, secure ingestion pipeline for manifest files.

**Part 1: Video Analysis**
You have been provided with a screen recording of the storage dashboard at `/app/storage_dashboard.mp4`. The dashboard flashes a bright red frame (where the average color of the frame is > 150 for Red and < 50 for Green/Blue) whenever a critical disk failure occurs. 
1. Analyze the video and count the exact number of these red failure frames.
2. Write this integer count to `/home/user/failure_count.txt`.

**Part 2: Secure Manifest Ingestion (Adversarial Filter)**
Users upload manifest files (in various text encodings) that contain metadata. Some users are malicious and upload files designed to perform path traversal or exploit system paths.

Write an executable script at `/home/user/process_manifests` (in any language you prefer) that takes two arguments: an input directory and an output directory.
Usage: `/home/user/process_manifests <input_dir> <output_dir>`

Your script must do the following for every file in the `<input_dir>`:
1. Attempt to read the file. Detect its character encoding (which may be UTF-8, UTF-16, ISO-8859-1, or Shift-JIS) and convert its contents to valid UTF-8.
2. **Sanitize / Filter**: You must REJECT any file if its *decoded UTF-8 contents* or its *filename* contain:
   - Path traversal sequences (e.g., `../` or `..\`)
   - Null bytes (`\0`)
   - Absolute paths to sensitive Unix directories (`/etc/`, `/var/`, `/root/`)
3. **Approve**: If the file passes the filter, copy it to `<output_dir>` using the original filename, but ensure the written file is strictly UTF-8 encoded.
4. **Manifest**: For all approved files, generate a SHA256 manifest file at `<output_dir>/manifest.sha256` in standard `sha256sum` format.

Your script will be tested against a hidden adversarial corpus to ensure it perfectly distinguishes safe manifests from malicious payloads. 

Once your script is ready, ensure it is executable. You do not need to run it yourself on the hidden corpora; the automated testing framework will invoke `/home/user/process_manifests` to grade your solution.