You are a mobile build engineer maintaining a secure artifact release pipeline. Our build system uses a unique mechanism to derive cryptographic signing keys directly from automated UI test artifacts to ensure that only builds passing the UI tests can be signed. 

Your task is to implement the build signature generator, wrap it in a lightweight Bash REST API, and configure a reverse proxy.

**Step 1: Extract the Secret Key from Video**
During the mobile UI test, the screen goes completely black at specific intervals. The exact number of black frames in the video `/app/ui_test.mp4` serves as the `SECRET_KEY`. 
- A frame is considered "black" if at least 98% of its pixels are below a luminance threshold of 32. You have `ffmpeg` installed to analyze this. 
- Find this count and use it as `SECRET_KEY` in the next step.

**Step 2: Implement the Checksum & Signature Logic**
Write a Bash script at `/home/user/sign_build.sh` that takes exactly one argument (a build ID string, consisting of alphanumeric characters) and prints a specific checksum signature to standard output. 
The signature must be generated as follows:
1. Initialize an empty result string.
2. For each character in the input string, get its ASCII decimal value.
3. Apply an XOR operation between the ASCII value and your `SECRET_KEY`.
4. Convert the result to a 2-digit uppercase Hexadecimal string and append it to the result string.
5. Error-correcting parity: Calculate the XOR sum of all the *original* ASCII values of the input string. Convert this single parity value to a 2-digit uppercase Hexadecimal string and append it to the very end of the result string.

Example: If `SECRET_KEY` is 10, and input is "A" (ASCII 65): 
65 XOR 10 = 75 (Hex 4B). Parity is 65 (Hex 41). Output: `4B41`.

**Step 3: REST API Construction**
Write a Bash script at `/home/user/api.sh` that acts as a basic HTTP server using `nc` (netcat) listening on port `9090`. 
It must continuously listen for incoming connections, parse `GET /sign?build_id=<string> HTTP/1.1` requests, and respond with HTTP 200 OK and a JSON body: `{"signature": "<output_of_sign_build.sh>"}`.

**Step 4: Reverse Proxy Configuration**
Install and configure `nginx` to act as a reverse proxy.
Modify the default Nginx configuration (`/etc/nginx/sites-available/default`) to listen on port `8080`.
All requests to `/api/` should be reverse-proxied to your Bash API at `http://127.0.0.1:9090/`. (e.g., `GET /api/sign?build_id=XYZ` forwards to `GET /sign?build_id=XYZ`).

Ensure both your `api.sh` is running and Nginx is started when you declare the task finished. The automated verifier will strictly test the exact bit-level output of `/home/user/sign_build.sh` against millions of random inputs using an oracle.