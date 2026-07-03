You have just inherited an unfamiliar codebase for a geospatial tracking application. The core component is a C++ command-line tool that calculates the total distance traveled along a trajectory using the Haversine formula. However, the system's output is failing its automated checks. The previous developer noted that the distance calculations drift significantly from the expected ground truth, and the error compounds over large datasets. 

Your task is to perform forensics on this data transformation pipeline, identify the root causes of the drift, and fix the C++ code.

**Environment & Files:**
* The C++ source code is located at: `/home/user/trajectory_analyzer.cpp`
* The input data file is a CSV located at: `/home/user/route.csv` (Columns: `id,latitude,longitude`)
* The application should compile with: `g++ -std=c++17 /home/user/trajectory_analyzer.cpp -o /home/user/analyzer`

**Symptoms reported:**
1. **Formula Implementation Error:** A core geometric transformation or formula step inside the distance calculation is implemented incorrectly, causing large deviances.
2. **Floating-point Precision Loss:** As the program accumulates distance over hundreds of thousands of points, floating-point accumulation causes a loss of precision, leading to subtle but failing discrepancies in the final sum.

**Requirements:**
1. Analyze `/home/user/trajectory_analyzer.cpp`.
2. Diff its internal logic against standard implementations of the Haversine formula.
3. Fix the mathematical formula error(s).
4. Fix the data types to ensure precision is maintained throughout the accumulation (use double precision `double` instead of single precision `float` for all coordinate data and distance accumulators).
5. Compile the fixed code.
6. Run the compiled executable. It is hardcoded to read `/home/user/route.csv` and output its result to `/home/user/fixed_analysis.json`.

**Verification:**
The final output must be written to `/home/user/fixed_analysis.json` in the exact format:
```json
{
  "total_distance_km": 12345.6789
}
```
The automated test will parse this JSON file and verify that the `total_distance_km` is correct within a tolerance of 0.001 km.