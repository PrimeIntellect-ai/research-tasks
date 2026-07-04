You are an engineer tasked with porting a legacy high-performance mathematical evaluation tool into a modern, minimal containerized microservice architecture. The tool evaluates complex polynomial structures and is written in C. We are wrapping it in a Python-based REST API mesh. 

Currently, the system is partially set up in `/home/user/app/`. There are three cooperating services:
1. **Nginx** (Reverse Proxy) - Should listen on port 8080.
2. **Gateway Service** (Python/Flask) - Should listen on port 5000. Handles URL routing, deserialization, and request sanitization.
3. **Compute Engine** (Python/C FFI) - Should listen on port 5001. Handles the actual mathematical execution.

Your goal is to complete the system implementation, fix the configuration, and ensure the pipeline is secure against algorithmic complexity attacks.

### Step 1: Multi-Service Configuration
- Configure Nginx. We have provided a skeleton configuration at `/etc/nginx/sites-available/math-app`. Modify it so that all requests to `http://127.0.0.1:8080/` are proxied to the Gateway Service at `127.0.0.1:5000`. Enable this site and restart Nginx.
- Start the Gateway Service and the Compute Engine. The startup script `/home/user/app/start_services.sh` is provided, but you must ensure the services communicate properly. The Gateway Service uses the `ENGINE_URL` environment variable to locate the Compute Engine. Set this variable to `http://127.0.0.1:5001` before starting the gateway.

### Step 2: C-FFI Integration in the Compute Engine
The Compute Engine relies on a compiled C library (`/home/user/app/compute/libpoly.so`).
- Edit `/home/user/app/compute/engine.py`.
- Complete the `ctypes` bindings for the function `double evaluate_polynomial(double* coefficients, int degree, double x);`.
- Ensure the API route `/compute` successfully deserializes the incoming JSON array of coefficients, calls the C library, and returns the float result.

### Step 3: Adversarial Payload Sanitizer
We are facing denial-of-service attacks via deeply nested JSON math structures or excessively large matrices. 
- You must implement a sanitizer module at `/home/user/app/gateway/sanitizer.py`.
- It must contain a function with the signature: `def is_safe_payload(json_payload: str) -> bool`.
- **Validation Rules**:
  1. The JSON must deserialize into a custom data structure representing a math AST.
  2. A payload is "evil" (return `False`) if the AST nesting depth exceeds `10`.
  3. A payload is "evil" if any `matrix` type node has dimensions exceeding `100x100`.
  4. Otherwise, the payload is "clean" (return `True`).
- We have provided two corpora of payloads at `/home/user/app/corpora/clean/` and `/home/user/app/corpora/evil/`. 
- An automated verifier will load your `is_safe_payload` function and test it against these corpora. You must achieve **100% rejection of the evil corpus AND 100% acceptance of the clean corpus**.

### Step 4: End-to-End Routing
- Edit `/home/user/app/gateway/app.py`.
- Implement the route `/api/v1/evaluate/<poly_id>`. It must parse the URL parameter `poly_id`, extract the query parameter `x` (float), read the raw JSON body, and pass it through your `sanitizer.is_safe_payload()`. 
- If unsafe, return HTTP 400. If safe, extract the `coefficients` array from the JSON structure, serialize it, and forward it to the Compute Engine. Return the final result.

Ensure the full pipeline works. You can test it by sending a POST request to `http://127.0.0.1:8080/api/v1/evaluate/test?x=2.5` with a valid JSON payload.