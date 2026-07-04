You are a data scientist tasked with cleaning a large dataset of sensor readings using a pre-trained linear autoencoder. The dataset contains noisy anomalies that must be filtered out. You will need to write a C++ program to perform model inference, calculate reconstruction errors, use bootstrap sampling to robustly determine an anomaly threshold, and generate a clean dataset.

**Setup:**
All files are located in `/home/user/data/`. All binary files use 32-bit floating-point numbers (`float` in C++) in little-endian format.
- `raw_data.bin`: The uncleaned dataset containing 100,000 records. Each record is a vector of 10 `float` values (i.e., 1,000,000 floats in total).
- `encoder_weights.bin`: A 5x10 weight matrix (5 rows, 10 columns, row-major order).
- `decoder_weights.bin`: A 10x5 weight matrix (10 rows, 5 columns, row-major order).
- `bias.bin`: A bias vector of 10 `float` values.

**Phase 1: Model Inference & Error Calculation**
Write a C++ program that reads the data and model weights. For each 10-dimensional input vector $x$ from `raw_data.bin`:
1. Encode: $h = W_{enc} \times x$
2. Decode: $\hat{x} = (W_{dec} \times h) + b$
3. Calculate the reconstruction error: $E = \sum_{i=1}^{10} (x_i - \hat{x}_i)^2$
*(Note: standard matrix multiplication applies).*

**Phase 2: Bootstrap Threshold Estimation**
To determine a stable anomaly threshold $T$, use bootstrap resampling on the 100,000 computed error values:
1. Initialize a Mersenne Twister RNG (`std::mt19937`) with the seed `42`.
2. Perform 1,000 bootstrap iterations.
3. In each iteration, draw a sample of 10,000 error values **with replacement** from the full set of 100,000 errors. Use `std::uniform_int_distribution<int>(0, 99999)` for the indices.
4. Sort the sampled 10,000 errors in ascending order.
5. Find the 95th percentile of the sample, defined strictly as the value at index `9500` (0-indexed).
6. The final anomaly threshold $T$ is the **mean** of these 1,000 95th percentile values.

**Phase 3: Data Cleaning & Reporting**
1. Filter the original records. A record is considered "clean" if its reconstruction error $E \le T$.
2. Write the clean records (the original 10-float vectors) sequentially to `/home/user/data/clean_data.bin`.
3. Write a report to `/home/user/data/summary.txt` with exactly two lines:
   - Line 1: The threshold $T$, formatted to exactly 4 decimal places.
   - Line 2: The total number of clean records.

**Requirements:**
- You must use C++ to perform these operations to handle the large-scale data efficiently. You may use any standard C++17 library features.
- Compile your code using `g++ -O3`.
- Ensure exact implementation of the random sampling logic, as the seed guarantees a deterministic threshold.