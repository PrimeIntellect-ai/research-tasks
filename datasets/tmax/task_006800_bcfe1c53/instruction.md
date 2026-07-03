You are a Data Engineer building a quality assurance ETL pipeline for incoming IoT sensor data. 

The raw data is located at `/home/user/sensor_data.csv`. It contains readings from four sensors: `sensor_A`, `sensor_B`, `sensor_C`, and `sensor_D`.

Your task is to write a Python script `/home/user/etl_pipeline.py` that processes this data and creates a reproducible, cleaned dataset along with a summary report.

The pipeline must perform the following steps in order:

1. **Data Loading & Numerical Accuracy Check**:
   Load the CSV. Any sensor reading strictly outside the bounds of `[-100.0, 100.0]` is a physical impossibility. Replace any such out-of-bounds values with `NaN`. Drop any rows that contain `NaN` values.

2. **Correlation Analysis**:
   Calculate the Pearson correlation matrix for the four sensors. If any pair of sensors has an absolute correlation strictly greater than `0.90`, they are redundant. For every such highly correlated pair, drop the sensor column that comes *later* in alphabetical order (e.g., if A and B are correlated > 0.90, drop B).

3. **Bayesian Anomaly Detection**:
   For the *remaining* sensor columns (excluding dropped ones), you suspect some sensors may occasionally enter a "failure state". You need to flag these anomalies using Bayesian inference. 
   
   For every remaining reading $x$ in each sensor column, calculate the posterior probability of failure $P(\text{Failure} | x)$ using Bayes' theorem.
   
   Assume:
   - The prior probability of failure $P(\text{Failure}) = 0.05$.
   - The prior probability of normal operation $P(\text{Normal}) = 0.95$.
   - The likelihood of a reading given normal operation, $P(x | \text{Normal})$, follows a Normal distribution $\mathcal{N}(\mu=0, \sigma=10)$.
   - The likelihood of a reading given failure, $P(x | \text{Failure})$, follows a Uniform distribution over $[-100, 100]$, meaning the likelihood is $1/200 = 0.005$ everywhere in that range.
   
   If $P(\text{Failure} | x) > 0.5$, flag this specific reading as an anomaly. 
   Add a new column for each remaining sensor named `failure_flag_<sensor_name>` (e.g., `failure_flag_sensor_A`) containing `1` if flagged, and `0` otherwise.

4. **Output Generation**:
   - Save the fully processed dataframe (including the retained sensors and their new failure flag columns) to `/home/user/cleaned_data.csv` (include the header, do not include the index).
   - Generate a JSON report at `/home/user/report.json` with the following exact structure:
     ```json
     {
       "dropped_columns": ["list", "of", "dropped", "column", "names"],
       "total_anomalies": <integer_sum_of_all_1s_in_all_failure_flag_columns>
     }
     ```

Ensure your script is self-contained and uses standard data science libraries (pandas, numpy, scipy). Run your script to produce the output files.