I am building a web backend that requires a high-performance numerical computation exposed via a microservice. I started writing a Python C-extension for the heavy lifting and a gRPC service to expose it, but I ran into build issues and haven't finished the implementation.

Your task is to fix the build configuration, design the gRPC API, implement the server, and benchmark it.

Here is the current state of the project in `/home/user/math_service`:
- `algo.c`: Contains a numerical algorithm calculating a custom series expansion. It relies on the math library (`<math.h>`).
- `setup.py`: A setuptools build script for compiling `algo.c` into a Python extension module named `algo_ext`. It currently fails to link properly when compiled.
- `requirements.txt`: Python dependencies.

Please complete the following steps:
1. Fix the `setup.py` file so that it correctly links the standard math library. Compile the extension using `python3 setup.py build_ext --inplace`.
2. Design a gRPC service in a file named `service.proto` inside `/home/user/math_service/`.
   - Package name: `mathapp`
   - Service name: `MathService`
   - RPC method: `ComputeSeries`
   - Request message: `SeriesRequest` containing an `int32 n` and a `double x`.
   - Response message: `SeriesResponse` containing a `double result`.
3. Generate the Python gRPC stubs from `service.proto` in the same directory.
4. Write the gRPC server implementation in `/home/user/math_service/server.py`. The server should import the `algo_ext` module, use its `compute` method (which takes `n` and `x`), and return the result. Configure the server to listen on port `50051`.
5. Write a benchmark client in `/home/user/math_service/benchmark.py`. The client must:
   - Connect to the server on `localhost:50051`.
   - Make 1000 sequential `ComputeSeries` requests with `n=100` and `x=0.5`.
   - Measure the total time taken for the 1000 requests.
   - Serialize the final result of the *last* computation and the total benchmark time into a JSON file at `/home/user/math_service/benchmark_results.json` with the following exact keys: `{"final_result": <float>, "total_time_seconds": <float>}`.

Start the server in the background and run the benchmark script to generate the JSON file. Ensure the server is cleanly terminated afterward.