You are a data scientist cleaning an experimental dataset of spatial coordinates. 

The raw dataset is located at `/home/user/spatial_data.jsonl`.
Each line is a JSON object with three fields:
- `x`: A float representing the X coordinate.
- `y`: A float representing the Y coordinate, or the exact string `"NaN"` if the sensor failed to record a value.
- `label`: A string containing the point's name, which includes unicode escape sequences (e.g., `\u03b1` for the Greek letter alpha).

Your task is to write a Bash-based pipeline (you can use standard tools like `jq`, `awk`, `sed`, `bc`, etc.) to process this file and generate a cleaned CSV file at `/home/user/cleaned_data.csv`. 

You must perform the following steps:
1. **Character Encoding:** Parse the JSON lines and decode all unicode escape sequences in the `label` field into their actual UTF-8 characters.
2. **Imputation (Interpolation):** For any line where `y` is `"NaN"`, calculate its value using linear interpolation based on the `x` coordinates of the nearest preceding and succeeding lines that have valid `y` values. You can assume the first and last lines of the file will always have valid `y` values, and `x` values are strictly increasing.
3. **Constraint Validation:** After computing the interpolated `y` values, evaluate the constraint equation $x^2 + y^2 \le 100$. Discard any rows that strictly exceed this threshold (i.e., keep rows where $x^2 + y^2 \le 100$).
4. **Formatting:** Output the valid rows to `/home/user/cleaned_data.csv` as comma-separated values in the format `x,y,label`. Do not include a header. Ensure the `y` values are formatted to exactly 1 decimal place.

You must accomplish this entirely within the terminal. Ensure `/home/user/cleaned_data.csv` exactly matches these specifications.