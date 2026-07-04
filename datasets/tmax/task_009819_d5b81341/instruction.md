You are an on-call engineer and have just been paged at 3 AM. The data pipeline is crashing intermittently. 

System Architecture:
- Incoming requests are processed by three distinct services.
- Logs for these services are stored in `/home/user/logs/`:
  - `ingest.log`: Uses Unix Epoch timestamps.
  - `transform.log`: Uses ISO-8601 timestamps.
  - `serialize.log`: Uses custom format `[MM-DD-YYYY HH:MM:SS]`.
- Raw payloads for each request are stored as JSON files in `/home/user/data/` named `raw_<ReqID>.json`.
- The final step of the pipeline is a Python script `/home/user/app/serializer.py` which reads a JSON payload and serializes it to a fixed-width binary format. 

The Problem:
`serialize.log` shows that `serializer.py` occasionally panics and throws an unhandled exception, causing the pipeline to drop data. This only happens for specific, rare edge-case data. 

Your Tasks:
1. **Log Timeline Reconstruction**: Identify the exact `ReqID` that caused the traceback in `serialize.log`. Reconstruct the timeline of this specific request across all three services. 
   Create a file `/home/user/timeline.txt` containing exactly three lines (one for each service's log entry for this `ReqID`), chronologically ordered, formatted exactly as:
   `[Service Name] | [Unified Unix Epoch Timestamp] | [ReqID]`
   (Service Names should be exactly `Ingest`, `Transform`, and `Serialize`. Use integer Epoch timestamps.)

2. **Encoding/Serialization Troubleshooting**: Inspect `/home/user/app/serializer.py` and the raw JSON payload for the failing `ReqID` (located in `/home/user/data/raw_<ReqID>.json`). Identify why the serialization is failing (it is an encoding issue related to edge-case characters).

3. **Intermittent Failure Reproduction & Fix**: 
   - Fix `/home/user/app/serializer.py` so it handles international/Unicode characters safely by encoding them to `utf-8` instead of `ascii`, while maintaining the 20-byte fixed-width padding requirements for the `user_name` field. If the utf-8 encoded string is longer than 20 bytes, it should be truncated to 20 bytes before padding.
   - Run the fixed script on the failing payload to verify it no longer crashes. The script takes two arguments: the input json file and the output binary file. Output the fixed payload to `/home/user/data/out_<ReqID>.bin`.

Ensure that you leave `/home/user/timeline.txt` and `/home/user/data/out_<ReqID>.bin` (where `<ReqID>` is the ID of the failing request) strictly correctly formatted and generated.