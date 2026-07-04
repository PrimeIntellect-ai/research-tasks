You are a performance engineer tasked with optimizing and profiling a spatial-genomics pipeline. The current pipeline analyzes sequences across a 2D spatial grid, but it is entirely sequential and too slow.

Your goal is to write a highly parallelized Bash script that implements domain decomposition to speed up the primer sequence alignment and feeds the aggregated results into a provided Markov Chain Monte Carlo (MCMC) posterior estimation tool.

Here are the details of the environment and your task:
1. **Input Data**: You have a CSV file at `/home/user/spatial_reads.csv` (which already exists). It has no header. The columns are `X,Y,Sequence` where X and Y are floating point coordinates between 0.0 and 100.0, and Sequence is a DNA string.
2. **Domain Decomposition**: Divide the data into 4 spatial quadrants:
   - Q1: X <= 50.0 and Y <= 50.0
   - Q2: X > 50.0 and Y <= 50.0
   - Q3: X <= 50.0 and Y > 50.0
   - Q4: X > 50.0 and Y > 50.0
3. **Primer Alignment**: In each quadrant, count how many sequences contain the exact primer sequence `GATTACA`. 
   - **Crucial Performance Requirement**: You must process these 4 quadrants *in parallel* in your Bash script (e.g., using background processes `&` and `wait`).
4. **Aggregation & MCMC Estimation**: Once all 4 background processes finish, sum the exact match counts from all quadrants. Pass this total sum as the single positional argument to the existing MCMC sampler script located at `/home/user/mcmc_sampler.sh`.
5. **Output**: Save the exact standard output of `/home/user/mcmc_sampler.sh` to `/home/user/final_posterior.txt`.

Write your completed pipeline script to `/home/user/run_pipeline.sh` and make sure it is executable. You should then run it so that `/home/user/final_posterior.txt` is generated. 

Do not modify `/home/user/mcmc_sampler.sh` or `/home/user/spatial_reads.csv`. Rely purely on standard Bash utilities (`awk`, `grep`, `sed`, `&`, `wait`, etc.) inside your script.