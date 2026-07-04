You are an engineer tasked with investigating a memory leak and data corruption issue in a long-running Python service.

The service, located at `/home/user/app/sensor_daemon.py`, processes a stream of hex-encoded 8-bit sensor readings from a text file, applies an Exponential Moving Average (EMA) smoothing algorithm, and stores the results. 

Recently, the service has been running out of memory and producing incorrect smoothed values. We suspect there is a format parsing issue related to how negative sensor readings are handled (the sensor outputs 8-bit signed integers in hex, e.g., "ff" should be -1, not 255). When the EMA fails to converge due to wildly out-of-bounds parsed values, the service queues the reading for a retry, but the retry logic is flawed, leading to an unbounded memory leak.

You have been provided with:
1. The script: `/home/user/app/sensor_daemon.py`
2. A simulated heap dump: `/home/user/app/heap.dump`
3. The application log: `/home/user/app/service.log`
4. A test data file: `/home/user/app/test_data.txt`

Your tasks:
1. Analyze the heap dump and logs to confirm the source of the memory leak.
2. Fix the format parsing bug in the script so that 8-bit signed hex strings are correctly converted to Python integers (e.g., "ff" -> -1, "80" -> -128, "7f" -> 127).
3. Ensure the script no longer leaks memory (failed convergences should be handled properly, either by discarding or correctly capping, but fixing the parsing should prevent the runaway retries).
4. Save your corrected script as `/home/user/fixed_daemon.py`.
5. Run your fixed script on `/home/user/app/test_data.txt` and pipe the standard output to `/home/user/final_state.json`.

The automated test will verify the contents of `/home/user/final_state.json` to ensure the final calculated averages are mathematically correct according to the fixed signed integer rules.