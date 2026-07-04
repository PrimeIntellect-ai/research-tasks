You are an open-source maintainer reviewing a pull request for a project called `math-api`, located at `/home/user/math-api`. 

The contributor's PR claims to do two things:
1. Optimize the core math library's modulo function (`fast_mod`) using x86_64 inline assembly.
2. Provide a Python Flask REST API wrapper for the library.

Unfortunately, the PR is broken and incomplete. You need to step in and fix the code before merging.

Here are your specific objectives:

**1. Fix the Assembly Bug in the C Library**
The C core library is located at `/home/user/math-api/math_core.c`. The contributor attempted to write a `fast_mod(uint64_t a, uint64_t m)` function using inline x86_64 assembly. However, they made a mistake in their register mapping—it currently returns the quotient instead of the remainder. 
* Analyze and fix the inline assembly in `math_core.c` so that it correctly returns the remainder of `a % m`.
* Build the shared library using the provided `Makefile` (`make`).

**2. Secure and Stabilize the API**
The Flask application is located at `/home/user/math-api/app.py`. It uses `ctypes` to call the compiled C library. The PR author added a `/mod` endpoint but failed to implement basic API safety features.
* **Input Validation**: Update `/mod` so that query parameters `a` and `m` are required. They must be valid integers, `a` must be >= 0, and `m` must be > 0. If any of these conditions fail, return an HTTP 400 status code with exactly this JSON response: `{"error": "Invalid input"}`.
* **Rate Limiting**: The API is vulnerable to abuse. Integrate `Flask-Limiter` into `app.py` to rate limit the `/mod` endpoint. The limit must be strictly **5 requests per minute** per IP address. Exceeding this limit should return a standard HTTP 429 status code.

**3. Write an Automated Test Script**
Create an integration test script at `/home/user/math-api/run_tests.sh`. Make sure it has executable permissions. The script must:
* Start the Flask server in the background (on port 5000).
* Wait briefly for the server to be ready.
* Send a valid request (e.g., `a=10&m=3`) and verify the output is `{"result": 1}`.
* Send an invalid request (e.g., `a=-5&m=3`) and verify it receives an HTTP 400 status.
* Fire a burst of requests to trigger the rate limit and verify that the 6th request receives an HTTP 429 status.
* If all of the above conditions are successfully met, the script must write the exact string `ALL TESTS PASSED` to `/home/user/math-api/test_report.log`. Clean up the background Flask process before exiting.

Your task is complete when the C code is fixed and compiled, the Flask app is updated, and your test script generates the `test_report.log` file with the success message.