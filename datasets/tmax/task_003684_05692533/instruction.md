You are an open-source maintainer reviewing a broken Pull Request for a testing utility repository located at `/app/test-util`. 

The contributor tried to package our bash-based mock server into a Python package, but the build is broken and the server implementation is incomplete. 

Your task is to fix the PR and bring up the test server:

1. **Fix the Python Package:** The file `/app/test-util/setup.py` has a syntax error or misconfiguration preventing installation. Fix it so that running `pip install .` inside `/app/test-util` completes successfully.

2. **Extract Configuration:** We use a visual configuration scheme for our integration tests. Read the image fixture located at `/app/server_config.png`. You will need to use OCR (e.g., `tesseract`) to extract two pieces of information from it:
   - The listening **Port**
   - The secret **Auth Token**

3. **Implement the Bash Server:** Edit the script at `/app/test-util/server.sh`. You must write a simple HTTP server entirely in Bash (you may use tools like `nc` or `socat` which are available on the system). 
   - The server must listen on `127.0.0.1` on the Port extracted from the image.
   - It must handle `GET /verify` requests.
   - It must check for the HTTP header `Authorization: Bearer <Auth Token>` (using the exact token extracted from the image).
   - If the authorization is correct, the server must respond with a `200 OK` status and the HTTP response body must be exactly the SHA256 checksum of the Auth Token string (just the hex hash, no trailing spaces or hyphens).
   - If the authorization is missing or incorrect, it should return a `401 Unauthorized`.

4. **Run the Server:** Once implemented, start the server in the background so it is actively listening for incoming connections. 

Leave the server running in the background when you are finished. Automated tests will send real HTTP requests to the port you extracted to verify the protocol handling and checksum logic.