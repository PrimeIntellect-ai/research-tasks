You are a developer tasked with organizing project files and debugging a legacy media processing pipeline. 

We have a video recording of a failed build process located at `/app/build_capture.mp4`. We also have the project's dependency graph located at `/home/user/project/deps.txt` (format: `module: dependency1 dependency2 ...`).

Your task is to write a comprehensive Bash-centric workflow to analyze the failure, trace the dependency graph, and expose the results via a WebSocket server for our automated test suite.

Perform the following steps:
1. **Video Analysis**: Use `ffmpeg` and OCR (like `tesseract`, preinstalled) to extract frames from `/app/build_capture.mp4`. Locate the exact frame number (1-based index) containing the text "CORRUPTION_DETECTED: <module_name>". Note the corrupted module.
2. **Graph Traversal**: Write a Bash script (`/home/user/organize.sh`) that reads `/home/user/project/deps.txt` and performs a graph traversal to find ALL downstream dependencies (recursive) of the corrupted module.
3. **Sorting and Diffing**: Sort the resulting impacted dependencies alphabetically and deduplicate them. 
4. **Numerical Checksum**: In your Bash script, implement a numerical checksum: concatenate the deduplicated dependency names into a single continuous string, and calculate the sum of the ASCII decimal values of all characters in that string.
5. **WebSocket Integration**: Bring up a WebSocket server listening on `0.0.0.0:8081`. You may use `websocat` (preinstalled), a Python wrapper, or pure bash with `socat`, provided the core logic remains in Bash. 
   - The server must accept WebSocket connections (RFC 6455) without authentication.
   - When the client sends the text payload `GET_REPORT`, the server must respond with a strict JSON string:
     `{"corrupt_frame": <frame_number>, "corrupt_module": "<module_name>", "impacted_deps": ["dep1", "dep2", ...], "ascii_sum": <sum>}`
   - The server must remain running in the background.

Ensure your scripts handle edge cases in graph traversal (e.g., circular dependencies) and that the JSON output strictly matches the required keys and types.