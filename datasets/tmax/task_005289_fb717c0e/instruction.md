You are a performance engineer tasked with debugging and fixing a distributed scientific computing pipeline. The system processes sensor network data (representing a graph of measurements) and computes a numerical integral. 

Currently, the system produces non-reproducible results because the aggregation step adds floating-point numbers in an unpredictable order depending on network latency. 

Your goals are twofold:

1. **Fix the multi-service pipeline**:
   The system consists of two services in `/app/services`:
   - `sensor_stream`: A service on port 9001 that outputs raw sensor data in HDF5-like text dumps.
   - `aggregator_api`: A web service on port 9002 that is supposed to trigger the calculation. 
   Configure the `aggregator_api` by editing `/home/user/config.env` so that it points to the `sensor_stream` on `localhost:9001`. Ensure both services are started using the provided `/app/start_services.sh` script.

2. **Rewrite the Aggregation Script**:
   The `aggregator_api` calls `/home/user/aggregate.sh <input_file>` to compute the final integral. 
   Write `/home/user/aggregate.sh` in Bash (using standard tools like `awk`, `sort`, `sed`) to compute the numerical integral of the input data using the Trapezoidal rule.
   
   The `<input_file>` contains lines with `<node_id> <floating_point_value>`.
   To guarantee bit-exact reproducibility and eliminate floating-point reduction order issues:
   - Extract the node IDs (which act as the x-coordinates) and the values (y-coordinates).
   - Strictly sort the data points by `node_id` in ascending numerical order before performing any arithmetic.
   - Compute the Trapezoidal rule integral: `Sum over i from 1 to N-1 of: (x_{i+1} - x_i) * (y_{i+1} + y_i) / 2.0`.
   - Print the final integral formatted to exactly 6 decimal places.
   
   Your script `/home/user/aggregate.sh` must be robust, executable, and perfectly match the deterministic output of our reference oracle.

Do not use Python or C++ for the math; rely on Bash and `awk`.