You are an MLOps engineer tasked with building a mathematical pipeline in Go to process text datasets, reduce their dimensionality, and track inference performance and artifacts. 

We are developing a custom, lightweight text embedding model. You need to implement the data processing and matrix operations using Go, specifically utilizing the `gonum.org/v1/gonum/mat` package.

Here are your instructions:

1. **Workspace Setup**:
   Create a directory `/home/user/mlops`. Initialize a Go module named `mlops` in this directory and install the required `gonum` package.

2. **Pipeline Implementation**:
   Write a Go program at `/home/user/mlops/pipeline.go` that performs the following steps:
   
   * **Tokenization & Feature Extraction**: Read the text file `/home/user/corpus.txt`. For each line, compute a 26-dimensional feature vector representing the frequency of each English letter ('a' through 'z', case-insensitive). Ignore any non-alphabetic characters. This creates an $N \times 26$ feature matrix $X$, where $N$ is the number of lines.
   
   * **Dimensionality Reduction**: We have a pre-generated random projection matrix stored at `/home/user/projection.csv`. This file contains 26 rows and 5 columns (comma-separated floats). Read this file into a $26 \times 5$ matrix $P$.
   
   * **Inference / Matrix Multiplication**: Multiply the feature matrix by the projection matrix to get the reduced embeddings: $Y = X \times P$. 
   *Benchmarking requirement:* You must measure the execution time of **only** this specific matrix multiplication step (using Go's `time` package).
   
   * **Artifact Storage**: Save the resulting $N \times 5$ matrix $Y$ to `/home/user/mlops/artifacts/reduced.csv`. Ensure the `artifacts` directory is created. Format the output as comma-separated values, with each float formatted to exactly 4 decimal places (e.g., `%.4f`).
   
   * **Metrics Reporting**: Create a JSON file at `/home/user/mlops/benchmark.json` containing the benchmarking results in this exact format:
     ```json
     {
       "lines_processed": <integer N>,
       "duration_ns": <integer time in nanoseconds>
     }
     ```

3. **Execution**:
   Run your Go program so that the artifacts and benchmark files are successfully generated.