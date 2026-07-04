You are acting as an MLOps engineer building a lightweight, high-performance artifact tracking suite in C and Bash. You have a set of experiment logs in `/home/user/experiments/`. 

Your task is to build a two-part pipeline:
1. **ETL Extraction (Bash):** Write a bash script `/home/user/extract.sh` that reads all `run_*.csv` files in `/home/user/experiments/`. Each file contains columns `epoch,loss,accuracy,latency_ms`. The script must extract the final epoch's `accuracy` and `latency_ms` for each run, and output a single compiled file `/home/user/summary.csv` with the format `run_id,final_accuracy,final_latency`. The `run_id` should be the filename without the `.csv` extension (e.g., `run_1`). Sort the output alphabetically by `run_id`. Do not include a header row in the output file.

2. **Analysis Tool (C):** Write a C program `/home/user/analyze_runs.c` and compile it to `/home/user/analyze_runs` (use `gcc -O2 -o analyze_runs analyze_runs.c -lm`). The program must support two modes via command-line arguments:
   - **Similarity Search:** `./analyze_runs similarity <csv_file> <target_accuracy> <target_latency>`
     This mode reads the parsed CSV and finds the run most similar to the target metrics. 
     Use this exact distance formula to penalize latency and accuracy differences equally: 
     `Distance = ((accuracy - target_accuracy) * 100)^2 + (latency - target_latency)^2`
     Print ONLY the `run_id` of the closest match to standard output.
   - **Bayesian Update:** `./analyze_runs bayes <prior_prob> <likelihood_success> <likelihood_failure>`
     MLOps tracking often involves updating the probability of a model's production readiness based on new artifact tests (e.g., a stress test). Calculate the posterior probability of readiness using Bayes' theorem:
     `Posterior = (prior * likelihood_success) / ((prior * likelihood_success) + ((1 - prior) * likelihood_failure))`
     Print ONLY the resulting posterior probability as a float formatted to 4 decimal places (e.g., `0.8521`) to standard output.

**Execution:**
Once your tools are written:
1. Run `/home/user/extract.sh` to generate `/home/user/summary.csv`.
2. Find the most similar run to a target accuracy of `0.91` and latency of `135`, saving the output to `/home/user/best_match.txt`.
3. An experiment artifact passed a stress test. The historical prior of readiness is `0.30`. The likelihood of passing this test if truly ready is `0.95`. The likelihood of passing if NOT ready is `0.10`. Calculate the posterior probability and save the output to `/home/user/posterior.txt`.