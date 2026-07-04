You are a machine learning engineer working on a C pipeline to analyze transaction data. We want to estimate the 95% confidence interval of the difference in normalized transaction amounts between two user groups (Group B - Group A) using the bootstrap method. 

However, we must avoid a common "data leakage" pitfall: standardizing the entire dataset *before* bootstrapping. Proper procedure requires standardizing the data *within* each bootstrap sample using that sample's own mean and standard deviation.

**Your Tasks:**

1. **Multi-source Data Joining**: 
   You are provided with two files in `/home/user/`:
   - `users.csv`: Contains `user_id` and `group` ('A' or 'B').
   - `transactions.csv`: Contains `user_id` and `amount` (float).
   Join these datasets on `user_id`. Only keep users that exist in both files (inner join). Each user has exactly one transaction.

2. **Bootstrap and Hypothesis Testing Pipeline in C**:
   Write a C program at `/home/user/bootstrap.c` that performs the following steps on the joined data:
   - Perform `B = 10000` bootstrap iterations.
   - For each iteration, draw a bootstrap sample of size `N` (where `N` is the total number of joined records) with replacement.
   - **Crucial Step (avoiding leakage)**: Calculate the mean and population standard deviation (divide by `N`, not `N-1`) of the `amount` *for the current bootstrap sample only*.
   - Standardize the amounts in the bootstrap sample using this sample mean and sample standard deviation: `z = (amount - sample_mean) / sample_std`.
   - Calculate the difference in the mean of the standardized amounts between Group B and Group A: `diff = mean(z_Group_B) - mean(z_Group_A)`. (If a group is missing in a sample, treat its mean as 0).
   - Store this difference.

3. **Confidence Interval**:
   - Sort the 10,000 differences in ascending order.
   - Calculate the 95% confidence interval using the percentile method. The lower bound is the 2.5th percentile (index `250` for 0-indexed array) and the upper bound is the 97.5th percentile (index `9749`).
   - Write these two values, formatted to exactly four decimal places and separated by a comma, to `/home/user/ci.txt` (e.g., `-0.1234,0.5678`).

**Deterministic Random Sampling:**
To ensure your results are exactly reproducible, you **must** use the following custom PRNG for sampling, rather than the standard C `rand()`:
```c
#include <stdint.h>

uint32_t state = 42;
uint32_t xorshift32() {
    state ^= state << 13;
    state ^= state >> 17;
    state ^= state << 5;
    return state;
}
```
To draw a random index from `0` to `N-1`, use: `uint32_t idx = xorshift32() % N;`. Draw the `N` indices for each bootstrap sample in sequence.

Ensure your C program is compiled to an executable named `/home/user/bootstrap` and run it to produce the `ci.txt` file.