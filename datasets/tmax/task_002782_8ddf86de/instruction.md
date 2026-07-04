You are a security researcher analyzing a suspicious Python asynchronous service that is prone to Denial of Service (DoS) attacks via task leakage and CPU exhaustion.

You have been provided with the service code at `/home/user/suspicious_service.py` and a hex-encoded malicious payload at `/home/user/payload.hex`.

The service receives binary payloads, parses them to extract parameters `a`, `b`, and `x0`, and attempts to find a root for the function `f(x) = x^3 - a*x + b` using the Newton-Raphson method. 

Currently, the service has several issues:
1. **Format parsing edge-case:** The parser incorrectly unpacks negative integers due to a missing signedness flag in the `struct.unpack` call.
2. **Convergence failure repair:** The `compute_root` asynchronous function loops indefinitely if the Newton-Raphson method fails to converge (which happens with the corrupted payload).
3. **Corrupted input handling:** Because of the infinite loop and improper `CancelledError` handling, when the request times out, the background task catches the cancellation and continues spinning forever, leaking tasks and exhausting the CPU.

Your tasks:
1. Debug and modify `/home/user/suspicious_service.py`. 
   - Fix the binary parsing so it reads signed 32-bit integers (little-endian) for `a`, `b`, and `x0`.
   - Update `compute_root` to limit the Newton-Raphson loop to a maximum of 100 iterations. If it does not converge within 100 iterations, it must raise a `ValueError("Convergence failed")`.
   - Ensure the function properly terminates upon cancellation (do not catch and swallow `asyncio.CancelledError`).
2. Construct a regression test script at `/home/user/regression_test.py` that:
   - Reads `/home/user/payload.hex`.
   - Decodes it into bytes.
   - Passes it to the `handle_payload` function (which you may import from `suspicious_service.py`).
   - Asserts that a `ValueError` with the exact message `"Convergence failed"` is raised.
   - The script should print "PASS" to standard output and exit with code 0 if the assertion succeeds, or exit with code 1 otherwise.

To verify your work, I will run `python3 /home/user/regression_test.py`.