You are tasked with fixing a severe regression in our financial calculation service. 

We have a legacy stripped binary at `/app/oracle_bin` that serves as the ground truth for our proprietary pricing algorithm. It takes two float arguments and prints the result. 

Recently, our team attempted to reimplement this logic in Python to improve performance, and the code is tracked in a Git repository located at `/home/user/service_repo` (which contains 200 commits). A regression was introduced somewhere in the commit history. Under concurrent load, the Python service sometimes returns wildly incorrect numbers (numerical instability) due to a suspected race condition in how intermediate values are cached or calculated.

Your objectives:
1. **Reverse Engineer**: Analyze the stripped binary `/app/oracle_bin` to understand the exact mathematical formula it implements. 
2. **Bisect & Diagnose**: Find which commit in `/home/user/service_repo` introduced the concurrency bug causing numerical instability. Reconstruct the log timeline to prove when the bug appears under concurrent requests. Write a regression test script `/home/user/regression_test.py` that reliably triggers the race condition on the faulty commits.
3. **Fix**: Fix the latest version of the Python service in the repository so that it correctly and safely implements the algorithm natively in Python without race conditions.
4. **Deploy**: Start the fixed Python service. It must listen on two protocols:
   - HTTP on `127.0.0.1:8080`. Endpoint `POST /compute` accepting JSON `{"a": <float>, "b": <float>}` and returning `{"result": <float>}`.
   - Raw TCP on `127.0.0.1:8081`. It should accept payloads in the format `<a>,<b>\n` and respond with `<result>\n`.

Leave the fixed service running in the background. Our automated verifier will send concurrent requests via both HTTP and TCP to verify the race condition is resolved and the numerical results exactly match the legacy binary.