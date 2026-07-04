You are a network security engineer tasked with securing a local multi-service application. 

In the `/app/` directory, there is a file upload system composed of three services:
1. **Nginx** (listening on port 8080) acting as a reverse proxy, configured via `/app/nginx.conf`.
2. **Flask Backend** (running on port 5000) handling the actual file uploads, located at `/app/app.py`.
3. **Redis** (running on port 6379) used for session tracking.

The Flask backend uses the `X-Upload-Filename` HTTP header to determine the name of the file being saved. Unfortunately, it is susceptible to path traversal attacks, allowing malicious actors to write files outside the intended `/app/uploads/` directory.

Your task is to:
1. Modify the Nginx configuration (`/app/nginx.conf`) to inspect the HTTP headers and automatically block any request where the `X-Upload-Filename` header contains path traversal sequences. Specifically, block any occurrence of `../` as well as its common URL-encoded variants (e.g., `%2e%2e%2f`, `..%2f`, `%2e%2e/` - case-insensitive).
2. Ensure that requests triggering this rule are rejected with an HTTP 403 Forbidden status code.
3. Ensure that benign requests (without traversal sequences) are still successfully passed to the Flask backend.
4. Apply the configuration changes so they are active on the running Nginx instance.

You may use Bash commands and any standard CLI tools to inspect the environment, test your rules, and restart the necessary services. 

An automated vulnerability scanner will evaluate your solution by sending a mix of benign and malicious HTTP requests to `http://localhost:8080/upload`. The test will measure the accuracy of your filtering. Ensure your configuration is robust.