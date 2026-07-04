You are an AI data analyst. We have a set of time series CSV files containing sensor readings. Some of these files are clean and valid, while others contain anomalies, malformed records (like embedded newlines designed to break naive parsers), or represent anomalous sensor behavior. 

Your objective is to build a robust Go-based classifier that correctly identifies whether a given CSV file is "clean" or "evil" (anomalous/malformed).

Here is what you need to do:

1. **Extract Configuration**: 
   There is an image located at `/app/config.png`. You must perform OCR on this image to extract three configuration parameters:
   - `Target Reference`: A sequence of 5 float values.
   - `Max Euclidean Distance`: A float threshold.
   - `Reject Token`: A specific string token.

2. **Write the Classifier**:
   Create a Go program at `/home/user/classifier.go`. The compiled binary must be executable at `/home/user/classifier`.
   The binary will be invoked with a single argument: the path to a CSV file.
   `./classifier /path/to/data.csv`

   The CSV files have a header: `timestamp,value,notes`.
   
   Your program must read and parse the CSV according to RFC 4180 (it MUST correctly handle quoted fields containing embedded newlines).
   
   **Rejection Criteria** (exit code 1):
   - **Tokenization/Normalization**: Strip leading and trailing whitespace from the `notes` field. If the `notes` field of ANY row contains the exact `Reject Token` (case-sensitive) as a substring, the file is anomalous.
   - **Distance Computation**: Extract the first 5 valid rows from the CSV. Parse their `value` column as floats. Compute the Euclidean distance between these 5 values and the 5 values of the `Target Reference`. If the distance is strictly greater than `Max Euclidean Distance`, the file is anomalous. (If a file has fewer than 5 valid rows, consider it anomalous).

   **Acceptance Criteria** (exit code 0):
   - If the file does not trigger any of the rejection criteria, it is clean. The program must exit with code 0.

3. **Multi-stage Pipeline Orchestration**:
   Compile your Go program so the automated test suite can verify it against an internal adversarial corpus. The suite will test your binary against a `clean/` directory and an `evil/` directory.

To succeed, you must correctly parse the image, write robust CSV parsing in Go, and ensure your program exits with `0` for clean files and `1` for evil files.