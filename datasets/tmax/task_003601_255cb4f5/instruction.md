You are a QA engineer tasked with setting up a local test environment for a C++ numerical computation service. The service parses JSON arrays, computes the sum, and returns a Base64-encoded JSON response. 

Currently, the automated CI pipeline fails because the C++ project cannot find a required shared library (`libencode.so`) during the build and execution phases, and the reverse proxy isn't routing requests correctly.

Your workspace is located at `/home/user/qa_env`.

Here is what you need to do:

1. **Fix the CMake configuration**:
   The project is in `/home/user/qa_env/backend`. It fails to link against `libencode.so` (located in `/home/user/qa_env/backend/lib`). Modify `/home/user/qa_env/backend/CMakeLists.txt` so that the `num_service` executable successfully links against this library. Also, ensure that the compiled executable can find the shared library at runtime *without* requiring the user to manually export `LD_LIBRARY_PATH`.

2. **Configure the Reverse Proxy**:
   Complete the Nginx configuration file located at `/home/user/qa_env/nginx.conf`. You must configure the `server` block listening on port `8080` so that any requests to the `/api` endpoint are reverse-proxied to `http://127.0.0.1:9000`. Keep the rest of the configuration intact, as it is designed to run Nginx without root privileges.

3. **Deploy and Test**:
   - Compile the C++ service by running the provided CI script: `/home/user/qa_env/build_and_serve.sh`. This script will build the project and start a `socat` listener on port `9000` that passes incoming HTTP bodies to your C++ executable. Keep this running in the background.
   - Start Nginx using the fixed configuration: `nginx -c /home/user/qa_env/nginx.conf`
   - Send an HTTP POST request to `http://127.0.0.1:8080/api` with the following raw JSON body:
     `{"data": [10.5, 20.0, -5.2, 14.7]}`
   - The server will respond with a Base64-encoded string. Save *only* this exact Base64 string to a file named `/home/user/qa_env/result.txt`.

Ensure all background processes are running when you test, but you do not need to leave them running permanently after you have saved `result.txt`.