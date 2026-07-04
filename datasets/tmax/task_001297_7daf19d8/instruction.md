You are tasked with debugging and optimizing a failing data processing pipeline for a local weather sensor network. The project is located in `/home/user/app/`.

Currently, the C-based ingestion service is failing to build. Even if it did build, it has severe parsing, logical, and performance bugs that prevent it from processing the sensor stream correctly and efficiently.

The system consists of three components:
1. **Sensor Stream Simulator**: Runs locally on TCP port 8081, emitting raw binary packet streams.
2. **Redis Database**: Runs locally on TCP port 6379, acting as the storage layer for processed readings.
3. **Ingestion Service (C)**: The code in `/home/user/app/ingest.c` is supposed to connect to the sensor stream, parse the packets, format them as JSON, and push them to a Redis list named `sensor_data`.

Your tasks:
1. **Fix the Build**: The `Makefile` and `ingest.c` contain compiler and linker errors. Fix them so the program compiles cleanly.
2. **Recover Database Credentials**: The Redis database requires a password, but the current `config.h` has a placeholder. The original password was accidentally committed to the git repository and later removed. Use git forensics to find the password and update `config.h`.
3. **Fix Protocol Parsing**: The ingestion service is incorrectly parsing the binary packets. We have provided a packet capture in `/home/user/app/docs/capture.pcap`. Analyze the pcap to deduce the correct binary structure, endianness, and padding, then fix the C struct and unpacking logic.
4. **Fix the Timezone Bug**: The C code has a subtle bug where it rejects packets it believes are "too old" or "in the future" based on timestamps. The sensors transmit UTC timestamps, but the C code logic mishandles the timezone conversion. Fix the logic so valid recent packets are accepted.
5. **Optimize Performance**: Once functional, the ingestion service is too slow. Identify the performance bottleneck (e.g., inefficient database connections or query construction) and fix it so it can handle high throughput.

To test the system, we have provided `/home/user/app/start_services.sh`, which brings up the sensor stream simulator and the Redis server.

When you are finished, ensure your compiled binary is located at `/home/user/app/ingest`. We will run an automated throughput benchmark against it. 

Your goal is to process the data accurately such that the automated benchmark scripts measure a throughput of at least 2000 valid records per second. Ensure the `ingest` binary runs infinitely until terminated by a `SIGINT`.