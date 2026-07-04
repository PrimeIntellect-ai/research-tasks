You are a performance engineer tasked with profiling a distributed signal processing workflow. We need to perform spectral analysis on a large dataset to identify the dominant frequency, and we want to test how the computation scales with multiple MPI processes.

Your task is to write a parallel Python script using `mpi4py` and a bash orchestration script to test its convergence and scaling.

Here are the specific steps:

1. A raw signal dataset will be located at `/home/user/data/signal.npy` (a 1D numpy array of `float64`, length 4,194,304). It represents a time-domain signal sampled at 1000 Hz.
2. Write an MPI-enabled Python script located at `/home/user/workspace/fft_mpi.py`. The script must:
   - Read the dataset (only rank 0 needs to read it and then scatter/broadcast, or all can read it and slice it, depending on your design, but ensure proper MPI data distribution where the array is split evenly among `N` ranks).
   - Each rank should compute the Fast Fourier Transform (FFT) magnitude of its local chunk using `numpy.fft.fft`.
   - Each rank identifies the index (relative to its local chunk) of the maximum FFT magnitude.
   - Gather all local maximum indices at rank 0.
   - Rank 0 should compute the mean of these indices and print exactly: `Average Peak Index: <mean_value>` (formatted to 2 decimal places).
3. Write a bash script at `/home/user/workspace/run_profiling.sh` that:
   - Uses `mpiexec` or `mpirun` to execute `fft_mpi.py` with 1, 2, and 4 processes.
   - Appends the output of each run to a log file at `/home/user/workspace/scaling_results.txt` in the exact format:
     `Cores: <N>, <Output from Python script>`
     (Example line: `Cores: 2, Average Peak Index: 42.00`)

Ensure the bash script is executable and run it to generate the final `scaling_results.txt` file.

Constraints:
- Do not use root privileges.
- Standard libraries, `numpy`, and `mpi4py` are available.