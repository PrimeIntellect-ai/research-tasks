You are tasked with recovering the directory structure and priority order of a corrupted software project. The only surviving metadata about the project's organization is stored in a video artifact containing QR codes flashed on screen.

We have placed this video at `/app/recovery.mp4`. 

Your objectives:
1. **Extract and Decode**: Use `ffmpeg` to extract frames from `/app/recovery.mp4`. Use `zbarimg` to read the QR codes from these frames. Each QR code contains a JSON payload with a file path and a mathematical expression representing its load priority, for example: `{"path": "/home/user/project/src/main.c", "expr": "5 * 3 + 2"}`.
2. **Evaluate and Sort**: Parse the JSON payloads. Evaluate the mathematical expression for each file to determine its integer priority score. Create a plain text file at `/home/user/ordered_files.txt` where each line is formatted as `[priority] [path]`, sorted by priority in strictly descending numerical order.
3. **Diff**: Compare your extracted list of paths (ignoring the priority number) with an existing file at `/home/user/legacy_order.txt`. Save the diff (using standard `diff -u` format) to `/home/user/order_diff.patch`.
4. **Serve (Multi-Protocol)**: Create and run a pure Bash TCP service (using `nc`, `socat`, or bash `/dev/tcp` built-ins) listening on `127.0.0.1:9000`. 
   - The service must accept plain-text TCP connections.
   - When the client sends a line starting with `QUERY ` followed by a math expression (e.g., `QUERY 10+7`), your server must evaluate that expression (e.g., to `17`), look up the file path associated with that priority score from your extracted data, and respond with the absolute file path followed by a newline.
   - If the priority doesn't exist, respond with `NOT_FOUND`.
   - The server must stay alive to handle multiple sequential requests.

Do not use Python, Node.js, or other scripting languages for the server; you must use Bash and standard CLI utilities (like `jq`, `bc`, `awk`, `sort`, `ffmpeg`, `zbarimg`, `nc`).