You are a data engineer tasked with fixing a critical data leakage bug in a machine learning ETL pipeline. 

A former engineer built a C++ command-line tool that performs Bayesian target encoding on categorical features. Unfortunately, the source code was lost, and all we have is the compiled, stripped binary located at `/app/leaky_target_encoder`. 

We recently discovered that this binary is causing data leakage: it computes the encoding statistics (global mean, category means, and category counts) over the *entire* input dataset before the train-test split, inflating our downstream inference performance metrics.

Your task is to write a replacement C++ program that performs the exact same Bayesian target encoding, but strictly prevents data leakage by computing statistics *only* on the training data.

### Instructions:
1. **Reverse-Engineer the Oracle:** 
   The binary `/app/leaky_target_encoder` takes two arguments: an input CSV and an output CSV path. 
   Input format: `id,category,target` (header included).
   The encoding follows the standard Bayesian smoothing formula:
   $E = \frac{n \times \bar{x}_c + m \times \bar{x}_g}{n + m}$
   Where:
   - $n$ = count of the category
   - $\bar{x}_c$ = mean of the target for the category
   - $\bar{x}_g$ = global mean of the target
   - $m$ = an unknown prior smoothing weight (an integer)
   Use the binary as a black-box oracle to discover the exact smoothing weight $m$ used by the former engineer.

2. **Build the Fixed ETL Pipeline:**
   Write a new C++ program at `/home/user/fast_etl.cpp`.
   It must compile with `g++ -O3 -std=c++17 /home/user/fast_etl.cpp -o /home/user/fast_etl`.
   It should take two command-line arguments: `train.csv` and `test.csv` (in that order).
   
   Your program must:
   - Read `train.csv` (format: `id,category,target`) and calculate the global mean, category counts, and category means.
   - Read `test.csv` (format: `id,category,target`).
   - Apply the Bayesian target encoding (using the $m$ you discovered) to both datasets, using *only* the statistics learned from `train.csv`.
   - If a category in `test.csv` was never seen in `train.csv`, its encoded value should just be the global mean from `train.csv`.
   - Output two files in the current working directory: `train_encoded.csv` and `test_encoded.csv`.
   - The output CSVs must contain exactly two columns: `id,encoded_target`, preserving the original row order and including the header. Encode as a float/double with standard precision.

3. **Performance Benchmarking:**
   The downstream inference engine requires the ETL to be extremely fast. Write clean, efficient C++ code. The automated verification will test your compiled program against a hidden dataset.