You are a machine learning engineer preparing spatial training data for a Physics-Informed Neural Network (PINN). The initial dataset contains scattered sensor readings, but certain regions of the spatial domain have high variance and require mesh refinement (over-sampling) before training. 

Your task is to implement a Python pipeline that performs domain decomposition, evaluates region variance using bootstrap confidence intervals, over-samples the high-variance regions, and computes the distributional shift caused by this refinement.

**Step 1: Environment Setup**
You will need `numpy`, `pandas`, and `scipy`. Install them in your environment. An initial dataset is located at `/home/user/initial_data.csv` with columns `x`, `y`, and `value`. The spatial domain is bounded by `x` in `[0, 1]` and `y` in `[0, 1]`.

**Step 2: Domain Decomposition & Bootstrap Analysis**
Write a Python script that does the following:
1. Set the random seed: `numpy.random.seed(42)`
2. Decompose the `[0, 1] x [0, 1]` domain into a 4x4 uniform grid (16 sub-domains). A point `(x, y)` belongs to grid cell `(i, j)` where `i = min(int(x * 4), 3)` and `j = min(int(y * 4), 3)`. The sub-domain index is `i * 4 + j`.
3. For each of the 16 sub-domains, calculate the 95% bootstrap confidence interval (CI) of the **mean** of the `value` column for the points in that sub-domain.
   - Use exactly 1000 bootstrap resamples.
   - Calculate the sample mean for each resample.
   - The 95% CI is defined by the 2.5th and 97.5th percentiles of the bootstrap means (use `numpy.percentile`).
4. Calculate the width of this CI (97.5th percentile - 2.5th percentile).

**Step 3: Mesh Refinement**
If a sub-domain has a CI width strictly greater than `0.2`, it requires refinement.
For each sub-domain requiring refinement (processed in order of their index 0 to 15):
1. Generate 50 new points.
2. The `x` coordinates should be drawn from a uniform distribution bounded by the sub-domain's x-limits: `[i*0.25, (i+1)*0.25)`.
3. The `y` coordinates should be drawn from a uniform distribution bounded by the sub-domain's y-limits: `[j*0.25, (j+1)*0.25)`.
4. The `value` for each new point should be randomly sampled (with replacement) from the *original* points located in that specific sub-domain.

**Step 4: Distribution Distance**
Combine the original dataset and all newly generated points into a single refined dataset.
Calculate the Wasserstein distance (using `scipy.stats.wasserstein_distance`) between the `value` array of the *original* dataset and the `value` array of the *final refined* dataset.

**Output Requirements**
1. Save the combined final dataset to `/home/user/refined_data.csv` (keeping columns `x, y, value`).
2. Generate a JSON report at `/home/user/report.json` with exactly these keys:
   - `"refined_subdomains"`: A list of integers (the indices of the sub-domains that were refined, in ascending order).
   - `"wasserstein_distance"`: A float representing the calculated 1D Wasserstein distance.
   - `"final_point_count"`: An integer representing the total number of points in the final dataset.