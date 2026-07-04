You are a DevOps engineer tasked with debugging a critical Rust-based video telemetry service. The service is designed to process a video feed, extract numerical telemetry (like average frame brightness and variance), apply an iterative smoothing algorithm, and serve these metrics via an HTTP API to the operations team.

However, the current implementation is failing in production. The service logs are filled with `NaN` and `Infinity` values, tracking algorithms are failing to converge, and our internal alerting queries are returning incorrect results.

The source code for the service is located at `/home/user/video_telemetry`. The video feed it needs to analyze is mounted at `/app/telemetry_feed.mp4`.

Your objectives are to diagnose and fix the following issues in the Rust application, then leave the service running for verification:

1. **Floating-point Precision & Convergence Issues**: The service calculates a rolling variance of frame pixel intensities. However, due to precision loss in the naive calculation ($E[X^2] - (E[X])^2$) using `f32`, catastrophic cancellation occurs, resulting in negative variances and subsequent `NaN`s when square roots are applied. Furthermore, the iterative smoothing algorithm fails to converge because of this precision loss. You must repair these floating-point and convergence issues (e.g., by upgrading precision to `f64` and/or implementing a numerically stable algorithm like Welford's).
2. **Query Result Debugging**: The service exposes an endpoint `/api/alerts` that allows the DevOps team to query frames where the smoothed metric exceeds a certain threshold. The current query logic contains a bug: it incorrectly filters the internal logs, returning false positives and missing critical frames. Debug and fix the filtering logic.
3. **Run the Service**: Once fixed, compile and run the service. It must listen on `127.0.0.1:8080`. 

**Service API Specification (for your reference):**
*   **Authentication:** All requests must include the header `Authorization: Bearer devops_admin_2024`. Requests without this (or with an incorrect token) must return a `401 Unauthorized`.
*   **`GET /api/variance?frame=<N>`**: Returns a JSON object `{"frame": N, "variance": <float>}` calculating the stable variance of pixel intensities up to frame N.
*   **`GET /api/alerts?threshold=<float>`**: Returns a JSON array of frame numbers where the smoothed metric strictly exceeded the given threshold.

You must modify the Rust code in `/home/user/video_telemetry` to fix these bugs. Once fixed, execute `cargo run --release` in the background so the server is listening on `127.0.0.1:8080`. You can extract frames or test locally using `ffmpeg` and `curl`. Leave the server running when you are done.