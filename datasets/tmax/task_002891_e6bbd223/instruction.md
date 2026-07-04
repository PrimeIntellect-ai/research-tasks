You are a deployment engineer tasked with rolling out a new staged routing proxy. Your team has provided the configuration for the new rollout, but it was sent as an architectural diagram image rather than a text file.

You must build and deploy the service based on the parameters hidden in the image.

Step 1: Extract Configuration
There is an image file located at `/app/architecture.png`. Use OCR (e.g., `tesseract`) to extract the text from this image. 
The image contains four key pieces of information:
- The version string
- The "Proxy Port" (where your service must listen)
- The "Route to" address (the upstream target)
- The "Secret Key" (used for authentication)

Step 2: Create the Proxy Service
Using Python and Bash, create a multi-language deployment. 
Write a Python HTTP server script at `/home/user/proxy.py` that implements the following:
- Listens on `127.0.0.1` at the "Proxy Port" extracted from the image.
- Expects an HTTP GET request.
- Checks for an HTTP header named `X-Deploy-Auth`. 
- If the header value does NOT exactly match the "Secret Key" from the image, respond with HTTP 401 Unauthorized.
- If the header is correct, respond with HTTP 200 OK and a JSON payload exactly matching this format: `{"status": "routed", "upstream": "<extracted Route to address>"}`.
- Every request (regardless of auth success) must be appended to `/home/user/access.log` in this exact format:
  `[YYYY-MM-DD HH:MM:SS] | X-Deploy-Auth: <header_value_or_NONE> | Path: <request_path>`

Step 3: Log Configuration and Rotation
Write a bash script at `/home/user/deploy.sh` that:
1. Starts the Python proxy service in the background.
2. Implements a continuous log rotation loop (using bash built-ins or standard tools, running in the background). 
3. The log rotation must check `/home/user/access.log` every 2 seconds. If the log file exceeds 5 lines, it must rename the file to `/home/user/archive/access.log.1` (creating the `/home/user/archive` directory if it doesn't exist), shift any older logs up to `.3` (e.g., `.2` becomes `.3`), and create a fresh `access.log`.

Step 4: Execution
Run your `/home/user/deploy.sh` script so that the proxy is actively listening and the log rotation daemon is running in the background. Leave these processes running. Do not exit the proxy.