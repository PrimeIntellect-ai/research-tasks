We have a long-running Go microservice located at `/home/user/service/main.go`. It has two endpoints:
1. `/process` - simulates a long-running task.
2. `/stats` - returns the current number of active goroutines.

Our monitoring alerts show that the service is experiencing a severe memory leak over time. It appears that when clients disconnect early or time out (which happens frequently due to our load balancer's aggressive timeout policies), goroutines are left lingering indefinitely, consuming memory and eventually crashing the service.

We have provided a Python script at `/home/user/client.py` that mimics this behavior by firing multiple concurrent requests and timing out quickly.

Your task:
1. Analyze the Go code in `/home/user/service/main.go` and identify the concurrency bug causing the goroutine leak during client cancellations.
2. Fix the bug in `/home/user/service/main.go`.
3. Recompile the service into an executable named `server` in the `/home/user/service/` directory.
4. Run the newly compiled `server` in the background (it listens on port 8080).
5. Execute the verification script `/home/user/verify.sh`. This script will use the `/stats` endpoint and `/home/user/client.py` to test your fix.

If the fix is correct, `/home/user/verify.sh` will produce a file at `/home/user/leak_fixed.log` containing the word `SUCCESS`. Ensure this file is created and shows success.