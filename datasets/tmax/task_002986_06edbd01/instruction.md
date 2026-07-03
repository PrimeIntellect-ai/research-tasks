You are a release manager preparing a deployment for a critical routing microservice. We have a legacy routing engine provided as a stripped binary at `/app/legacy_router`. 

Through previous memory debugging and profiling, we discovered that this binary has a severe memory leak if used in a long-running streaming mode (reading and writing continuously from stdin/stdout). Therefore, it must be invoked as a short-lived process for each computation.

Your task is to build a robust HTTP API wrapper around this legacy binary using any language of your choice.

Requirements:
1. The legacy binary `/app/legacy_router` takes exactly 8 bytes of input from `stdin` (representing two 32-bit unsigned integers: `source` and `destination`, in little-endian format) and outputs exactly 4 bytes to `stdout` (representing a 32-bit unsigned integer: `next_hop`, in little-endian format).
2. Create an HTTP REST service listening exactly on `127.0.0.1:9000`.
3. Implement a `POST /route` endpoint that accepts a JSON payload of the form:
   `{"source": 12345, "destination": 67890}`
4. Your service must deserialize this JSON, serialize the integers into the correct little-endian binary format, invoke `/app/legacy_router` for a single execution, read the binary output, deserialize it, and return a JSON response of the form:
   `{"next_hop": 42}`
5. Once your service is running, perform a performance benchmark against your `/route` endpoint using `ab` (Apache Bench) or `wrk`. Use at least 100 total requests and a concurrency of 10. Write the raw benchmarking tool output to `/home/user/bench.txt`.
6. Ensure your HTTP service is running in the background on port 9000 when you complete the task.

Leave your HTTP server running so it can be verified.