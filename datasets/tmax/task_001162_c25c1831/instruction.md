You are a build engineer responsible for securing your team's internal gRPC-based build artifact caching service. Management wants to enable TLS for all internal gRPC traffic but is concerned about the performance overhead. 

Your task is to implement a prototype gRPC service, secure it with TLS, and benchmark the performance difference between plaintext and TLS endpoints.

Perform the following steps:
1. Create a Protocol Buffer definition file at `/home/user/artifact.proto`. It must define a `package build;` and a service named `ArtifactCache` with a single RPC method `GetChecksum`. The method should accept an `ArtifactRequest` (containing a `string filename`) and return an `ArtifactResponse` (containing a `string checksum`).
2. Generate a self-signed RSA (2048-bit) certificate and private key for `localhost`. Save them in `/home/user/certs/` as `server.crt` and `server.key`.
3. Implement and start a gRPC server (in the language of your choice) in the background. The server must:
   - Serve the `ArtifactCache` service.
   - Return the hardcoded string `"sha256:dummy"` for any `GetChecksum` request.
   - Listen on port `50051` for plaintext (insecure) connections.
   - Listen on port `50052` for TLS (secure) connections using the generated certificates.
4. Benchmark both endpoints. Send exactly 1000 requests to the plaintext port and 1000 requests to the TLS port (you may write a simple client script to measure the total time taken for 1000 sequential requests and calculate Requests Per Second, or install/use a benchmarking tool).
5. Calculate the performance overhead and write the results to `/home/user/tls_overhead.json` exactly in this format:
   ```json
   {
     "plaintext_rps": 1500.5,
     "tls_rps": 1200.2,
     "overhead_percentage": 20.01
   }
   ```
   *(Note: `overhead_percentage` is calculated as `((plaintext_rps - tls_rps) / plaintext_rps) * 100`. The actual numbers will depend on your system's performance.)*

Keep the server running in the background when you complete your turn so the endpoints can be verified.