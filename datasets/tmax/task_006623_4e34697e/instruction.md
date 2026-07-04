You are an automation specialist creating a data processing workflow for a fleet of environmental sensors. Some sensors occasionally fail to report their values, resulting in missing data. 

You need to write a C++ program that processes a dataset of sensor readings, imputes the missing values using spatial interpolation, applies a quality gate, and outputs a cleaned dataset.

The input data is located at: `/home/user/sensor_data.csv`
It has the following header: `id,x,y,value`
Some rows have a blank `value` (e.g., `4,5.0,5.0,`).

Your C++ program must perform the following tasks:
1. **Distance & Similarity:** For each row with a missing value, find the exactly 3 nearest valid (non-missing) sensor points using standard Euclidean distance based on their `x` and `y` coordinates. (Assume no two points have the exact same coordinates).
2. **Interpolation & Imputation:** Calculate the missing value using Inverse Distance Weighting (IDW) with a power of 2. 
   The formula is: `v = sum(v_i / d_i^2) / sum(1 / d_i^2)` where `v_i` and `d_i` are the values and distances of the 3 nearest valid points.
3. **Validation Checkpoint (Quality Gate):** Environmental constraints dictate that valid interpolated readings must fall within the inclusive range `[10.0, 90.0]`. If the newly calculated value is strictly less than `10.0` or strictly greater than `90.0`, it fails the quality gate.
4. **Output Generation:** Write the fully processed dataset to `/home/user/imputed_sensor_data.csv` maintaining the exact same header and row order.
   - Existing valid rows must be output exactly as they were.
   - Imputed values that pass the quality gate must be formatted to exactly two decimal places (e.g., `50.00`).
   - Imputed values that fail the quality gate must be replaced with the string `REJECTED`.

Please write, compile, and execute the C++ program to generate the target output file.