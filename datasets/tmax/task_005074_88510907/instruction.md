You are acting as a Data Engineer supporting a team of quantitative analysts. We have received a batch of sensor data in a CSV file, but the data pipeline that generated it had a bug, causing some mathematical constants to be written as unicode escape sequences instead of standard floats, and occasionally corrupting rows.

Your task is to write a Go program that processes this data in parallel, applies strict validation gates, extracts specific mathematical features, and writes the clean data to a new CSV file.

**Input Data Description:**
File location: `/home/user/data/raw_vectors.csv`
The CSV has two columns: `ID` (integer) and `VectorData` (string).
The `VectorData` column contains a JSON-formatted array of numbers represented as a string.

**Anomalies & Validation Checkpoints (Quality Gates):**
1. Due to a bug in the upstream JSON-lines parser, the mathematical constant Pi was serialized as the unicode escape sequence `\u03c0` instead of a float. Your Go program must intercept and replace this specific escape sequence in the JSON string with the float value `3.14159` before or during JSON unmarshaling.
2. **Quality Gate 1 (Parsing):** Any row where `VectorData` cannot be parsed into a valid slice of float64s (after fixing the `\u03c0` issue) must be completely discarded.
3. **Quality Gate 2 (Dimensionality):** Any row where the resulting vector has strictly less than 3 dimensions (length < 3) must be discarded.

**Feature Extraction Transforms:**
For each valid vector, calculate the following mathematical features:
1. **L2 Norm:** The Euclidean length of the vector (square root of the sum of the squared vector values).
2. **Population Variance:** The average of the squared differences from the Mean.

**Processing Requirements:**
- **Parallelism:** You must process the CSV rows concurrently using Go routines and channels. Do not process the rows sequentially.
- **Language:** The solution must be written entirely in Go. Save your source code to `/home/user/workspace/processor.go` and compile/run it.

**Output Specification:**
Create a new CSV file at `/home/user/data/features.csv`.
The file must have exactly this header: `ID,L2Norm,Variance`
The rows must be sorted in ascending order by `ID`.
Both `L2Norm` and `Variance` must be formatted to exactly 4 decimal places (e.g., `13.0000`).

Ensure all files and directories exist (create them if necessary in your shell before running your Go code).