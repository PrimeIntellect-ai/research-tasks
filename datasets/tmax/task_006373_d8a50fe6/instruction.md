You are an ETL data engineer building a data validation pipeline for a batch of sensor readings and model predictions. 

You need to write a Python script at `/home/user/validate_etl.py` that reads an incoming dataset from `/home/user/data/incoming.csv` and performs strict schema enforcement, numerical configuration, and mathematical validation on the model outputs.

The input CSV has the following columns: `id`, `x1`, `x2`, `model_output`.

Your script must perform the following pipeline steps in order:

1. **Schema Enforcement:** 
   Ensure that `id` is an integer, and `x1`, `x2`, and `model_output` are all valid floats. Any row containing missing values, empty strings, or values that cannot be parsed into these exact types violates the schema. 
   - Log the `id` of all schema-violating rows to `/home/user/schema_errors.log` (one ID per line, as a string). 
   - Drop these rows from further processing.

2. **Numerical Library Configuration:**
   Before performing any mathematical operations, you must configure `numpy` to strictly raise exceptions on floating-point overflows and invalid operations. You must use `numpy.seterr(over='raise', invalid='raise')`.

3. **Mathematical Output Validation & Overflow Catching:**
   For the remaining valid rows, evaluate the theoretical expected value:
   `V = 0.5 * (x1 ** 2) + 3.2 * x2`
   
   - **Overflows:** Due to potentially corrupt sensor inputs, computing this formula may cause an overflow (which NumPy will now raise as a `FloatingPointError`). Catch this specific exception. If caught, log the `id` of the row to `/home/user/overflow_errors.log` (one ID per line) and drop the row.
   - **Bounds Validation:** The recorded `model_output` must fall within a strict mathematical tolerance of the theoretical value `V`. Specifically, `|model_output - V| <= 1.5`. If the absolute difference strictly exceeds 1.5, it is considered an anomaly. Log the `id` of such rows to `/home/user/math_anomalies.log` (one ID per line) and drop the row.

4. **Output Valid Data:**
   Save all rows that pass all the above checks (schema, no overflow, math within bounds) to `/home/user/valid_data.csv`, preserving the original headers and order.

Make sure your script runs without crashing when it encounters these errors, processing the whole file and producing the required log files. Once you have written the script, run it to generate the output files.