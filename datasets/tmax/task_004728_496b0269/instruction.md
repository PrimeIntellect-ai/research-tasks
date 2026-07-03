You are a data scientist cleaning up a noisy telemetry dataset. You need to extract spatial coordinates from a messy log file, deduplicate the readings, and calculate some spatial statistics. 

Your task is to build a C++ data processing pipeline orchestrated by a Makefile.

Here are the requirements:

1. **Setup**:
   - The input file is located at `/home/user/raw_telemetry.txt`.
   - Install any necessary C++ packages for JSON processing (e.g., `nlohmann-json3-dev`) and compilation (`g++`, `make`).

2. **Data Extraction & Deduplication**:
   - Write a C++ program (e.g., `process_telemetry.cpp`) that reads `/home/user/raw_telemetry.txt`.
   - Extract all 3D coordinates. They are embedded in random text in the format `[X, Y, Z]`, where X, Y, and Z are floating-point numbers.
   - For deduplication, round each extracted coordinate exactly to 1 decimal place. 
   - Use a hash-based data structure (like `std::unordered_set`) to store the unique *rounded* points. (Points with the same X, Y, and Z after rounding to 1 decimal place are duplicates).

3. **Mathematical Computation**:
   - Calculate the **centroid** (the average of the X, Y, and Z coordinates) of all the *unique rounded points*.
   - Calculate the **maximum Euclidean distance** from the centroid to any of the *unique rounded points*.

4. **Pipeline Orchestration**:
   - Create a `Makefile` in `/home/user/` with the following targets:
     - `build`: Compiles the C++ code to an executable named `telemetry_processor`.
     - `run`: Depends on `build`. Executes the program and processes `/home/user/raw_telemetry.txt`.
     - `clean`: Removes the executable.

5. **Output**:
   - The C++ program must write its final results to `/home/user/output_metrics.json`.
   - The JSON file must have the following exact structure:
     ```json
     {
       "unique_points": <integer>,
       "centroid": [<float>, <float>, <float>],
       "max_distance": <float>
     }
     ```
   - Float values in the output JSON should be rounded to exactly 2 decimal places.

Run your Makefile to complete the pipeline. Do not change the input file.