Wake up, you're on call. We have a P1 incident at 3 AM.

Our real-time financial aggregation service, `ticker-service`, is completely down. Downstream systems are reporting three distinct issues:
1. The service is intermittently crashing (panicking) when processing certain edge-case ticks.
2. The Volume Weighted Average Price (VWAP) calculations are suffering from precision loss, causing accounting discrepancies.
3. The service is failing to authenticate with our upstream verification sink because the API key was lost during a recent refactor.

The source code for the service is a vendored Rust package located at `/app/data-ingestor`. 

Your tasks:
1. **Git Forensics:** The API key was accidentally hardcoded in a previous commit and then removed, but we lost the secure vault entry. Recover the API key from the local Git history of `/app/data-ingestor`. You must set this key as the `UPSTREAM_API_KEY` environment variable when you run the service. The service expects requests to include this key in the `Authorization: Bearer <KEY>` header.
2. **Intermittent Failure Reproduction & Fix:** The service panics when a tick with a `qty` (quantity) of `0` is received, because it blindly divides by total quantity when calculating the VWAP. You must implement a fix that ignores (safely drops) any ticks where `qty == 0` without panicking, returning a `400 Bad Request` instead.
3. **Precision Loss Tracking:** Look at how `price` and internal VWAP accumulators are typed. They are currently using `f32`. You must upgrade the data types to `f64` throughout the service to ensure high-precision calculations.
4. **Integration & Deployment:** Once the code is fixed, compile it using `cargo build --release`. Start the service so that it binds to exactly `127.0.0.1:8080`. Leave it running in the background.

The service must implement the following HTTP API:
- `POST /tick`: Accepts JSON e.g., `{"symbol": "AAPL", "price": 150.123456789, "qty": 100}`.
- `GET /vwap?symbol=AAPL`: Returns JSON e.g., `{"symbol": "AAPL", "vwap": 150.123456789}`.

Fix the bugs, recover the secret, and start the fixed service. An automated verifier will send HTTP requests to test the robustness and precision of your running server.