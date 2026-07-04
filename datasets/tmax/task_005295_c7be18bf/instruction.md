You are a QA engineer tasked with setting up a legacy test environment. Our frontend test suite fails to run because it depends on a legacy backend service that was recently decommissioned. We need you to build a lightweight mock service in Python to unblock the testing pipeline. 

Unfortunately, the original documentation is lost. The only remaining specification is an architectural diagram saved as an image at `/app/system_diagram.png`. 

Your objectives are:

1. **Extract Specifications**: Analyze the image `/app/system_diagram.png` (using OCR tools like `tesseract` which are installed) to determine:
   - The required SQLite database schema and table name.
   - The specific character encoding that the HTTP responses must use.
   - The ports for the HTTP and TCP services.

2. **Schema Migration & Data Setup**:
   - Create an SQLite database at `/app/legacy.db`.
   - Apply the schema migration extracted from the image.
   - Insert exactly one mock user record into the table: ID `1`, name `mötley_user`, and role `admin`.

3. **Polyglot Build**:
   - We have recovered the original C-based token generation algorithm at `/app/legacy_hash.c`.
   - Compile this C file into a shared library (`/app/legacy_hash.so`) using standard tools (`gcc`).
   - The Python mock server must load this library and use its `generate_token(int id)` function to generate authorization tokens.

4. **Service Implementation (Python)**:
   - Write and start a Python server (e.g., `/app/mock_server.py`) that implements two protocols based on the extracted specs:
     - **HTTP Service**: Listen on the HTTP port specified in the image. An HTTP GET request to `/user/1` must query the SQLite database, format the response as `id,name,role` (e.g., `1,mötley_user,admin`), and encode the HTTP response body strictly in the legacy character encoding specified in the image.
     - **Raw TCP Service**: Listen on the TCP port specified in the image. When a client connects and sends the exact string `TOKEN 1\n`, the server must call the compiled C library's `generate_token(1)` function and return the resulting integer as a string followed by a newline over the TCP socket.

Start your server in the background so it remains running. The automated test suite will verify the environment by sending actual HTTP and TCP requests to your mock service and checking the binary encoding of the responses.