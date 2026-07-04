You are an AI assistant helping a data researcher organize a high-dimensional dataset of sensor readings. 

The researcher has raw data and a pre-trained linear projection model (which reduces dimensionality), but the pipeline to process and classify this data has been lost. You need to reconstruct this pipeline in **Rust**.

Here is what you have:
1. `/home/user/data/raw_sensor.csv`: A CSV file containing 50 rows of raw sensor data. It has no header. The first column is the integer `id`, followed by 10 float columns representing the high-dimensional features.
2. `/home/user/data/model_weights.json`: A JSON file containing a 2D array (10 rows, 2 columns) representing the extracted weights of a dimensionality reduction model.

Your task is to create a reproducible Rust pipeline that does the following:

**1. Dimensionality Reduction (Model Reconstruction)**
Read the raw data and the model weights. For each row's 10-dimensional feature vector $X$ (shape: $1 \times 10$), multiply it by the model weights matrix $W$ (shape: $10 \times 2$) to get a 2-dimensional reduced vector $Z = X \cdot W$.

**2. Probabilistic Modeling (Bayesian Classification)**
We have two known classes with bivariate Gaussian priors in the reduced 2D space. Both classes have an identity covariance matrix $\Sigma = I$.
- Class 0 Prior Mean: $\mu_0 = [0.0, 0.0]$
- Class 1 Prior Mean: $\mu_1 = [2.0, -2.0]$

For each reduced vector $Z = [z_1, z_2]$, compute the log-likelihood (ignoring the constant normalization term for simplicity) for both classes:
$LL_k = -0.5 \times ((z_1 - \mu_{k,1})^2 + (z_2 - \mu_{k,2})^2)$

Assign each data point to the class (0 or 1) that yields the maximum log-likelihood.

**3. Reproducible Pipeline Construction**
- Create a Rust Cargo project named `sensor_pipeline` inside `/home/user/`.
- Write the Rust code to perform the steps above. You may use external crates like `csv` and `serde_json` in your `Cargo.toml`.
- The Rust program must write the results to `/home/user/data/classified_results.csv`.
- The output CSV must have a header: `id,class,max_ll`
- `max_ll` should be the maximum log-likelihood value, rounded to 4 decimal places.
- Create a shell script `/home/user/run_pipeline.sh` that, when executed, builds the Rust project (using `cargo build --release`) and runs the binary to produce the output file.

Execute your script to ensure `/home/user/data/classified_results.csv` is correctly generated.