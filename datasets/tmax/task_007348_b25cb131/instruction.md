You are an automation specialist creating a data processing workflow to extract, process, and deduplicate sensor telemetry from an unstructured log file.

Your task is to process the log file located at `/home/user/sensor_data.log` and generate a normalized report.

Here are the requirements:
1. **Extraction**: The log file contains a lot of unstructured text. You need to extract the spatial coordinates which are embedded within the text. The coordinates always appear in this exact format: `{x: <num>, y: <num>, z: <num>}` where `<num>` is a valid integer or floating-point number (can be negative).
   *Example:* `[INFO] Drone 4 reached {x: -2.5, y: 4.0, z: 1.1} safely.`

2. **Mathematical Processing**: For each extracted coordinate, calculate the squared distance from the origin. The formula is: `R^2 = x^2 + y^2 + z^2`.

3. **Hash Generation & Deduplication**: Compute the SHA-256 hash of the *exact extracted coordinate string* (e.g., `{x: -2.5, y: 4.0, z: 1.1}`) without any trailing newlines. Many logs will contain the exact same coordinate string; you must deduplicate them so that each unique coordinate string appears only once in your final output.

4. **Formatting and Sorting**: Create an output file at `/home/user/processed_coordinates.txt`.
   Each line in this file must contain the SHA-256 hash of the coordinate string, followed by a single space, followed by the computed `R^2` value.
   The lines must be sorted numerically in **descending order** based on the `R^2` value.

Your pipeline must correctly handle decimals, negative numbers, and ignore all surrounding text.