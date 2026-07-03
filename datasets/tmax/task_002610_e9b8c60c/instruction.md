You are an integration developer setting up a local API testing environment. We have a backend authentication microservice written in C that handles API tokens. It is fronted by an Nginx reverse proxy. 

Currently, the C project is broken, fails to compile, has memory safety issues, and is missing key functionality. Your task is to fix the application, complete its implementation, configure the reverse proxy, and test the integration.

The project is located in `/home/user/auth_service`.

**Step 1: Fix the Build (Makefile linking error)**
If you run `make` in `/home/user/auth_service`, it will fail. Fix the `Makefile` so that:
1. It successfully links all object files (you will need to ensure `ds.c` and `math_utils.c` are compiled and linked).
2. It links the math library (needed for the numerical algorithm).

**Step 2: Fix the Memory Safety Bug**
In `main.c`, the function `process_request(const char* http_payload)` reads an HTTP request and extracts the `X-API-Token` header. There is a severe buffer overflow vulnerability (Undefined Behavior) caused by an unsafe copy into a fixed-size buffer. 
Fix this function so it safely handles tokens up to 128 characters long without overflowing, truncating gracefully if necessary, and ensuring null-termination.

**Step 3: Implement the Numerical Algorithm**
In `math_utils.c`, implement the function `double compute_token_variance(const char* token)`.
This function must calculate the population variance of the ASCII values of the characters in the token string. 
For a token of length N, let mu be the mean of the ASCII values. The population variance is the sum of `(ascii_val - mu)^2` for each character, divided by N. 
Return 0.0 if the token is empty.

**Step 4: Implement the Custom Data Structure**
In `ds.c`, implement a simple Fixed-Size Hash Set to store previously seen tokens and detect replay attacks.
Complete the functions:
- `void init_set()`: Initializes the set (size 256).
- `int insert_and_check(const char* token)`: Hashes the token using a simple sum of ASCII characters modulo 256. If the token exists at that index (resolving collisions using linear probing), return `1` (replay detected). Otherwise, insert it and return `0` (new token).

**Step 5: Configure the Reverse Proxy**
There is an Nginx configuration file template at `/home/user/auth_service/nginx.conf`. 
Edit it to configure a reverse proxy that listens on port `8080` and forwards requests for the `/api/auth` endpoint to the C backend running on `127.0.0.1:9000`.
Start Nginx using this specific configuration file as the user (do not use sudo):
`nginx -c /home/user/auth_service/nginx.conf -p /home/user/auth_service/`

**Step 6: Run and Test**
1. Start the compiled C backend `auth_server` in the background (it listens on port 9000).
2. Send an HTTP POST request to `http://127.0.0.1:8080/api/auth` with the header `X-API-Token: SECRET123`.
3. Send a second HTTP POST request with the exact same header to test the replay attack detection.

To allow automated verification of your success, the C backend writes its output to `/home/user/auth_service/auth.log`. Ensure the backend is running, the proxy passes the traffic correctly, and the log file shows the processed requests, the calculated variance, and the replay detection.