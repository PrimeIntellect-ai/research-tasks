You are a backup operator performing an automated testing restore drill. Your team receives restoration directives as scanned image files.

You must build an automated Python-based recovery verification service that processes a provided image directive, extracts the backup archive, formats the disk configuration, and serves the results over HTTP for the automated verification suite to validate.

Here are the specific steps to complete the drill:

1. **Process the Restore Directive Image:**
   There is an image file located at `/app/restore_directive.png`. Use OCR (e.g., `tesseract`, which is installed on the system) to read the text. The image contains three critical pieces of information:
   - The path to a backup archive (`Archive: <path>`)
   - A recovery token (`RecoveryKey: <token>`)
   - The port number the verification service must listen on (`ServerPort: <port>`)

2. **Extract and Process Backup Logs:**
   Extract the `.tar.gz` archive specified in the image. Inside, you will find a file named `disk_info.log`. 
   This file contains raw string dumps of disk configuration in the format:
   `Device: <device>, Mountpoint: <mountpoint>, Type: <type>, Options: <options>`
   
   Using text processing pipelines (like `awk`, `sed`, or `grep` invoked via shell or subprocess), convert this line into a standard Linux `fstab` format string with a dump frequency of `0` and a pass number of `2`.
   For example, it should be formatted exactly as:
   `<device> <mountpoint> <type> <options> 0 2`
   Save this single line to `/app/parsed_fstab.conf`.

3. **Deploy the Verification Service:**
   Write and run a Python HTTP server (you may use `Flask`, `FastAPI`, or the standard `http.server` module) that listens on `127.0.0.1` using the port extracted from the image directive.
   
   The server must implement the following `GET` endpoints:
   - `/health`: Returns an `application/json` response with the body `{"status": "ok"}`
   - `/key`: Returns a `text/plain` response containing exactly the `<token>` extracted from the image.
   - `/fstab`: Returns a `text/plain` response containing exactly the formatted fstab string.

Keep the Python server running so the automated test suite can query it to verify your restore drill.