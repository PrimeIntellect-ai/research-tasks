You are an automation specialist tasked with creating a text-matching pipeline.

We receive batches of comma-separated value files in `/home/user/incoming/`. Each line in these files contains a pair of words separated by a comma (e.g., `apple,apply`).

Your task is to:
1. Write a C++ program at `/home/user/compute_dist.cpp` that takes an input file path and an output file path as command-line arguments. It must read the word pairs from the input file, compute the Levenshtein (edit) distance for each pair, and write the results to the output file in the format: `word1,word2,distance`. 
Since the real files are large, your C++ program must use parallel data processing (e.g., OpenMP or C++ `std::thread`/`std::async`) to compute the distances concurrently. Compile this program to `/home/user/compute_dist`.
2. Write a bash script at `/home/user/run_pipeline.sh` that iterates over all `.csv` files in `/home/user/incoming/`. For each file, it should run `/home/user/compute_dist` to process it, save the output to `/home/user/outgoing/` with the exact same filename, and then delete the original file from `/home/user/incoming/`. Make sure the script is executable.
3. Schedule a cron job for the current user that executes `/home/user/run_pipeline.sh` exactly every 15 minutes.

Do not run the pipeline script yourself; just set up the C++ program, the shell script, and the cron job. Ensure that all paths are absolute and the C++ program handles standard ASCII strings.