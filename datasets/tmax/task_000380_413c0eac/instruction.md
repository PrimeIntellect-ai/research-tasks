We have a C++ HTTP server that computes the sample variance of a list of numbers. Our support engineers are collecting diagnostics for two reported issues:

1. **Numerical Instability**: When computing variance for datasets where the values are very large but close to each other (e.g., `[100000000.1, 100000000.2, 100000000.3]`), the server produces wildly incorrect values or `0.0`. The current implementation uses the naive $E[X^2] - E[X]^2$ formula, which suffers from catastrophic cancellation.
2. **Serialization Truncation**: Even when the math is somewhat correct, the returned JSON truncates all floating-point values to exactly 2 decimal places, losing critical precision.

The server source code is located at `/home/user/app`. It uses the header-only `cpp-httplib` (included in the directory) and a vendored `nlohmann_json` library located at `/app/nlohmann_json`.

Your tasks:
1. Fix the numerical instability in `/home/user/app/server.cpp`. You should replace the naive variance calculation with a numerically stable method (like Welford's algorithm or a robust two-pass mean-centered algorithm). Note: compute the *sample* variance (divide by N-1).
2. Diagnose and fix the serialization issue. A previous developer modified the vendored `/app/nlohmann_json/single_include/nlohmann/json.hpp` file, deliberately hardcoding floating-point serialization precision to `2` decimal places instead of the standard library limits. Find this perturbation and restore it to use `std::numeric_limits<number_float_t>::max_digits10` (or `digits10` depending on the original code).
3. Recompile the server using the provided `Makefile` in `/home/user/app`.
4. Start the server in the background. It is configured to listen on `127.0.0.1:8080`.

To verify your fix, the server must properly handle a `POST` request to `/variance` with a JSON payload like `{"data": [100000000.1, 100000000.2, 100000000.3]}` and return the JSON response `{"variance": 0.01}` with high precision. Do not change the endpoint path or port. Leave the server running so it can be tested.