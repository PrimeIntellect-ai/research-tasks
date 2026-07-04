You are a performance engineer tasked with profiling a distributed scientific computing pipeline. The pipeline performs domain decomposition, adaptive mesh refinement, and MCMC sampling for posterior estimation.

You have been given a profiling trace log file located at `/home/user/trace.log`.
Each line in the log file represents a completed operation and contains four space-separated columns:
`TIMESTAMP MODULE RANK DURATION`

- `TIMESTAMP`: The time the operation completed.
- `MODULE`: The component of the pipeline (e.g., `MCMC_SAMPLER`, `MESH_REFINE`, `DOMAIN_DECOMP`).
- `RANK`: The MPI rank (an integer) that executed the operation.
- `DURATION`: The time taken for the operation in milliseconds (an integer).

Your task is to analyze this log using standard Linux command-line tools (like `awk`, `grep`, `sort`, etc.) to find the following:
1. Identify the `RANK` that spent the **maximum total time** (sum of durations) in the `MCMC_SAMPLER` module.
2. For that specific bottleneck rank, calculate the **average duration** of its `MESH_REFINE` operations.

Write the final result to a file named `/home/user/bottleneck.txt` in the exact following format:
```
Target Rank: <rank>
Average MESH_REFINE Duration: <average_rounded_to_2_decimal_places>
```

Example output format:
```
Target Rank: 5
Average MESH_REFINE Duration: 145.67
```

Ensure the average is strictly formatted to two decimal places.