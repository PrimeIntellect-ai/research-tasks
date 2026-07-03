You are an SRE investigating a Python-based metrics aggregation service that has been triggering uptime alerts. The service calculates uptime scores and processes incoming telemetry, but it has two severe bugs:

1. **Asyncio Task Leak:** When a client cancels a request to the `/process` endpoint (e.g., due to a timeout), a background worker task is leaked. Over time, these orphaned tasks accumulate, consuming memory and CPU, which degrades the service.
2. **Precision Loss:** The service updates a high-resolution uptime metric. It adds nanosecond-level deltas (e.g., `1e-9` seconds) to a large cumulative uptime counter (e.g., `100000000.0` seconds). Because of standard IEEE 754 64-bit floating-point precision limits, these tiny additions are truncated, causing the metric to stop incrementing entirely.

The buggy code is located at `/home/user/app/server.py`.

Your task:
1. Debug and fix the precision loss issue in the `UptimeMonitor.add_uptime_delta` method. Ensure that adding very small floating-point numbers to a large float does not suffer from catastrophic truncation. You may use standard Python libraries.
2. Debug and fix the asyncio task leak in the `MetricsServer.handle_process_request` method. Ensure that if the request handler is cancelled, any background tasks it spawned are cleanly cancelled and awaited.
3. Save the corrected code as a new file: `/home/user/app/server_fixed.py`. Ensure the class names and method signatures remain exactly the same so our automated test suite can import it.
4. Construct a regression test script at `/home/user/app/test_regression.py` that imports `server_fixed.py` and programmatically verifies both fixes. The script must:
   - Instantiate `UptimeMonitor`, add `1e-9` exactly `10,000,000` times to `100000000.0`, and assert the final value is strictly greater than `100000000.0`.
   - Run an asyncio test that simulates calling `handle_process_request`, cancels it halfway through, and asserts that `len(asyncio.all_tasks())` returns to the baseline after a brief settle period.
   - Exit with code `0` if successful, and a non-zero code if it fails.

Do not use third-party libraries (e.g., `pytest` or `numpy`); use only the standard library.