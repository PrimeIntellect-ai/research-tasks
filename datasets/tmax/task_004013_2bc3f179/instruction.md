You are an engineer setting up a polyglot gRPC system. We have a vendored repository located at `/app/vendored/service-mesh` which contains a Go gRPC server and a Python client. 

Unfortunately, the system is currently broken and the client is heavily underperforming. Your tasks are:

1. **Fix the Go Build**: The Go server in `/app/vendored/service-mesh/server` currently fails to build due to a circular import between the `config` and `models` packages. Refactor the Go code to resolve the circular import so that `go build -o server .` succeeds. Start the server on port 50051 (it will run in the background).
2. **Generate Protobufs**: Compile the protobuf definition (`/app/vendored/service-mesh/proto/service.proto`) into Python gRPC code inside the `/app/vendored/service-mesh/client/` directory.
3. **Property-based Testing**: Write a property-based test in `/app/vendored/service-mesh/client/test_props.py` using the `hypothesis` library to generate arbitrary string payloads and verify that the Go server's `Echo` RPC returns the exact same payload. 
4. **Optimize Python Client**: The benchmark script `/app/vendored/service-mesh/client/benchmark.py` currently makes 10,000 synchronous gRPC calls, which is extremely slow. Rewrite `benchmark.py` to use `asyncio` and `grpc.aio` to make concurrent requests. Your goal is to maximize throughput.
5. **Output Metric**: Run your optimized `benchmark.py`. The script must output the requests per second (RPS) as a single float to a file named `/app/throughput.txt`. 

You have succeeded if the Go server builds, the protobufs are generated, the property-based tests pass, and the benchmark throughput recorded in `/app/throughput.txt` exceeds 2000 requests per second.