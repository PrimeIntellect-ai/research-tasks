You are a data engineer responsible for building an ETL pipeline that processes multi-dimensional embeddings.

You have been provided with a raw dataset located at `/home/user/raw_data.csv`.
The file is a CSV without spaces, formatted as:
`id,category,v1,v2,v3,v4,v5`

Your objective is to create an automated pipeline that filters the data, performs stratified sampling using a C++ program, calculates mathematical distances, and outputs the result.

Please perform the following steps:

1. **Pipeline Orchestrator (`/home/user/pipeline.sh`)**:
   Create a bash script named `/home/user/pipeline.sh`. This script will orchestrate your pipeline as a Simple DAG.
   - **Step 1:** The bash script must first filter `/home/user/raw_data.csv` to remove the header row, and filter out any rows where the `category` is exactly the string `IGNORE`. Save this intermediate file to `/home/user/clean_data.csv`.
   - **Step 2:** The bash script should compile your C++ program (described below) using `g++ -std=c++17 -O3 -o /home/user/processor /home/user/processor.cpp`.
   - **Step 3:** The bash script should execute the compiled C++ program.

2. **C++ Processor (`/home/user/processor.cpp`)**:
   Write a C++ program that reads `/home/user/clean_data.csv` line-by-line (simulating a large-file stream to avoid memory exhaustion on massive files).
   - **Stratified Sampling:** For each unique `category`, retain only the **first 2** records encountered in the file. Any subsequent records for a category that already has 2 samples must be ignored.
   - **Distance Computation:** For the sampled records, calculate the Manhattan distance ($L_1$ norm) between the 5-dimensional vector `(v1, v2, v3, v4, v5)` and the fixed reference vector `R = (1.0, -1.0, 1.0, -1.0, 1.0)`. The Manhattan distance between two vectors $A$ and $B$ is the sum of the absolute differences of their components: $\sum |A_i - B_i|$.
   - **Output:** The C++ program must write its results to `/home/user/final_output.csv`.
     - The output file must include a header: `id,category,distance`
     - The output rows must be sorted primarily by `category` (alphabetically, ascending), and secondarily by `distance` (ascending).
     - The `distance` must be formatted to exactly **3 decimal places** (e.g., `2.500`).

Ensure that all scripts are executable. Once you have created `/home/user/pipeline.sh` and `/home/user/processor.cpp`, run your bash script to produce `/home/user/final_output.csv`.