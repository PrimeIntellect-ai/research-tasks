You are an edge-computing data scientist. We have recently collected matrix multiplication inference performance logs from several edge devices, but the data is messy, spread across multiple files, and needs cleaning and statistical estimation strictly using Bash and core UNIX utilities (like `awk`, `join`, `sed`, `sort`, `bc`). 

Your objective is to write a Bash script `/home/user/process_benchmarks.sh` that processes this data.

**Input Files (Already exist):**
1. `/home/user/device_info.csv`: Contains device metadata.
   Headers: `DeviceID,Architecture,BaseMemory`
2. `/home/user/inference_logs.csv`: Contains raw benchmarking logs.
   Headers: `LogID,DeviceID,MatrixSize,InferenceTimeMS`

**Task Requirements:**

1. **Multi-source joining & cleaning:**
   - Join the two CSV files on `DeviceID`.
   - Filter out any rows where `MatrixSize` is $\le 0$ or `InferenceTimeMS` is $\le 0$.

2. **Tabular transformation & Linear algebra profiling:**
   - For valid rows, calculate the theoretical GigaFLOPS for standard matrix multiplication (assuming $C = A \times B$ where matrices are $N \times N$, so FLOPs $= 2 \times N^3$).
   - The formula for GigaFLOPS is: `(2 * MatrixSize^3) / (InferenceTimeMS * 10^6)`.
   - Create an output file `/home/user/metrics.csv` with comma-separated values and headers:
     `DeviceID,Architecture,MatrixSize,InferenceTimeMS,GigaFLOPS`
   - GigaFLOPS should be rounded to 3 decimal places.

3. **Bootstrap Estimation (Bash/awk):**
   - We need to estimate the mean GigaFLOPS specifically for the `ARM64` architecture.
   - Filter your cleaned metrics for `Architecture == "ARM64"`.
   - Write a routine (using `awk` inside your bash script is recommended) that performs **100 bootstrap samples** (random sampling *with replacement*) from the ARM64 rows. The size of each bootstrap sample must equal the total number of ARM64 rows.
   - For each bootstrap sample, compute the mean GigaFLOPS.
   - Calculate the grand mean of these 100 bootstrap sample means.
   - Save this single grand mean value (rounded to 3 decimal places) to `/home/user/bootstrap_arm64.txt`.

**Execution:**
Your script must be executable. When run via `./process_benchmarks.sh` without arguments, it should read the input files and produce `/home/user/metrics.csv` and `/home/user/bootstrap_arm64.txt`. Use standard POSIX/GNU tools. You are free to use `awk`'s `rand()` function for the sampling.

*Note:* Because random sampling implies variability, any output in `bootstrap_arm64.txt` that is within $\pm 1.5$ of the true population mean of the ARM64 data will be accepted by the verification test.