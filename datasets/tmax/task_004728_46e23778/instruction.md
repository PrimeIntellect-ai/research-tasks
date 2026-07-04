You are an integration developer responsible for testing a mathematical API infrastructure. We have a backend Python server that computes prime factors, and a custom Go reverse proxy designed to load-balance requests to multiple backend instances. 

Currently, the system is failing its performance tests. The Go reverse proxy source code is vendored at `/app/vendored/goproxy-1.0`. It compiles but stalls under heavy concurrent load due to a synchronization bug in how it uses goroutines and channels to dispatch requests.

Your task:
1. Fix the Go concurrency issue in `/app/vendored/goproxy-1.0/main.go`. The proxy must successfully route parallel incoming requests to the backend(s) without deadlocking. 
2. Build the fixed Go proxy (`go build -o proxy main.go`) and run it on port 8080.
3. Start the backend Python prime-factorization API (provided at `/home/user/backend/server.py`) on ports 8081 and 8082. The Go proxy is hardcoded to round-robin to these two ports.
4. Write a Python benchmarking script at `/home/user/benchmark.py` that sends 5,000 concurrent GET requests to the proxy (`http://localhost:8080/factor?n=10403`).
5. Your benchmarking script must write its results to `/home/user/benchmark_results.json` with the following structure:
```json
{
    "total_requests": 5000,
    "successful_requests": 5000,
    "total_time_seconds": 1.23,
    "requests_per_second": 4065.0
}
```

The success of your task will be evaluated by an automated verifier that runs its own benchmarking tool against your fixed Go proxy. To pass, the proxy must successfully handle 10,000 requests without dropped connections, and the average throughput must exceed 2000 Requests Per Second (RPS) on the test infrastructure.