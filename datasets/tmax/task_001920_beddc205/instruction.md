You are an open-source maintainer reviewing a broken Pull Request for a lightweight, C-based Web Application Firewall (WAF) named `MiniWAF`. The PR introduces a new HTTP request filtering engine, but the author left it in a broken state. 

Your task is to fix the build, patch a critical memory safety vulnerability in the parser, extract a hardcoded initialization token left only in a PR screenshot, and write a Bash orchestration script to serve it.

Here are the specific requirements:

1. **Extract the Admin Token (Vision/OCR):**
   The PR author forgot to document the test environment's admin token, but accidentally included a screenshot of their terminal in the PR assets at `/app/pr_assets/token.png`. 
   Use `tesseract` (which is pre-installed) to read the text from this image. The image contains a single alphanumeric token. Save the exact extracted token (stripping any surrounding whitespace/newlines) to `/home/user/admin_token.txt`.

2. **Fix the Build System (CMake Link Error):**
   The source code is located in `/home/user/miniwaf`. 
   Currently, running `cmake . && make` fails at the linking stage because the main executable cannot find the shared library `libhttp_parser.so`. 
   Modify the `CMakeLists.txt` file to correctly link the `http_parser` library to the `miniwaf_server` target so that the build succeeds.

3. **Fix the Memory Safety Issue (C/C++):**
   The PR introduces a custom state-machine parser in `/home/user/miniwaf/src/parser.c`. There is a critical memory safety bug (buffer overflow) when parsing HTTP header values that exceed 128 bytes. 
   Identify the unsafe string copying function in `parser.c` and replace it with a bounds-checked equivalent to prevent segmentation faults on long headers. The parser should safely truncate or reject headers larger than the buffer size without crashing.

4. **Bash Orchestration:**
   Write a Bash script at `/home/user/start_waf.sh` that does the following:
   - Builds the `miniwaf` project from scratch.
   - Reads the token from `/home/user/admin_token.txt`.
   - Starts the `miniwaf_server` binary, binding it to listen on `127.0.0.1` port `8080`.
   - The server binary takes the admin token as its first command-line argument: `./miniwaf_server <TOKEN>`
   - The script must leave the server running in the background or foreground (ensure it stays running so it can process requests).

The server, once correctly compiled and running, expects raw HTTP/1.1 requests. Make sure it is up and running when you consider the task complete. Automated tests will verify the server's behaviour over the network.