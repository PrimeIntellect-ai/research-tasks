You are a platform engineer maintaining the CI/CD pipeline for a suite of mathematical microservices. We are currently evaluating whether to migrate our mathematical computation services from REST to gRPC to reduce latency overhead.

Your task is to set up, implement, and benchmark both a REST and a gRPC service for a "Sum of Divisors" mathematical function. 

You have been provided a partially complete workspace at `/home/user/math_perf`.
Inside, you will find:
- `math_lib.py`: Contains the core mathematical logic `compute_sum_of_divisors(n)`.
- `rest_server.py`: A complete Flask-based REST API that exposes the function at `GET /sum_divisors/<n>`.
- `math_service.proto`: A skeleton Protocol Buffers file.
- `grpc_server.py`: A partially implemented gRPC server.
- `numbers.txt`: A file containing 100 integers, one per line.

Follow these instructions exactly:

1. **Environment Setup**:
   - Create a Python virtual environment at `/home/user/venv`.
   - Install the necessary dependencies to run Flask, compile Protobufs, run gRPC servers, and make HTTP requests (`flask`, `grpcio`, `grpcio-tools`, `requests`).

2. **gRPC Implementation**:
   - Edit `/home/user/math_perf/math_service.proto` to define a gRPC service named `MathService`. It must have an RPC method named `SumOfDivisors`.
   - The method should accept a message `DivisorRequest` containing an `int64 number`.
   - The method should return a message `DivisorResponse` containing an `int64 result`.
   - Compile the protobuf file into Python code (`math_service_pb2.py` and `math_service_pb2_grpc.py`) inside the `/home/user/math_perf/` directory.
   - Complete `/home/user/math_perf/grpc_server.py` so that it implements the `MathService` and uses `math_lib.compute_sum_of_divisors`.

3. **Performance Benchmarking**:
   - Start `rest_server.py` (runs on port 5000) and `grpc_server.py` (runs on port 50051) in the background.
   - Write a benchmarking script `/home/user/math_perf/benchmark.py` that reads the 100 integers from `numbers.txt`.
   - For each number, send a request to the REST API, measure the latency (in milliseconds), and record the mathematical result.
   - Do the same for the gRPC API.
   - Calculate the mean latency for both the REST API and the gRPC API across the 100 requests.

4. **Reporting**:
   - Your benchmarking script must output a JSON file at `/home/user/math_perf/report.json` with the following exact keys:
     - `"rest_mean_latency_ms"`: (float) the average latency of the REST calls in milliseconds.
     - `"grpc_mean_latency_ms"`: (float) the average latency of the gRPC calls in milliseconds.
     - `"total_divisors_sum"`: (integer) the sum of all 100 results returned by the API (to verify correct mathematical evaluation). You should get the same total sum from both APIs; just report it once.

Ensure the servers remain running or your script properly outputs the final `report.json` before finishing.