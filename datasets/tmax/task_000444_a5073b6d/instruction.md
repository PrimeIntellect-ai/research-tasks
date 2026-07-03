You are a QA engineer tasked with setting up a mock API environment to test client applications. The environment requires a custom rate-limiting REST API written in Bash, and a helper binary compiled from a provided CMake project.

Here are your specific requirements:

1. **Extract Authentication Token from Audio:**
   You have been provided an audio artifact at `/app/system_auth.mp3`. The secret Bearer token for the API is hidden in the audio file's metadata (specifically, the 'title' tag). Extract this token. You may use tools like `ffprobe` or `exiftool`.

2. **Fix and Build the Helper Tool:**
   There is a C project located at `/home/user/helper_tool`. It is designed to evaluate properties of incoming request payloads. 
   Currently, running `cmake . && make` fails at link time because it cannot find the shared math library (`libm`). 
   Fix the `CMakeLists.txt` to correctly link the math library, and compile the tool. The resulting binary should be located at `/home/user/helper_tool/payload_eval`.

3. **Develop the Bash REST API:**
   Write a Bash script named `/home/user/server.sh` that implements an HTTP server. You should use `socat` to listen on `127.0.0.1:8080`.
   The API must handle `POST /submit` requests and enforce the following rules:
   - **Authentication:** Must include the header `Authorization: Bearer <TOKEN>` (using the token extracted from the MP3). Return `HTTP/1.1 401 Unauthorized` if missing or incorrect.
   - **Validation:** Must read the request body and pass it via standard input to the compiled `/home/user/helper_tool/payload_eval` binary. If the binary exits with a non-zero status, return `HTTP/1.1 400 Bad Request`.
   - **Rate Limiting:** Implement a simple rate limit of a maximum of 3 successful requests per 10-second window. If a client exceeds this, return `HTTP/1.1 429 Too Many Requests`. State can be maintained using temporary files in `/tmp/api_state/`.
   - **Success:** If all checks pass, return `HTTP/1.1 200 OK`.

4. **Start the API:**
   Run your `server.sh` in the background so that it listens on `127.0.0.1:8080`. Keep it running. An automated test suite will send real HTTP protocol requests to verify authentication, rate limiting, and request validation properties.