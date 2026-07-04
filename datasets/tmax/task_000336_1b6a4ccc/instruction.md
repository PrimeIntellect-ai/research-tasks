You are acting as a build engineer managing our artifact dependency resolution pipeline. Our pipeline relies on a distributed microservice architecture to evaluate complex dependency expressions (e.g., boolean logic for conditional artifact inclusion). 

Currently, we have three services that run locally for testing:
1. A Redis instance acting as an expression cache.
2. A Python gRPC service (`/app/eval_server.py`) that implements the expression parsing and evaluation (using a custom protobuf definition).
3. A client load generator (`/app/load_tester.py`) that sends a massive stream of expression evaluation requests.

The Python gRPC service is severely unoptimized. Under heavy load, its memory usage spikes, causing our CI/CD workers to run out of memory. 

Your task is to:
1. Compile the protobuf file `/app/proto/expression.proto` into Python gRPC code.
2. Inspect and optimize `/app/eval_server.py`. It currently does naive, memory-intensive parsing and caching of abstract syntax trees (ASTs) for the expressions.
3. Set up test fixtures using the provided `/app/tests/test_fixtures.py` to ensure your optimized logic still returns the correct evaluation results.
4. Integrate the server with the Redis instance (configured via environment variables `REDIS_HOST` and `REDIS_PORT`) to cache results efficiently without leaking memory in the Python process.
5. Create a shell script `/home/user/run_services.sh` that starts the Redis server, the Python gRPC service, and the load tester in the background.

The objective is to reduce the peak memory usage of the `eval_server.py` process. The load tester will execute 50,000 requests. 

When you are done, run the load tester. The automated grading system will execute `/home/user/run_services.sh`, wait for the load tester to finish, and measure the peak RSS (Resident Set Size) memory of the `eval_server.py` process.