A researcher in radio astronomy is running simulations of an antenna array. Unfortunately, some simulation outputs are contaminated by non-reproducible floating-point artifact cascades and Radio Frequency Interference (RFI). 

You need to accomplish two things:
1. Create an RFI and artifact detector.
2. Fix and launch the automated data processing pipeline that relies on this detector.

**Part 1: The Detector**
Write a Python script at `/home/user/filter.py`. It must take exactly one argument (the path to a `.npy` file) and determine whether the file is "clean" or "evil" (contaminated).
- **Data Format:** Each `.npy` file contains a 2D NumPy array of shape `(1000, 64)` representing `(Time, Antennas)`.
- **Clean Data:** Consists of standard normally distributed thermal noise.
- **Evil Data:** Contains either narrow-band RFI (a coherent sine wave persisting across time, which produces a sharp spike in the Fourier domain along the time axis) or floating-point `NaN` / `Inf` values resulting from reduction-order bugs in the simulator.
- **Requirement:** Your script must use Fourier transforms to detect the RFI. If the data is clean, the script must exit with status code `0`. If the data contains RFI or NaNs, it must exit with status code `1`.
- You are provided with training corpora in `/home/user/sim_data/clean/` and `/home/user/sim_data/evil/`. Your script must perfectly classify all files in these directories.

**Part 2: The Multi-Service Pipeline**
The automated pipeline consists of three services located in `/home/user/services/`:
1. `redis-server`: Needs to run on its default port `6379`.
2. `producer.py`: Scans a directory, publishes file IDs to a Redis list named `raw_data_queue`, and serves the `.npy` files over HTTP on port `8080`.
3. `aggregator.py`: An HTTP API running on port `9090` that receives JSON payloads of clean data metadata.

You must create a bash script at `/home/user/services/consumer.sh` that loops to pop items from the Redis list `raw_data_queue`. For each item (a file ID):
1. Download the `.npy` file from `http://localhost:8080/data/<file_id>.npy`.
2. Run your `/home/user/filter.py` on the downloaded file.
3. If the file is clean (exit code 0), send a POST request to `http://localhost:9090/register` with JSON body `{"file_id": "<file_id>", "status": "clean"}`.
4. If evil, do not send the POST request.

Finally, write a script `/home/user/start_all.sh` that starts the Redis server, `producer.py`, `aggregator.py`, and `consumer.sh` in the background so the pipeline processes all data.

Ensure all ports are correctly bound and the pipeline successfully filters and registers the data.