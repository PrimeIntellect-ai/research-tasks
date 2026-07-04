You are a mobile build engineer maintaining the CI pipelines for a C++ Android application. Recently, a bad commit caused our CMake project to fail at link time because it can't find a shared library. 

Our pipeline receives automated code patches via a local WebSocket broadcast before they are merged. 
A WebSocket server script has been provided at `/home/user/ws_server.py`. 

Your task is to:
1. Start the WebSocket server in the background: `python3 /home/user/ws_server.py &` (It listens on `ws://127.0.0.1:9753`).
2. Write a Bash script (you may use Python for the WebSocket connection part if needed, as `websockets` is installed) to connect to `ws://127.0.0.1:9753`.
3. The server will send a single text payload containing multiple concatenated Unified Diffs, and then close the connection.
4. Process this payload:
   - Identify and **remove** the diff that modifies `CMakeLists.txt` and removes the linking of the `native_camera` library (look for the removed line containing `native_camera`).
   - Keep all other diffs.
   - **Sort** the remaining valid diffs alphabetically based on their target file path (the file listed in the `+++ b/...` line).
5. Output the final, sorted, concatenated unified diffs to exactly `/home/user/final_pipeline.patch`. 

Ensure the diffs in the final file are properly separated (exactly as they were formatted individually) but sorted by the target filename.