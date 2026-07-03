You are acting as a bioinformatics analyst. We are tracking a rapidly mutating viral strain and need to design a diagnostic primer for the most conserved genomic region. 

We have isolated three candidate regions (Region A, Region B, and Region C). You are provided with a CSV file containing the mutation frequencies of these regions measured over several days: `/home/user/viral_samples.csv`. You also have the reference genome: `/home/user/reference.fasta`.

The mutation frequency $M(t)$ for a region follows a simple ODE model of mutation accumulation:
$dM/dt = k(1 - M)$
where $M(0) = 0$ at $t=0$, and $k$ is the region-specific mutation rate constant. 

Your task is to:
1. Write a Python script to estimate the parameter $k$ for each of the three regions by fitting the analytical solution or numerical integration of the ODE to the data in `/home/user/viral_samples.csv`. Use an optimization method (e.g., least squares) to find the best-fit $k$ for each region.
2. Identify the most conserved region (the one with the lowest $k$ value).
3. The regions correspond to the following 0-indexed intervals in the first sequence of `/home/user/reference.fasta`:
   - Region A: 100 to 200 (i.e., sequence[100:200])
   - Region B: 300 to 400
   - Region C: 500 to 600
4. Extract the sequence for the most conserved region. Within this 100-bp window, design a 20-bp forward primer.
5. The optimal primer is the contiguous 20-bp sequence within this region that has a GC content (percentage of G and C nucleotides) closest to 50.0%. If there is a tie for the closest GC content, choose the sequence that occurs first (lowest starting index) within the region window.
6. Export your final results to a JSON file at `/home/user/primer_report.json` with the following exact keys:
   - `"best_region"`: A string ("A", "B", or "C").
   - `"k_value"`: The optimized $k$ value for this region as a float, rounded to 4 decimal places.
   - `"primer_sequence"`: The 20-bp primer string (uppercase).
   - `"gc_content"`: The GC percentage of the primer as a float, rounded to 2 decimal places (e.g., 50.0).

Please generate the Python script, run it, and ensure the JSON file is created exactly as requested.