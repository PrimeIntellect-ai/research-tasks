We have a log ingestion pipeline that is currently failing. I am a DevOps engineer trying to debug why our log processor is dropping data and producing incorrect metric values.

The system consists of three services that should run together:
1. **Redis**: Used for metric caching (needs to run on port 6379).
2. **Log Generator**: A Python service located in `/home/user/services/generator/`, which generates custom binary log streams.
3. **Log Processor**: A C++ service in `/home/user/services/processor/` that reads these binary logs, applies data transformations, repairs corrupted entries, and outputs serialized JSON logs.

Currently, the pipeline is broken in two ways:
**Part 1: Service Composition**
The startup script `/home/user/start_services.sh` is misconfigured. The Log Generator is trying to send logs to the wrong port, and the C++ Processor isn't configured to connect to Redis. You need to fix the script and configuration files (like `/home/user/services/processor/config.env`) so that:
- Redis starts correctly on port 6379.
- The Log Processor listens on TCP port 8080 and connects to Redis.
- The Log Generator connects and sends its stream to TCP port 8080.

**Part 2: C++ Processor Bugs**
The C++ Log Processor (`/home/user/services/processor/main.cpp`) has several data transformation and encoding bugs:
1. **Floating-point precision repair:** The float values in the binary stream are little-endian IEEE 754 32-bit floats. The current C++ code incorrectly reads them, causing precision loss or absurd values. It also prints them to JSON with poor precision; they must be formatted with exactly 6 decimal places (e.g., `12.345600`).
2. **Database recovery (WAL):** Occasionally, the stream includes WAL (Write-Ahead Log) recovery frames. These start with the magic bytes `WAL\x01`. The current parser throws an error and crashes when it sees this. It should instead skip the next 4-byte CRC checksum, and then read the normal log entry that follows.
3. **Encoding troubleshooting:** The strings in the binary format are length-prefixed (2 bytes, little-endian) UTF-8. The current implementation sometimes reads the wrong length due to endianness issues.

Fix `main.cpp` so that it correctly parses the binary stream from `stdin` and outputs valid JSON lines to `stdout`. 

We have a stripped reference binary (an oracle) of the log processor at `/app/oracle_processor`. Your compiled C++ program (which you must compile to `/home/user/services/processor/processor`) must produce BIT-EXACT identical stdout output to `/app/oracle_processor` for any given raw binary input chunk.

Your tasks:
1. Fix the environment setup and service scripts.
2. Fix the C++ bugs in `/home/user/services/processor/main.cpp`.
3. Compile your fixed version to `/home/user/services/processor/processor`.
4. Ensure the end-to-end pipeline works when `/home/user/start_services.sh` is run.

Please debug the logs, compare diffs using the oracle, and provide a working, equivalent binary.