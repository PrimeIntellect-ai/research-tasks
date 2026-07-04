You are a performance engineer tasked with profiling a parallel scientific application to ensure it maintains numerical correctness when distributed across multiple nodes. You need to set up the environment, write a parallel data generator using MPI, compare its output to a reference dataset, and log the results.

Please perform the following steps:

1. **Environment Setup**:
   - Create a Python virtual environment at `/home/user/scienv`.
   - Activate it and install `mpi4py`, `numpy`, and `scipy`. 

2. **Parallel Implementation**:
   - Write an MPI script located at `/home/user/mpi_profiler.py`.
   - The script must be designed to run with exactly 4 MPI processes (`mpirun -np 4 python /home/user/mpi_profiler.py`).
   - In the script, each MPI rank must generate exactly 10,000 samples from a standard normal distribution (mean=0, std=1). 
   - You must use `numpy.random.default_rng(seed=rank)` for each process to ensure reproducible, rank-dependent generation (e.g., Rank 0 uses seed 0, Rank 1 uses seed 1, etc.).
   - Gather all generated samples from all ranks into a single flat array on Rank 0. The gathered array should contain 40,000 samples, ordered sequentially by rank (Rank 0's samples, then Rank 1's, etc.).

3. **Distribution Verification**:
   - There is a pre-existing reference dataset located at `/home/user/reference_data.txt`.
   - On Rank 0, load this reference dataset.
   - Calculate the 1D Wasserstein distance (using `scipy.stats.wasserstein_distance`) between the newly gathered 40,000 parallel samples and the reference dataset.

4. **Reporting**:
   - Rank 0 must write a JSON file to `/home/user/profiling_report.json` containing the calculated distance and the process count.
   - The JSON file must have exactly this format:
     ```json
     {
       "wasserstein_distance": <float>,
       "processes": 4
     }
     ```

Execute these tasks by creating the environment, writing the script, running it using `mpirun`, and ensuring the JSON report is generated successfully.