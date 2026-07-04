You are tasked with fixing a broken web application stack and restoring its backend processor.

Currently, an Nginx instance configured in `/home/user/nginx/` is supposed to serve requests, but users are reporting a "502 Bad Gateway" error when accessing the backend processor. The previous administrator accidentally deleted the source code and the compiled binary of the FastCGI backend! 

Your task is to recreate the backend processor in C, fix the Nginx configuration, and set up proper log management.

Here are your objectives:
1. **Recreate the Backend Processor (C Language):**
   We have a backup of the design spec in an image at `/app/token_spec.png`. Use an OCR tool (like `tesseract`, which is installed) to extract the secret authentication token from this image.
   Write a C program at `/home/user/src/processor.c` and compile it to the executable `/home/user/bin/processor`.
   The program must:
   - Accept exactly one command-line argument (a string).
   - Reverse the characters of the provided string.
   - Print the result to standard output exactly in this format, followed by a newline:
     `PROCESSED: <reversed_string> | AUTH: <extracted_token>`
   *(For example, if the token was "BETA", `./processor hello` should output `PROCESSED: olleh | AUTH: BETA`)*

2. **Fix the Nginx Configuration:**
   The configuration file is located at `/home/user/nginx/conf/nginx.conf`. It contains a typo in the `fastcgi_pass` directive for the `/process` location, causing the 502 error. Update it to point to `127.0.0.1:9000`, which is where our FastCGI wrapper is expected to run.

3. **Configure Log Rotation:**
   The Nginx access logs at `/home/user/nginx/logs/access.log` are growing too large. Create a logrotate configuration file at `/home/user/logrotate.conf` that will rotate all `.log` files in `/home/user/nginx/logs/`. Configure it to:
   - Rotate daily.
   - Keep 7 days of backlogs.
   - Compress old log files.
   - Missing log files should not produce an error.

Ensure the C program is compiled without errors and is fully functional, as it will be strictly tested against a reference implementation with automated fuzzing.