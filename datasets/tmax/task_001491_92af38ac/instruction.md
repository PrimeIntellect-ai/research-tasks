We are migrating an old internal text-processing pipeline to a new microservice architecture. However, the core logic was originally written in a proprietary C application, of which we only have a stripped binary oracle left (`/opt/oracle/decoder_oracle`).

Your task is to recreate this C utility and integrate it into our new service stack.

**Part 1: The C Utility (`decoder.c`)**
Create a C program at `/home/user/decoder.c` that takes exactly one command-line argument: a custom routing URL.
The URL format is: `patch://<target_file_id>/<encoded_patch_string>`
1. `<target_file_id>` is a single uppercase letter (A-Z).
2. `<encoded_patch_string>` is a URL-encoded, Base64 string.
   
The program must:
1. Parse the URL (you must implement a state machine to parse the `patch://` protocol and extract the components).
2. URL-decode the `<encoded_patch_string>`.
3. Base64-decode the result to get a binary patch sequence.
4. Apply the patch sequence to an initial empty string buffer. The patch sequence consists of 2-byte commands:
   - `I<char>`: Insert `<char>` at the end of the buffer.
   - `D\x00`: Delete the last character (if buffer is not empty).
   - `R<char>`: Replace the last character with `<char>` (do nothing if empty).
5. Print the final result to standard output in the exact format: `TARGET=[target_file_id] RESULT=[patched_string]` and exit with 0.

Write a `Makefile` at `/home/user/Makefile` to compile this into an executable named `decoder`. It must statically link standard libraries if necessary, but GCC is available.

**Part 2: Service Integration**
We have three services that must be glued together to form the pipeline:
1. Nginx (runs on port 8080)
2. A Python Flask backend app (`/app/backend.py`, runs on port 5000)
3. Redis (runs on port 6379)

A startup script `/app/start.sh` exists but the Nginx configuration `/etc/nginx/nginx.conf` and Flask configuration `/app/config.json` are broken. 
1. Fix the Nginx config so that any HTTP GET request to Nginx on `http://localhost:8080/process/<url_remainder>` proxies to the Flask app at `http://127.0.0.1:5000/process/<url_remainder>`.
2. Modify `/app/backend.py` (which currently just returns 200 OK) so that it takes the `<url_remainder>`, prepends `patch://`, calls your compiled `/home/user/decoder` utility via a subprocess, reads the stdout, and saves the literal stdout string into Redis (using `redis` python package, connecting to `localhost:6379`) under the key `latest_patch`. It should then return the stdout string as the HTTP response.

Ensure you start the services using `/app/start.sh` to test your end-to-end flow.