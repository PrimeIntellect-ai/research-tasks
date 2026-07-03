As a data analyst for a drone logistics company, you need to track how far drones have moved between two timestamps. You have been given two CSV files containing the 3D coordinates of drones at time $T_1$ and time $T_2$.

Write and execute a C++ program at `/home/user/drone_tracker.cpp` that performs the following tasks:

1. **Multi-format Reading:** Read both `/home/user/t1_positions.csv` and `/home/user/t2_positions.csv`. 
   The CSVs have a header row: `id,x,y,z`. Data types are string for `id` and float for `x,y,z`.

2. **Distance Computation:** For every drone `id` that exists in **both** files, calculate the Euclidean distance it moved between $T_1$ and $T_2$. Note: some drones may only appear in one of the files; ignore those.
   The Euclidean distance formula in 3D is: $\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2 + (z_2-z_1)^2}$

3. **Summary Statistics & Multi-format Writing:** Calculate the total number of matched drones, the average distance moved (across all matched drones), and the `id` of the drone that moved the maximum distance.
   Write these summary statistics to a JSON file at `/home/user/movement_summary.json` with the exact following keys and format:
   ```json
   {
     "matched_drones": <integer>,
     "average_distance": <float rounded to 2 decimal places>,
     "max_distance_id": "<string>"
   }
   ```

4. **Pipeline Logging:** Throughout the execution, the C++ program must append log messages to `/home/user/pipeline.log`. The log file must contain exactly these lines (replace `<N>` with the actual integer numbers):
   ```text
   [INFO] Read <N> records from t1
   [INFO] Read <N> records from t2
   [INFO] Computed distances for <N> drones
   [INFO] Results written to JSON
   ```
   *(Note: The `<N>` for records read should NOT include the header row).*

Compile your C++ program using `g++` (e.g., `g++ -std=c++17 /home/user/drone_tracker.cpp -o /home/user/drone_tracker`) and run it to generate the JSON and log files.