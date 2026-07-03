You are a data analyst tasked with processing a dataset of system logs. Because performance is critical, you must write the processing pipeline in C++.

Your environment does not have root access, but you need to use the Eigen library for matrix operations.

1. **Dependency Installation**:
   Download the Eigen 3.4.0 source code to `/home/user/eigen.tar.gz` and extract it so that the headers are accessible at `/home/user/eigen/Eigen/Dense` (you may need to rename the extracted directory to `/home/user/eigen`). The URL is `https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz`.

2. **Data Preparation & Schema Enforcement**:
   You have been provided three files in `/home/user/data/`:
   - `logs.csv`: Contains columns `id`, `timestamp`, `message`.
   - `vocab.txt`: Contains one vocabulary word per line.
   - `projection.csv`: A comma-separated projection matrix (rows = vocabulary size, columns = 2).
   
   Write a C++ program at `/home/user/process_logs.cpp` that reads `logs.csv`. 
   - Skip the header row.
   - **Enforce Schema**: Discard any row where the `id` field cannot be parsed as a strictly valid integer.
   - **Tokenization**: For valid rows, convert the `message` to lowercase and split it into tokens by space.
   - Create a Bag of Words (BoW) vector for each valid message using the exact vocabulary order in `vocab.txt`. The vector should count the occurrences of each vocabulary word in the message.

3. **Dimensionality Reduction**:
   Use Eigen to multiply the BoW matrix (N rows x V vocab size) by the projection matrix (V rows x 2 columns) loaded from `projection.csv`. This reduces your sparse text vectors to 2-dimensional continuous embeddings.

4. **Bootstrap Sampling**:
   Focus on the **first dimension** (index 0) of the resulting projected data.
   Perform non-parametric bootstrap sampling to estimate the 95% confidence interval of the mean of this first dimension.
   - Use `std::mt19937 gen(42);` as your exact random number generator.
   - Use `std::uniform_int_distribution<> dis(0, N - 1);` to sample row indices with replacement.
   - Draw `N` samples per iteration (where `N` is the number of valid rows).
   - Perform 10,000 iterations.
   - Save the mean of each iteration.
   - Sort the means and extract the 2.5th percentile (index 250) and 97.5th percentile (index 9750).

5. **Output**:
   Write the resulting lower and upper bounds of the confidence interval to `/home/user/output/ci.txt` in the format:
   `Lower: <value>, Upper: <value>` (formatted to 4 decimal places).

Compile your code using `g++ -O3 -I/home/user/eigen/ /home/user/process_logs.cpp -o /home/user/process_logs` and run it to produce the final output file.