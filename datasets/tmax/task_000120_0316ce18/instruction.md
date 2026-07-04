You are a data engineer troubleshooting a legacy ETL pipeline. A critical upstream sensor malfunctioned, inserting `NaN` values into our primary dataset instead of integers. This "silent" corruption broke our downstream Bash-based mathematical modeling tools, which only expect integers.

Fortunately, a field engineer dictated the missing values into an audio log when the automated system failed. 

Your task is to repair the dataset, compute statistical models purely using Bash/Awk (no Python/R allowed for the core logic), and predict missing values for a new evaluation set.

Here are your detailed instructions:

1. **Audio Data Recovery:**
   - An audio file containing the missing telemetry is located at `/app/backup_log.wav`.
   - We have provided an offline transcription tool at `/usr/local/bin/transcriber`. It takes a single argument (the path to the `.wav` file) and outputs the transcript to standard output.
   - The transcript contains phrases like "At timestamp 1450, the value is 42." Extract these timestamp-value pairs.

2. **Data Imputation:**
   - The corrupted dataset is at `/app/raw_data.csv` (Header: `Timestamp,SensorA,SensorB`).
   - Replace any `NaN` values in `SensorA` with the correct integer values extracted from the audio transcript based on the `Timestamp`.
   - Save the cleaned, valid dataset to `/home/user/clean_data.csv`.

3. **Statistical Modeling (Linear Regression & Correlation):**
   - Using *only* standard Linux command-line tools (like `awk`, `sed`, `grep`, `bc`, `datamash`), compute the linear regression line predicting `SensorB` from `SensorA`.
   - Calculate the slope ($m$) and y-intercept ($c$) where $SensorB = m \times SensorA + c$. 
   - Calculate the Pearson correlation coefficient ($r$) between `SensorA` and `SensorB`.
   - Write these three values to `/home/user/model_stats.txt` in the format:
     ```
     Slope: <value>
     Intercept: <value>
     Correlation: <value>
     ```

4. **Prediction:**
   - You are provided an evaluation dataset at `/app/eval_data.csv` (Header: `Timestamp,SensorA`).
   - Using your derived slope and intercept, predict `SensorB` for each row in the evaluation dataset.
   - Save your predictions to `/home/user/predictions.csv`. The file must contain exactly two columns, no spaces: `Timestamp,PredictedSensorB`. Include the header.

Constraints:
- You must write your logic in Bash, Awk, or standard shell utilities. Do not use Python or R for the imputation or modeling steps. 
- Ensure your math retains at least 4 decimal places of precision during intermediate calculations.