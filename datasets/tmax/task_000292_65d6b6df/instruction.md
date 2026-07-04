You are tasked with debugging a failing C++ mathematical microservice. 

A previous developer was working on a root-finding network service located in the git repository at `/app/math_server`. However, the build is currently broken due to a linker error, and even when previous versions compiled, the mathematical algorithm recently started suffering from convergence failures.

Furthermore, the specifications for the service were handed over in an image file located at `/app/specs.png`. 

Your objectives are:
1. Extract the service specifications (Listen Port and Tolerance level) from `/app/specs.png` (Tesseract OCR is installed on the system).
2. Fix the compiler/linker error in the current `HEAD` of the `/app/math_server` repository.
3. Identify and fix the mathematical regression that causes the Newton-Raphson algorithm to fail to converge (you may want to use `git bisect` to find when the regression was introduced). The mathematical function being solved is hardcoded, but the update step was recently corrupted.
4. Apply the extracted Tolerance level to the convergence condition in the code.
5. Recompile the service.
6. Start the server in the background so it listens on the exact Port extracted from the image. 

The service is a raw TCP server. When it receives a newline-terminated floating-point string (representing the initial guess `x0`), it computes the root of the hardcoded function, and responds with the computed root formatted to 5 decimal places followed by a newline, then closes the connection.

Ensure your fixed server is running and bound to the correct port before finishing the task. Do not change the function being evaluated, only the root-finding logic and server configuration.