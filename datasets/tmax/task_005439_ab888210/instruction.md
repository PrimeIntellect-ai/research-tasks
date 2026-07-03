You are a data scientist tasked with cleaning a noisy dataset using Rust. You need to impute missing values by leveraging feature correlations and linear regression.

A dataset has been provided at `/home/user/sensor_data.csv` containing four columns: `temp`, `pressure`, `humidity`, and `vibration`. Some values in the `humidity` column are missing (represented by empty fields, e.g., `16.0,100.9,,0.4`).

Your objective is to write a Rust program in `/home/user/cleaner` that does the following:
1. Configures a Rust project (using standard tools like `cargo`) and includes any necessary numerical libraries (e.g., `ndarray` or standard mathematical primitives).
2. Reads `/home/user/sensor_data.csv`.
3. Isolates the rows where no data is missing.
4. Calculates the Pearson correlation coefficient between `humidity` and all other features using the complete rows.
5. Identifies the feature most strongly correlated with `humidity` (highest absolute Pearson correlation).
6. Fits a Simple Linear Regression model ($y = mx + c$) where $y$ is `humidity` and $x$ is the most correlated feature, using the complete rows.
7. Uses this regression model to impute the missing values in the `humidity` column.
8. Writes the repaired dataset to `/home/user/cleaned_data.csv`.

**Output Formatting:**
- The output file `/home/user/cleaned_data.csv` must include the header row.
- All floating-point numbers in the output must be formatted to exactly one decimal place (e.g., `10.0`, `101.2`, `45.0`, `0.5`).
- The row order must remain identical to the input file.

Ensure your Rust code compiles and runs successfully, and generates the final cleaned file exactly as specified.