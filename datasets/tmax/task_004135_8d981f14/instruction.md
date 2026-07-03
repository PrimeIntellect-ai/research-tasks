You are a data engineer building a C-based ETL pipeline. The pipeline ingests raw text, computes an embedding based on character frequencies, trains a simple prototype (centroid) model, and evaluates incoming data against this model with statistical confidence bounds to ensure pipeline stability.

You have been provided with a working directory `/home/user/etl` containing:
- `dataset_A.txt`: A set of baseline text records (training data).
- `dataset_B.txt`: A set of incoming text records (evaluation data).
- `embedder.c`: A C program that reads a text file and outputs 26-dimensional embeddings (normalized frequencies of characters a-z, case-insensitive, ignoring non-alphabetic characters) as comma-separated values.

Your task is to:
1. Compile `embedder.c` into an executable named `embedder`.
2. Process `dataset_A.txt` and `dataset_B.txt` using `embedder` to produce `embed_A.csv` and `embed_B.csv` respectively.
3. Write a new C program named `evaluate.c` in `/home/user/etl` that:
   - Reads `embed_A.csv` and computes the "centroid" (the element-wise mean vector across all rows). This represents our baseline "trained model".
   - Reads `embed_B.csv` and computes the Euclidean distance between *each* row's embedding and the centroid of A.
   - Calculates the overall mean Euclidean distance ($\mu$) and the sample standard deviation ($s$) of these distances across dataset B (use $N-1$ for sample standard deviation).
   - Computes the 95% Confidence Interval for the mean distance using the formula: $[\mu - 1.96 \cdot \frac{s}{\sqrt{N}}, \mu + 1.96 \cdot \frac{s}{\sqrt{N}}]$, where $N$ is the number of records in dataset B.
4. Compile `evaluate.c` and run it to produce a file named `/home/user/etl/metrics.txt` exactly matching this format:

```
Centroid_A_Dim0: <value>
Centroid_A_Dim25: <value>
Mean_Distance: <value>
Std_Dev: <value>
CI_95_Lower: <value>
CI_95_Upper: <value>
```
*Note: Print only Dim0 ('a') and Dim25 ('z') for the centroid. Format all floating-point numbers to exactly 6 decimal places (e.g., `%.6f`).*

Ensure your `evaluate.c` handles file I/O properly and compiles with standard libraries (`-lm` for math).