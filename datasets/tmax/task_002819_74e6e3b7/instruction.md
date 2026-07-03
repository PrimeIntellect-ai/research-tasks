You are tasked with debugging a failing data aggregation pipeline for a high-frequency sensor network. The CI pipeline is currently failing the end-to-end integration tests due to both crashes and unacceptable numerical errors in the output data.

The project is located in `/home/user/app/`. 

The pipeline consists of three cooperating services:
1. **Sensor Simulator (`sensor_sim.py`)**: Emits a continuous stream of binary sensor data over TCP on port 8081.
2. **Aggregator API (`aggregator.py`)**: Connects to the sensor stream, parses the proprietary binary format, calculates the statistical variance of each batch of readings, and stores the results in Redis.
3. **Redis**: Runs locally on the default port (6379) and acts as the data store.

### The Issues
Your investigation needs to address two separate problems:
1. **Format Parsing Edge-Cases**: The `aggregator.py` script sporadically crashes or loses synchronization with the stream. The proprietary binary format specifies that each packet consists of a 2-byte unsigned short (little-endian) representing the payload length, followed by an array of 32-bit floats. However, the sensor occasionally injects 4-byte "heartbeat" markers (`0x00 0x00 0xFF 0xFF`). The current parsing logic in `aggregator.py` does not handle this edge case correctly, leading to massive misalignment. You need to repair the parser to safely ignore heartbeats and correctly read the subsequent packets.
2. **Precision Loss and Binary Reversing**: The aggregator computes the variance of the sensor readings by delegating to a pre-compiled shared library `/home/user/app/libvariance.so`. We've lost the source code for this library. When processing datasets with high baseline offsets (e.g., values around `100,000.0` but with small fluctuations), the variance values stored in Redis are completely wrong. You must reverse engineer the binary to understand the flawed algorithm it uses (likely catastrophic cancellation due to a naive formula and/or floating-point precision issues). Once you understand the flaw, bypass the binary by implementing a numerically stable variance calculation directly in `aggregator.py` (e.g., using Welford's algorithm or standard library tools with high precision).

### Running and Testing
- A convenience script `/home/user/app/start_services.sh` is provided to spin up the mock sensor and the aggregator. (Ensure Redis is running).
- You can run the integration test via `python3 /home/user/app/run_e2e_test.py`.
- The `run_e2e_test.py` script will pull the calculated variances from Redis and compare them against the true analytical variances. It outputs a Mean Squared Error (MSE) metric. 

### Goal
Modify `/home/user/app/aggregator.py` to fix the parsing bugs and replace the flawed binary variance calculation with a numerically stable Python implementation. 
Run the integration test. To succeed, the test must complete without crashing (meaning the parser handles the heartbeats) and the MSE must be less than `1e-6`. 
Leave your finalized `aggregator.py` in the `/home/user/app/` directory. You do not need to rewrite the C library; doing it in Python is perfectly acceptable.