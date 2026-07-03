I am a researcher organizing a large collection of datasets. I need to build a small data processing pipeline to calculate the probability that my datasets are "clean" (uncorrupted) based on some heuristics, and I need to ensure the pipeline is reproducible and numerically stable.

Please write a Go program and a Bash script to handle this workflow.

1. **The Go Program (`/home/user/bayes_check.go`)**:
   Create a Go program that reads a CSV file located at `/home/user/dataset_stats.csv`. 
   The CSV will have a header and four columns: `dataset_id`, `prior_clean`, `likelihood_clean`, `likelihood_corrupt`.
   
   For each dataset, calculate the Posterior Probability that the dataset is Clean using Bayes' Theorem:
   `Posterior_Clean = (likelihood_clean * prior_clean) / ((likelihood_clean * prior_clean) + (likelihood_corrupt * (1 - prior_clean)))`

   The program should output the results to standard output, one dataset per line, in this exact format:
   `<dataset_id>,<posterior_clean>`
   
   Ensure that the `posterior_clean` value is formatted to exactly 6 decimal places (e.g., `0.987097`).

2. **The Pipeline Script (`/home/user/run_pipeline.sh`)**:
   Write a bash script that performs the following reproducibility and numerical checks:
   - Compiles the Go program.
   - Runs the compiled binary and saves the output to `/home/user/results.txt`.
   - Runs the compiled binary a second time and saves the output to `/home/user/results2.txt`.
   - Compares the two result files to ensure pipeline reproducibility. If the files are exactly identical, append the string `Reproducible: YES` to `/home/user/pipeline.log`. If they differ, append `Reproducible: NO`.
   - To test numerical accuracy across the pipeline, use `awk` to calculate the sum of all the `posterior_clean` values from `/home/user/results.txt`. Append the sum to `/home/user/pipeline.log` in the format `Sum: <sum>` (also rounded/formatted to 6 decimal places).

Make sure the bash script is executable. You do not need to create the CSV file; assume it already exists at `/home/user/dataset_stats.csv`. Once you've created both files, execute `/home/user/run_pipeline.sh` so I can verify the final `pipeline.log`.