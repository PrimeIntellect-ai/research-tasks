You are a Linux Systems Engineer tasked with hardening and fixing a local deployment configuration. 

Currently, our local NGINX reverse proxy is returning 502 Bad Gateway errors because it is configured with the wrong upstream socket path for the backend application. 

Here is your task:
1. We have a screenshot of the legacy deployment dashboard located at `/app/legacy_dashboard.png`. Use an OCR tool (like `tesseract`, which is preinstalled) to extract the text from this image. Somewhere in the extracted text, you will find the correct Unix socket path for the upstream application (e.g., `unix:/path/to/socket.sock`).
2. Update the local NGINX configuration file at `/home/user/nginx.conf`. Replace the incorrect `proxy_pass` directive in the `location /` block with the correct socket path extracted from the image. 
3. Write a robust Python CI/CD validation script at `/home/user/ci_test.py`. This script must do the following:
   - Start the backend application by running the provided script `/app/backend.py <EXTRACTED_SOCKET_PATH>` as a background subprocess.
   - Start NGINX locally using your updated config as a background subprocess: `nginx -c /home/user/nginx.conf -g 'daemon off;'`.
   - Implement a robust polling mechanism (with error handling and timeouts) to wait for NGINX to start listening on `127.0.0.1:8080`.
   - Send 50 HTTP GET requests to `http://127.0.0.1:8080/health`.
   - Calculate the success rate (number of HTTP 200 responses / 50).
   - Print ONLY the success rate as a float (e.g., `1.0` or `0.98`) to standard output.
   - Gracefully terminate both the backend and NGINX processes before exiting.

Ensure your Python script is robust, handles potential network errors gracefully, and outputs only the final float value, as it will be used by our automated metric tracking system.