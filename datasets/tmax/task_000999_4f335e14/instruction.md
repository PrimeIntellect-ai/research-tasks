You are helping a climate researcher organize a massive dataset of continuous sensor readings. The data pipeline involves multiple interacting services and requires a high-performance C++ worker to process files before the disks fill up.

We have a multi-service setup located in `/app/services/`.
1. Run `/app/services/start_services.sh` to launch the required background services:
   - **Redis** (running on `localhost:6379`): Tracks processed file metadata.
   - **Flask Rules API** (running on `http://localhost:5000`): Serves the current dataset configuration.
   - **Sensor Simulator**: Continuously writes new binary data files to nested subdirectories inside `/app/raw_data/` and acquires an exclusive lock (`flock`) on each file while writing.

Your task is to write a highly concurrent C++ program at `/home/user/organizer.cpp` that acts as the dataset processing worker. 

The C++ program must perform the following:
1. **Fetch Configuration:** Make an HTTP GET request to `http://localhost:5000/rules` to retrieve the current organization rules (JSON format: `{"target_dir": "<path>", "prefix": "<string>"}`).
2. **Recursive Traversal:** Recursively traverse `/app/raw_data/` to find all `.dat` files.
3. **Safe Access:** The sensor simulator might still be writing to files. You must acquire a shared or exclusive file lock (`flock`) before reading to ensure you don't read partial data.
4. **Binary Reading:** Each `.dat` file is a binary file containing:
   - Bytes 0-3: A 32-bit signed integer representing the `sensor_id` (little-endian).
   - Bytes 4-403: An array of 100 32-bit floating-point numbers (`float`).
5. **Processing:** Calculate the arithmetic mean of the 100 floats.
6. **Bulk Renaming / Moving:** Move the file to the `target_dir` specified by the Rules API. The new filename must be `{prefix}_{sensor_id}.dat`.
7. **Thread-Safe Logging:** Append a line formatted as `sensor_id,mean_value` (mean formatted to 4 decimal places) to a central text file `/app/organized_data/summary.csv`. Since your C++ program should be highly concurrent, you must use file locks to prevent interleaved writes to this CSV.
8. **Redis Tracking:** For each successfully processed file, add the `sensor_id` to a Redis Set named `processed_sensors` (e.g., using a hiredis client or system commands if necessary, though a native C++ Redis client is preferred).

**Constraints & Verification:**
- You may use Python, bash, or standard tools to explore the system and install necessary C++ libraries (e.g., `libcurl`, `hiredis`), but the core file processing logic **must** be written in C++ (`/home/user/organizer.cpp`).
- You must compile your code to an executable at `/home/user/organizer`.
- **Performance is critical:** A naive single-threaded Python script takes roughly 25 seconds to process 10,000 files. We will test your compiled C++ binary against a massive burst of 50,000 files. Your program must finish processing the batch in **under 3.0 seconds**.
- Once you have written and tested your code, execute `/app/verify_performance.sh` which will stop the continuous simulator, spawn a fresh batch of 50,000 files, and measure your C++ program's throughput.