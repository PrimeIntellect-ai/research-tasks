You are an IT support technician responding to an urgent ticket. Our newly deployed Rust-based authentication service is failing, and the original developer is unreachable. 

You are provided with a multi-service setup located in `/app/auth-service`. The system consists of a local Redis instance and the Rust API server. 

Here are the issues reported in the ticket:
1. **Lost Secret:** The service requires a `SECRET_API_KEY` environment variable to start. It used to be hardcoded in the source code but was recently removed. However, we suspect the secret can still be recovered from the local Git repository's history in `/app/auth-service`. Find the secret and put it in a `/app/auth-service/.env` file in the format `SECRET_API_KEY=your_found_secret`.
2. **Crash on Edge Cases:** The Rust API server (using `axum`) has an endpoint `/api/v1/auth` that accepts POST requests with a JSON body. Recently, the service has been panicking and creating core dumps when the `payload` field contains unpadded Base64 strings, or when the `client_id` field is missing. You need to fix the Rust code in `/app/auth-service/src/main.rs` to handle these parsing edge-cases gracefully (returning a 400 Bad Request instead of panicking).
3. **Encoding Bug:** The Base64 decoded payload sometimes contains non-UTF8 bytes, which causes another `.unwrap()` panic during string conversion. Fix this so it replaces invalid sequences with the Unicode replacement character rather than crashing.

Your tasks:
1. Recover the secret and set up the `.env` file.
2. Fix the panics in `/app/auth-service/src/main.rs`.
3. Start the Redis server in the background using `redis-server --port 6380 --daemonize yes`.
4. Compile and run the Rust service. It is configured to listen on `127.0.0.1:8080`. Leave it running in the background.

The automated verification will test the `/api/v1/auth` endpoint over HTTP with various edge-case payloads to ensure it no longer crashes and correctly returns 200 OK for valid payloads and 400 Bad Request for malformed ones.