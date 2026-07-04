You are an operations engineer triaging an ongoing incident. Our video motion analysis API is failing. Monitoring shows that the service intermittently returns HTTP 500 errors or crashes completely due to unhandled exceptions when processing certain segments of our surveillance footage.

The API source code is located at `/home/user/api.py`. It uses FastAPI to serve an endpoint that analyzes video frames to calculate a "motion index" (the standard deviation of pixel differences between consecutive frames). The video file being analyzed is hardcoded as `/app/surveillance.mp4`.

Your investigation has revealed the following symptoms:
1. **Numerical Instability**: The application calculates variance naively. For certain very still frames, floating-point inaccuracies cause the calculated variance to become slightly negative, which then causes a `ValueError: math domain error` when computing the square root for the standard deviation.
2. **Missing Validation**: The system lacks assertion-based intermediate validation, allowing invalid statistical anomalies (like negative variance or `NaN` values) to propagate until they crash the math library.

Your task:
1. Debug and fix the numerical instability in `/home/user/api.py`. You should replace the naive variance calculation with a numerically stable approach (e.g., using `numpy.var` directly, or ensuring variance is clamped to a minimum of `0.0` before taking the square root).
2. Add assertion-based intermediate validation right before the square root calculation to explicitly assert that the variance is not negative and not `NaN`.
3. Install any required dependencies (like `fastapi`, `uvicorn`, `opencv-python-headless`, `numpy`).
4. Start the API server on `0.0.0.0:8080`.

The API must expose the following endpoint:
- `GET /analyze?start_frame=<int>&end_frame=<int>`
- Requires HTTP Header: `X-Ops-Token: triage-2024`
- Must return a JSON response: `{"motion_index": <float>}` where the float is the average standard deviation of differences across the requested frame range.

Leave the fixed server running in the background on port 8080 so our automated verifier can test it against specific frame ranges.