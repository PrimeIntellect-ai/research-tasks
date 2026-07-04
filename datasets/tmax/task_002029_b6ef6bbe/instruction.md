You are an IT support technician resolving escalating tickets for a back-end mathematical microservice. 
Users are complaining about two major issues with the `/home/user/math_service.py` service:
1. The service occasionally crashes with a `RecursionError`.
2. The service intermittently deadlocks under high contention, causing all requests to hang indefinitely.

You have been provided with the service code `/home/user/math_service.py` and a log file `/home/user/service.log` that captures the timeline of recent requests, including thread IDs, request IDs, and stack traces.

Your objectives are:
1. **Analyze Logs**: Reconstruct the timeline from `/home/user/service.log` to identify all Request IDs that ultimately failed due to a `RecursionError` (or max recursion depth exceeded). Extract these Request IDs and write them to `/home/user/recursion_ids.txt`, one ID per line, sorted numerically.
2. **Fix Recursion Bug**: Modify `/home/user/math_service.py` so that any negative value of `n` passed to `compute_sequence(n)` immediately returns `-1`. This will terminate the runaway recursion.
3. **Fix Deadlock**: Modify `/home/user/math_service.py` to eliminate the deadlock condition in `process_request`. The strict requirement is that `lock_A` MUST always be acquired before `lock_B`, regardless of whether `n` is even or odd. Keep the locks in the code, just reorder the acquisition in the problematic branch to be consistent.
4. **Regression Testing**: Write a regression test script at `/home/user/test_math_service.py` that imports `process_request` from `math_service`. The script should launch 50 threads concurrently, passing a mix of even, odd, and negative integers to `process_request`. The script must verify that all threads complete successfully without hanging or throwing exceptions. It should exit with code `0` if successful, and non-zero if a deadlock or exception occurs.

Ensure that after your fixes, running `/home/user/test_math_service.py` completes in under 5 seconds.