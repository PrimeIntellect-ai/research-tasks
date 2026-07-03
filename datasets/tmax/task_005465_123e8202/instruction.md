You are acting as a release manager trying to unblock a deployment. Our CI pipeline is failing during the integration load-test phase due to a severe memory/goroutine leak in our Go microservice, which causes OOM kills under load. 

The Go service is located at `/home/user/app/main.go`. It exposes a REST API with a `POST /process` endpoint. However, the current concurrency implementation is flawed and leaks goroutines.

Your tasks are:
1. **Fix the Go Service:** 
   Modify `/home/user/app/main.go` to fix the goroutine leak. The endpoint currently sends data to an unbuffered channel (`jobChan`), but nothing consumes it, causing the spawned goroutines to block indefinitely. Implement a background worker (a single goroutine started in `main()`) that continuously reads from `jobChan` to unblock these goroutines.
2. **Expose Memory Profiling:** 
   Update `main.go` to expose the standard Go `pprof` endpoints so we can monitor memory in our CI pipeline. (Hint: import `net/http/pprof`).
3. **Write a Load Test in Python:** 
   Create a Python script at `/home/user/scripts/load_test.py` that sends 500 concurrent `POST` requests to `http://localhost:8080/process`. The payload for each request should be a JSON object: `{"data": "ci_test"}`. You may use Python's `asyncio` and `aiohttp`, or `concurrent.futures` with `requests`. (You can install any needed Python packages via pip).
4. **Generate the Profile:**
   Start the Go server in the background. Run your Python load test. Once the load test finishes, capture a heap profile from the Go server's pprof endpoint and save it exactly to `/home/user/output_heap.pb.gz`.

Ensure your Go code compiles successfully (`go build`) before capturing the profile. You do not need to keep the server running after you have saved the heap profile.