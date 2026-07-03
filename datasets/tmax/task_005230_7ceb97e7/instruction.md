As a machine learning engineer, I am preparing a synthetic dataset of molecular network features for a graph neural network. I have written a C program that generates random network topologies and uses Monte Carlo simulations to estimate the average random walk hitting time between nodes. 

The source code is located at `/home/user/ml_data/network_mc.c`.

I need you to complete the data generation pipeline:
1. Compile the C source file into an executable named `generate_features` in the same directory. You may need to link standard libraries (like the math library) depending on standard C practices.
2. Write a bash script at `/home/user/ml_data/run_all.sh` that automates the data generation.
3. The script should loop through random seeds from `101` to `150` (inclusive).
4. For each seed, execute `./generate_features <seed>` and append the output to `/home/user/ml_data/training_data.csv`.
5. Run your bash script to produce the final dataset.

The final CSV file `/home/user/ml_data/training_data.csv` should contain exactly 50 lines, each with the seed and the corresponding computed feature. Make sure the script is executable and the task is fully completed when you finish.