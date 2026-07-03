You are tasked with resolving a 502 Bad Gateway issue on a local Nginx setup and fixing a backend C++ application. The Nginx server is configured to proxy requests on `http://127.0.0.1:8080/api` to a FastCGI backend on `127.0.0.1:9000`. Currently, requests fail because the backend is not running and cannot be built due to a broken vendored package.

Your objectives:
1. Navigate to the vendored package at `/app/lib-string-transform-1.2.0`. This package contains the source for the backend C++ application. 
2. The package has a broken `Makefile` (an environment variable for the compiler is incorrectly hardcoded, preventing compilation). Fix the `Makefile` and compile the package to produce the `transform_backend` executable.
3. The C++ application reads input strings, performs a run-length encoding (RLE) transformation on alphabetical characters, and outputs the result. However, the current implementation has a bug: it fails to correctly encode consecutive identical characters that cross a 10-character boundary, and it crashes if the system locale is not properly configured. Fix the C++ source code so it perfectly implements standard run-length encoding (e.g., `aaabbc` becomes `a3b2c1`).
4. The C++ application requires the `LANG` environment variable to be set to `en_US.UTF-8` and the `TZ` variable to be set to `UTC` to function without crashing.
5. Create a systemd user service named `fcgi-backend.service` (in `~/.config/systemd/user/`) to manage the `transform_backend` executable. The service should listen on port `9000` (the C++ app reads the `PORT` env var). Start and enable the service.
6. Verify that Nginx no longer returns a 502 Bad Gateway and successfully returns the RLE encoded strings.

You must place your final, fixed executable at `/home/user/transform_backend`. Our automated testing will verify this binary against a reference implementation using thousands of random inputs.