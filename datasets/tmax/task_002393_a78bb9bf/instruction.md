You are an integration developer setting up a secure testing environment for a new set of APIs. The environment consists of a backend Node.js API, a native C library for secure hashing, and a Python reverse proxy that enforces rate limiting. 

Currently, the setup is broken and you need to fix the build sequence, compile the native code, and implement the reverse proxy from scratch.

Here are your tasks:

1. **Fix and Start the Node.js API**
   - The Node.js API is located in `/app/node_api/`.
   - Running `npm install` fails due to a conflicting peer dependency issue between `express` and a mock `auth-module`. 
   - Resolve the dependency conflict, install the packages, and start the service in the background. The service listens on `127.0.0.1:3001`. Do not modify `index.js`.

2. **Compile the Native Hashing Library**
   - A C file is provided at `/app/c_lib/hasher.c`.
   - Compile this into a shared object file named `/app/c_lib/libhasher.so`.
   - This library exposes a function `uint32_t hash_api_key(const char* key)` which you must use in your Python proxy.

3. **Develop the Python Reverse Proxy & Rate Limiter**
   - Create a Python script at `/app/proxy/proxy.py` and run it in the background.
   - **HTTP Reverse Proxy:** The proxy must listen on `0.0.0.0:8080`. It must forward all incoming HTTP GET requests to `http://127.0.0.1:3001`.
   - **Security / Rate Limiting Data Structure:** 
     - Every request to the proxy must include an `X-API-Key` HTTP header. If missing, return `401 Unauthorized`.
     - You must design a custom "Sliding Window" rate limit data structure in Python.
     - The limit is **5 requests per 10-second window** per API key.
     - Before checking the rate limit, the raw `X-API-Key` string must be hashed using the `hash_api_key` function from `/app/c_lib/libhasher.so`. Store the timestamps against the *hashed* key, not the raw key.
     - If the limit is exceeded, do not forward the request to the Node API. Instead, return a `429 Too Many Requests` status code.
   - **Admin TCP Protocol:** The Python proxy must also listen on `0.0.0.0:9000` with a raw TCP socket.
     - If it receives the exact string `FLUSH <hashed_key>\n` (where `<hashed_key>` is the numeric hash output), it must immediately clear all stored timestamps for that hashed key and respond with `OK\n`.

Ensure all three components (Node API, Python Proxy HTTP, Python Proxy Admin) are running and properly integrated.