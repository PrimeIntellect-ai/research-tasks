You are a web developer working on a backend character-encoding microservice. The service receives raw text strings via gRPC and returns a processed, encoded string. This microservice is a critical bottleneck in our architecture, so we are migrating it from a legacy script to a high-performance C++ service.

Currently, the C++ project in `/home/user/encoder_service/` has a few severe issues:
1. **Build Failure:** The `Makefile` has a linking error. The object files are not being linked correctly against the gRPC and Protobuf libraries.
2. **Missing Logic:** The `Encode` RPC method in `server.cpp` is supposed to perform a Custom Run-Length Encoding (RLE) followed by standard Base64 encoding. The logic is currently incomplete.
3. **Concurrency Bottleneck:** To handle concurrent requests, the previous developer added a global naive cache wrapper with a single `std::mutex` locking the entire RPC call, destroying the service's throughput when hit by concurrent workers.

Your task is to:
1. Fix the `Makefile` so that `make` successfully builds the `encoder_server` binary.
2. Implement the encoding logic in `server.cpp`: 
   - First, apply Run-Length Encoding to the input string. For example, `AAAABBBCCDAA` becomes `A4B3C2D1A2`. (Note: Case-sensitive, count always follows the character).
   - Second, encode the resulting RLE string into Base64.
3. Remove the concurrency bottleneck in `server.cpp` so the service can process concurrent gRPC requests efficiently.
4. Run the server on port `50051`.

**Testing and Verification:**
We have provided a stripped, highly-concurrent benchmarking client written in Go at `/app/benchmark_client`. 
Once your server is running on `localhost:50051`, run the client:
`/app/benchmark_client`

The client will verify the correctness of your encoding over several random payloads. If correct, it will then bombard your server with 50,000 concurrent requests and print the Requests Per Second (RPS) to standard output. 

Your C++ implementation must pass the correctness checks AND achieve a metric threshold of at least **10,000 RPS**. 

Save the final output of the successful `/app/benchmark_client` run to `/home/user/benchmark_results.log`.