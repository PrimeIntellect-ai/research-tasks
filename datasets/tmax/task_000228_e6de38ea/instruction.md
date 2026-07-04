You are a Data Analyst at a sensor monitoring company. Your system receives incoming telemetry data from remote field sensors in CSV format, but the data is often corrupted, improperly encoded, or contains poorly gap-filled (interpolated) records from faulty edge devices.

Your task is to create a robust C++ data sanitization pipeline that filters a stream of CSV data. 

Write a C++ program located at `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`.
Your program must read a CSV stream from `stdin` and print strictly the **valid** rows to `stdout` (including the CSV header).

**CSV Format:**
The CSV has the following columns, strictly in this order:
`Timestamp,SensorID,SensorDescription,Value,IsInterpolated`
- `Timestamp`: Integer (Unix epoch)
- `SensorID`: String
- `SensorDescription`: String (Free-text description)
- `Value`: Float (Sensor reading)
- `IsInterpolated`: Integer (`0` for raw reading, `1` for gap-filled/interpolated reading)

**Sanitization Rules (A row is kept ONLY if it passes ALL of these):**
1. **Regex Validation**: The `SensorID` must exactly match the pattern: `^[A-Z]{3}-\d{4}-[A-F0-9]{4}$` (e.g., `TMP-1024-A1B2`).
2. **Encoding Validation**: The `SensorDescription` must be perfectly valid UTF-8. You must reject the row if it contains any invalid UTF-8 byte sequences (e.g., leftover Windows-1252 or ISO-8859-1 artifacts like `\xff`).
3. **Resampling / Gap-fill Validation**: If `IsInterpolated` is `1`, the `Value` must mathematically match the proprietary interpolation algorithm between the *closest preceding* raw row (`IsInterpolated=0`) and the *closest succeeding* raw row (`IsInterpolated=0`) for the **same** `SensorID`. 

**The Math Oracle:**
Because the interpolation algorithm uses a proprietary smoothing curve, we have provided a compiled tool at `/app/interp_oracle`. 
You can execute it to find the expected interpolated value:
`/app/interp_oracle <timestamp_prior> <value_prior> <timestamp_next> <value_next> <target_timestamp>`
*(It will print a float to stdout. Allow a tiny epsilon like 0.0001 for floating-point comparisons).*

*Note: For testing purposes, you can assume that for any given `SensorID`, the data will always contain a valid `IsInterpolated=0` row before and after any `IsInterpolated=1` row.*

**Environment & Setup:**
- You have standard build tools (`g++`, `make`, `cmake`) installed.
- Do not add any external C++ libraries outside of the standard library, `regex`, and basic POSIX APIs.
- Your program will be evaluated against a hidden clean corpus (which must be 100% preserved) and a hidden evil corpus (which must be 100% rejected).