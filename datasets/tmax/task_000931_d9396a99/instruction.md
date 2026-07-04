You are a release manager tasked with securing and preparing your deployment pipeline. The deployment infrastructure uses a microservices architecture to validate and sign deployment manifests before they are applied to the cluster.

Your environment is located at `/home/user/app/` and contains the following components:
1. **Redis**: Used for caching signed manifests.
2. **Rust gRPC Service (`/home/user/app/services/rust_signer`)**: A service that takes a valid protobuf deployment manifest and returns a cryptographic signature.
3. **Python Gateway (`/home/user/app/services/python_gateway`)**: A Flask web service that receives JSON manifests, sanitizes them, converts them to protobuf, calls the Rust gRPC service, and caches the signature in Redis.

However, the system is currently broken and incomplete. You need to perform the following steps to get it ready for production:

**1. Fix the Rust Service**
The Rust gRPC service has a borrow checker / ownership error in `/home/user/app/services/rust_signer/src/main.rs`. Debug and fix the Rust code so that it compiles successfully using `cargo build`.

**2. Protobuf Compilation**
You are provided with a protobuf definition at `/home/user/app/proto/manifest.proto`. Compile this protobuf file into Python bindings inside the `/home/user/app/services/python_gateway` directory so the gateway can communicate with the Rust service.

**3. Implement the Adversarial Sanitizer**
We frequently face malicious payload injections in deployment manifests. Implement a sanitizer module at `/home/user/app/services/python_gateway/sanitizer.py`. It must expose a function `def is_safe(manifest_dict: dict) -> bool`.
The function must recursively inspect the parsed JSON dictionary and return `False` (meaning "evil") if ANY string value contains any of the following restricted substrings:
- `&&`
- `|`
- `;`
- `$`
- `../`
If none of these are present anywhere in the values, return `True` (meaning "clean"). 

**4. Complete the Python Gateway API**
In `/home/user/app/services/python_gateway/app.py`, implement the `/validate` POST endpoint. 
- It should accept JSON.
- Pass the parsed JSON to `is_safe()`. If it returns `False`, respond with HTTP 400.
- If safe, convert the JSON data to the gRPC Protobuf request format, call the Rust gRPC service at `localhost:50051`.
- Cache the resulting signature in Redis (at `localhost:6379`) using the `app_name` as the key.
- Respond with HTTP 200 and the signature in JSON: `{"signature": "<sig>"}`.

**5. Service Integration**
A start script is provided at `/home/user/app/start.sh` which launches Redis, the Rust gRPC service, and the Python Gateway on port 8080.
Ensure all services can communicate. 

To verify your solution, the automated test suite will send a corpus of clean and evil JSON manifests to your Python Gateway's `/validate` endpoint.