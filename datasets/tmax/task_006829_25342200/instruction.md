You are a data engineer tasked with building a robust ETL pipeline in Rust. A common pitfall in data science is "data leakage," where information from the test set leaks into the training process (e.g., computing normalization statistics over the entire dataset before splitting).

Your objective is to write a Rust application that processes a dataset, performs bootstrap sampling, applies feature scaling without leaking data, and tracks experiment metrics.

**Task Steps:**

1. **Setup:**
   Initialize a new Rust project at `/home/user/etl_pipeline`.
   You are provided with a raw dataset at `/home/user/data/raw.csv` containing a header `f1,f2,target` and 100 rows of data.

2. **Train/Test Split:**
   Read the CSV. Assign the first 80 rows (excluding the header) to the Training set, and the remaining 20 rows to the Test set.

3. **Bootstrap Sampling:**
   Create an augmented, bootstrapped training set of exactly 80 rows by sampling the original 80 training rows *with replacement*. 
   To ensure strict reproducibility for this task, use the following Linear Congruential Generator (LCG) algorithm to pick the indices instead of a random crate:
   - Modulus: $m = 2^{31}$
   - Multiplier: $a = 1103515245$
   - Increment: $c = 12345$
   - Seed: $X_0 = 42$
   - For $i = 1$ to $80$:
     $X_i = (a \cdot X_{i-1} + c) \pmod m$
     $\text{Index} = \lfloor X_i / 65536 \rfloor \pmod{80}$
   Use these 80 indices to pull rows from the original training set.

4. **Feature Engineering (Avoiding Data Leakage):**
   - Calculate the mean and population standard deviation (dividing by $N$, not $N-1$) for features `f1` and `f2` **only** on the bootstrapped training set.
   - Apply Z-score normalization: $x_{scaled} = \frac{x - \mu}{\sigma}$ to `f1` and `f2` for BOTH the bootstrapped training set and the test set using the $\mu$ and $\sigma$ derived from the bootstrapped training set. Leave `target` unmodified.

5. **Experiment Tracking:**
   Create an experiment log at `/home/user/experiment_log.json` containing the calculated statistics and tracking metrics. The JSON must exactly match this structure (round all floating-point numbers to 4 decimal places):
   ```json
   {
     "train_f1_mean": 0.0000,
     "train_f1_std": 0.0000,
     "train_f2_mean": 0.0000,
     "train_f2_std": 0.0000,
     "test_f1_mean_after_scaling": 0.0000,
     "test_f2_mean_after_scaling": 0.0000
   }
   ```
   *Note: `test_f1_mean_after_scaling` is the mean of `f1` in the test set AFTER the scaling has been applied.*

6. **Output Generation:**
   Save the scaled bootstrapped training set to `/home/user/data/train_scaled.csv` and the scaled test set to `/home/user/data/test_scaled.csv` (keep the `f1,f2,target` header format).
   Run your Rust application to generate the outputs.

Make sure your Rust project can be built and run using standard `cargo` commands within the `/home/user/etl_pipeline` directory.