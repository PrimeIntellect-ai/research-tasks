You are an automation specialist setting up a data pipeline to process sensor logs. 

You have a raw log file located at `/home/user/raw_sensors.log`. This file contains text logs where 3D spatial coordinates (x, y, z) are embedded with inconsistent formatting. 

Your task is to write a bash script or use command-line tools (like `grep`, `sed`, `awk`) to perform the following pipeline:
1. **Regex Extraction**: Extract the `x`, `y`, and `z` numeric values from each line of the log file. The numbers may be integers or floats, positive or negative, and might be surrounded by brackets `[]`, parentheses `()`, angle brackets `<>`, or nothing, with varying whitespace.
2. **Normalization**: Calculate the L2 norm (Euclidean length) of each extracted (x, y, z) vector. Use this to L2-normalize the vector so its length becomes 1. 
3. **Distance Computation**: Calculate the Euclidean distance between the newly *normalized* vector and a fixed reference vector: `(1.0, 0.0, 0.0)`.
4. **Output Generation**: Write the results to a CSV file located at `/home/user/processed_sensors.csv`.

**Formatting Requirements for `/home/user/processed_sensors.csv`**:
- Do not include a header row.
- The columns must be exactly: `original_x,original_y,original_z,norm_x,norm_y,norm_z,distance`
- Every value (both original and computed) must be formatted to exactly 4 decimal places (e.g., `12.0000` or `0.3922`).

You should use only standard Linux CLI tools (Bash, awk, sed, grep, etc.). Do not use Python, Perl, or other scripting languages.