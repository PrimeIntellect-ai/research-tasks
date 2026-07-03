You have recently inherited a mathematical aggregation API codebase that has been acting up. The previous developer left behind a FastAPI service in `/home/user/math-service/` (a Git repository) and a vendored computational library in `/app/vendored/fast-variance/`. 

Users are reporting two major issues with the API:
1. **Precision Loss:** The endpoint `POST /sum` is returning highly inaccurate results for large sequences of numbers with varying magnitudes. It used to be highly accurate. You suspect a recent commit in the `/home/user/math-service/` repository introduced a floating-point regression.
2. **Intermittent Failures under Load:** The endpoint `POST /variance` occasionally returns completely nonsensical values or raises exceptions when hit with concurrent requests. The variance calculation is handled by the `fast-variance` package vendored in `/app/vendored/fast-variance/`.

Your tasks:
1. Use `git bisect` (or manual inspection) in `/home/user/math-service/` to find the commit that introduced the floating-point precision loss in the summation logic. Fix the bug in the current `main` branch so that the `POST /sum` endpoint correctly aggregates numbers without catastrophic cancellation (hint: it previously used an algorithm suitable for high-precision summation, like Kahan summation or `math.fsum`).
2. Debug the concurrent data corruption in the vendored `fast-variance` package (`/app/vendored/fast-variance/`). Identify the race condition in the package's source code, fix it, and reinstall the package. 
3. Start the FastAPI service so it listens on `127.0.0.1:8080`. Ensure it runs as a background process or daemon so the automated verifier can reach it.

API Specification:
- **Base URL:** `http://127.0.0.1:8080`
- **Authentication:** All requests must include the header `Authorization: Bearer calc-token-998`
- **Endpoints:**
  - `POST /sum`: Accepts JSON `{"data": [float, float, ...]}`. Returns JSON `{"result": float}`.
  - `POST /variance`: Accepts JSON `{"data": [float, float, ...]}`. Returns JSON `{"result": float}`.

The automated test will concurrently issue multiple HTTP POST requests to both endpoints using the exact bearer token specified above. Ensure the service is robust to concurrency and mathematically accurate.