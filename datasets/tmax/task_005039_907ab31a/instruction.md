You are an engineer investigating a memory leak and processing errors in a long-running Python data ingestion service. The service is supposed to process incoming telemetry data, but it is currently crashing due to memory exhaustion over time and returning incorrect floating-point values for some inputs.

We have a vendored third-party package located at `/app/vendored/telemetry-decoder` (version 1.2.4). This package handles the decoding and serialization of incoming payloads. However, a recent incomplete update to this package introduced several issues:
1. A memory leak occurs when handling corrupted inputs (it caches failed serialization attempts in a global, unbounded dictionary).
2. There is a floating-point precision loss when deserializing coordinate data (using standard float instead of maintaining Decimal precision or a fixed-point struct, causing validation failures down the pipeline).
3. The correct initialization secret needed to authenticate incoming requests was accidentally committed and then removed from the git history of the `/app/service` repository.

Your task is to:
1. Perform git history forensics in `/app/service` to recover the lost authentication secret.
2. Fix the memory leak in `/app/vendored/telemetry-decoder/decoder.py` by ensuring the error cache is either removed or properly bounded/cleared.
3. Fix the floating-point precision issue in `decoder.py` so that coordinate data retains its exact precision (modify the deserialization function to use `decimal.Decimal` instead of `float` for keys ending in `_coord`).
4. Fix the encoding error handling so that corrupted UTF-8 inputs are safely ignored rather than crashing the service or leaking memory.
5. Start the service by running `python /app/service/server.py`. The service should listen on `127.0.0.1:8080`.

The service accepts HTTP POST requests to `/ingest`. You must ensure the service is running in the background and properly handles incoming requests using the recovered secret in the `Authorization: Bearer <secret>` header.