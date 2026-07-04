You are assisting a researcher who needs to run a set of Monte Carlo data generation scripts and perform basic statistical analysis and density estimation entirely within the Linux terminal using Bash. 

A data generator script has been provided at `/home/user/generate_data.sh`. It takes a single integer as an argument (a random seed) and outputs a 1000-row, 10-column CSV file named `/home/user/data_<seed>.csv` containing values between 0 and 100.

Your task is to write a Bash script at `/home/user/analyze.sh` that performs the following steps:
1. **Parallel Execution:** Execute `/home/user/generate_data.sh` four times concurrently using background processes (seeds: 1, 2, 3, and 4). Your script must wait for all four background jobs to complete before proceeding.
2. **Data Aggregation:** Concatenate the four resulting CSV files (in order of seed 1, 2, 3, 4) into a single file at `/home/user/combined.csv`.
3. **Statistical Comparison:** Process `combined.csv` to calculate the difference between the mean of Column 2 and the mean of Column 1 (`Mean(Col2) - Mean(Col1)`). Save this exact result, formatted to exactly 3 decimal places, to `/home/user/diff.txt`.
4. **Density Estimation:** Extract Column 3 from `combined.csv` and compute a histogram with 5 equal bins: [0, 20), [20, 40), [40, 60), [60, 80), and [80, 100]. (If a value is exactly 100, include it in the final bin). Save the counts to `/home/user/hist.txt`, with each bin's count on a new line (5 lines total, representing the bins in ascending order).

Make sure `/home/user/analyze.sh` has executable permissions and run it so that the final output files (`/home/user/combined.csv`, `/home/user/diff.txt`, and `/home/user/hist.txt`) are generated.