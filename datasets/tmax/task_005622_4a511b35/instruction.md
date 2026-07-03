**PagerDuty Alert - 03:00 AM**
**Service:** Location Anomaly Detector (Service-Beta)
**Issue:** P99 processing latency spiking. Intermittent crashes reported. Anomaly scores for the fleet are diverging from expected bounds.

You are the on-call engineer. The Location Anomaly Detector processes location telemetry from our mobile fleet (Service-Alpha). It seems to be failing on specific payloads, and the downstream dashboards are showing garbage anomaly scores.

**System Overview:**
- Service-Alpha emits base64-encoded telemetry payloads. It logs dispatched event IDs to `/home/user/logs/service_alpha.log`.
- Service-Beta consumes these payloads, decodes them, and calculates an anomaly score. It logs processing attempts to `/home/user/logs/service_beta.log`.
- The processor script is located at `/home/user/system/processor.py`. It reads from `/home/user/data/raw_events.jsonl` and writes results to `/home/user/output/anomalies.json`.

**Your Tasks:**
1. **Investigate Intermittent Failures & Serialization:** Service-Beta is intermittently crashing on certain payloads. By reconstructing the timeline between `service_alpha.log` and `service_beta.log`, you'll notice Service-Beta drops specific records. Fix the deserialization logic in `/home/user/system/processor.py`. (Hint: Service-Alpha recently had a regression where it sometimes encodes the JSON string as `utf-16le` before base64-encoding it, instead of `utf-8`).
2. **Correct the Algorithmic Formula:** The anomaly score formula in `processor.py` is mathematically incorrect and also causes intermittent crashes under specific conditions (e.g., zero time delta). 
   - The *correct* mathematical formula for the score is: `Euclidean_Distance(p1, p2) * e^(-0.1 * time_delta_seconds)`.
   - Ensure the formula handles identical timestamps gracefully without crashing or returning `NaN`.
3. **Generate Correct Outputs:** Once fixed, run `/home/user/system/processor.py` to process `/home/user/data/raw_events.jsonl`. It must successfully process all records and write the correct scores to `/home/user/output/anomalies.json`.
4. **Write a Regression Test:** Create a regression test script at `/home/user/system/test_regression.py` that imports `processor`, stubs a failing utf-16le base64 payload and a zero-time-delta case, and asserts that they no longer raise exceptions.

**Success Criteria:**
- `/home/user/system/processor.py` must be fixed.
- `/home/user/output/anomalies.json` must exist and contain the mathematically correct anomaly scores for *all* events (including the previously dropped ones). Format must be a JSON array of objects: `[{"event_id": "...", "score": 12.34}, ...]`, rounded to 4 decimal places.
- `/home/user/system/test_regression.py` must exist and exit with code 0.