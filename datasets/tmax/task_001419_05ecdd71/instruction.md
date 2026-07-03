You are an automation specialist creating a data processing workflow to reconcile two sets of 3D spatial coordinates from different sensors. 

You have two input datasets located at:
- `/home/user/points_A.csv` (Columns: `id_A, x, y, z`)
- `/home/user/points_B.csv` (Columns: `id_B, x, y, z`)

Your objective is to write and execute a C++ program (`/home/user/process.cpp`) that performs the following pipeline:

1. **Cleaning & Normalization:** Read both CSV files. For every point, normalize the `x`, `y`, and `z` coordinates by rounding them to exactly 1 decimal place. Use standard half-way rounding (e.g., 1.04 becomes 1.0, 1.05 becomes 1.1, 1.99 becomes 2.0).
2. **Hash-based Deduplication:** For each dataset separately, remove duplicate points based on their *normalized* coordinates. If multiple points resolve to the same normalized coordinate in a single file, keep the first `id` encountered and discard the rest.
3. **Inner Join:** Find the intersection of the two deduplicated datasets based on their normalized coordinates.
4. **Output Generation:** Write the joined results to `/home/user/joined_points.csv`. The output must have a header `id_A,id_B,x,y,z` and contain the intersecting points with their normalized coordinates (formatted to 1 decimal place, e.g., `1.0`, not `1`). Sort the output rows in ascending lexicographical order by `id_A`.
5. **Pipeline Logging:** Throughout the process, the program must append to a log file at `/home/user/pipeline.log` with exactly the following lines in order:
   - `Loaded [count] raw points from A`
   - `Loaded [count] raw points from B`
   - `Deduplicated A to [count] points`
   - `Deduplicated B to [count] points`
   - `Found [count] intersecting points`

Ensure your C++ code handles file I/O gracefully, uses efficient hash-based data structures (like `std::unordered_map` or `std::unordered_set` with custom hash functions for the 3D coordinates), and produces the exact output formats requested. Compile and run your script to generate the final CSV and log file.