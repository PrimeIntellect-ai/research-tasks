You are acting as a release manager and full-stack performance engineer. We are preparing to deploy a new hybrid high-performance microservice. The service consists of a C++ core for heavy computations and a Go wrapper that exposes a REST API concurrently. 

However, the previous engineer left the project in a broken state:
1. The deployment specifications (required API port, endpoint path, and target throughput) were only captured in a screenshot of a whiteboard. This image is located at `/app/deployment_spec.png`. You will need to extract these details.
2. The C++ core (`/home/user/src/cpp/`) has a broken `Makefile` that fails to compile into a shared library (`libcompute.so`). It also contains a severe performance bottleneck in `compute.cpp`.
3. The Go REST API (`/home/user/src/go/`) has not been fully implemented. It needs to call the C++ shared library using `cgo` and handle concurrent requests efficiently using goroutines.

Your tasks:
1. **Extract Specs:** Use OCR or visual inspection on `/app/deployment_spec.png` to find the `PORT`, the `ENDPOINT`, and the `TARGET_MS` (maximum allowed milliseconds per 1000 requests).
2. **Fix C++ Build:** Repair `/home/user/src/cpp/Makefile` so that it correctly builds a shared library named `libcompute.so`. Fix any ABI/linking issues.
3. **Optimize C++:** Identify and fix the performance bottleneck in `/home/user/src/cpp/compute.cpp`. You are allowed to change the implementation as long as the mathematical result remains exactly the same.
4. **Implement Go API:** Write the Go web server in `/home/user/src/go/main.go` that listens on the extracted `PORT` and exposes the extracted `ENDPOINT`. It must accept a JSON POST request with the payload `{"values": [float64, float64, ...]}`. It should pass these values to the C++ shared library concurrently, and return the result as `{"result": float64}`.
5. **Run Service:** Start the Go service in the background and ensure it is ready to receive requests. Create a file `/home/user/status.txt` with the word "READY" when your service is running and optimized.

The automated test will evaluate the performance of your running API against the extracted `TARGET_MS` threshold using a load test. You must achieve performance better than or equal to this threshold.