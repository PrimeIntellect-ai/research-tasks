Wake up, we have a P1 incident! It's 3 AM and the sequence calculation service is completely locked up. The monitoring dashboard shows that the CPU usage is pegged at 100% and new requests are timing out. 

We recently deployed a new version of our Collatz sequence API, but it seems there are two major issues:
1. The service fails to start in the new container environment due to a dependency conflict. Someone updated `Werkzeug` to a version that breaks our older `Flask` version, causing `ImportError` on startup.
2. Even when running, a specific mathematical edge case causes the main calculation loop to run infinitely, locking up the server.

You need to fix this system. Here is your objective:

1. Look in `/home/user/service`. You will find `requirements.txt`, `app.py`, and `math_utils.py`.
2. Fix the dependency conflict in `requirements.txt` so that the app can run. (Hint: Flask 2.0.1 requires Werkzeug < 2.1.0, or you can upgrade Flask to 2.2.2).
3. Find the infinite loop bug in `math_utils.py`. The function `collatz_steps(n)` calculates the number of steps to reach 1. However, it currently hangs if `n <= 0`. Modify the code to immediately raise a `ValueError("n must be positive")` if `n <= 0`.
4. Create a regression test file at `/home/user/service/test_math.py`. It must use `pytest` and contain at least two tests:
   - `test_collatz_valid()`: Asserts that `collatz_steps(10)` returns `6`.
   - `test_collatz_invalid()`: Asserts that `collatz_steps(0)` raises a `ValueError`.
5. Run `pytest /home/user/service/test_math.py` to verify your fix.
6. Once everything is working, create a log file at `/home/user/resolution.log` containing exactly two lines:
   - Line 1: The exact name and version of the package you modified in `requirements.txt` to fix the conflict (e.g., `Flask==2.2.2` or `Werkzeug==2.0.3`).
   - Line 2: The string `TESTS_PASSED`

Please resolve this immediately so we can bring the service back online.