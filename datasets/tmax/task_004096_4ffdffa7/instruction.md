You are an environmental data scientist building a robust ETL pipeline to sanitize and transform telemetry data from remote weather stations. 

Currently, our telemetry source streams raw JSON records over a TCP socket, but the data is polluted with malformed entries, outlier noise, and occasional corrupted metadata (like injected escape characters or control sequences). 

You need to implement a high-performance C++ stream processor that filters out the noise (the "evil" data) while keeping the valid records (the "clean" data), and transforms the valid records into a specific XML-like template format before sending them to a downstream sink.

Here is the setup:
1. **Source Service:** A background service listening on `localhost:9001`. Upon connection, it streams continuous raw JSON records (one per line) representing sensor telemetry.
2. **Sink Service:** A destination service listening on `localhost:9002`. It expects to receive cleaned, formatted records line-by-line.

**Requirements:**
1. **C++ Stream Processor (`/home/user/processor.cpp`):**
   - Write a C++ program that reads JSON lines from standard input (`stdin`) and writes to standard output (`stdout`). Memory efficiency is critical; you must process the data as a stream (line-by-line), NOT load everything into memory.
   - You can use `#include <nlohmann/json.hpp>` (already installed in the system) for JSON parsing.
   - **Input Format:** `{"id": "<string>", "sensor": "<string>", "value": <float>, "meta": "<string>"}`
   - **Validation Rules (to filter out "evil" records):**
     - The record MUST contain all four fields (`id`, `sensor`, `value`, `meta`).
     - `value` MUST be between `-50.0` and `150.0` (inclusive).
     - `meta` MUST contain strictly alphanumeric characters and underscores (`^[a-zA-Z0-9_]+$`). Any spaces, punctuation, or special characters mean the record is corrupted and should be dropped.
   - **Transformation Template:** For valid records, output exactly one line per record to `stdout` in this format:
     `<Reading><ID>{id}</ID><Type>{sensor}</Type><Val>{value}</Val><Meta>{meta}</Meta></Reading>`
     *(Note: Format `value` to exactly 2 decimal places).*
   - Compile this program to `/home/user/processor`.

2. **Pipeline Glue Script (`/home/user/run_pipeline.sh`):**
   - Write a bash script that connects the source service (`localhost:9001`), pipes the stream through your compiled `/home/user/processor`, and pipes the output directly into the sink service (`localhost:9002`). Use tools like `nc` (netcat).
   - Ensure the script is executable.

The system will verify your solution by testing your C++ processor against a corpus of verified clean and maliciously corrupted ("evil") records, and by invoking your pipeline script to ensure the multi-service composition works end-to-end.