You are an AI assistant acting as a Data Scientist. We have a raw dataset of sensor readings from our manufacturing floor that needs to be cleaned and analyzed to determine if there is a statistically significant difference between two machine types (Type A and Type B). 

Because our production servers only allow the execution of bash scripts for automated cron jobs, you must write a single executable Bash script located at `/home/user/analyze_sensors.sh` that performs the entire end-to-end pipeline.

Your Bash script must perform the following tasks when executed:
1. **Dependency Installation**: Ensure any necessary Python packages for data analysis (e.g., `pandas`, `numpy`, `scipy`, `scikit-learn`) are installed locally for the user. (You may use `pip3 install --user` or create a virtual environment within the script).
2. **Data Cleaning**: Read the input dataset at `/home/user/data/sensor_readings.csv`. The dataset contains the columns: `machine_id`, `machine_type` ('A' or 'B'), `sensor1`, `sensor2`, `sensor3`, and `sensor4`. Remove any rows containing missing or NaN values in any column.
3. **Linear Algebra (Dimensionality Reduction)**: Use Principal Component Analysis (PCA) on the cleaned numerical sensor columns (`sensor1` through `sensor4`) to extract the first principal component (PC1).
4. **Hypothesis Testing**: Perform an independent two-sample Welch's t-test (unequal variances) on the PC1 values to test the null hypothesis that Type A and Type B machines have the same population mean for PC1.
5. **Reporting**: The bash script must output exactly two lines to a file located at `/home/user/analysis_report.txt` in the following format (rounding values to exactly 4 decimal places):

```text
PC1_Variance_Ratio: 0.XXXX
T-Test_P-Value: 0.XXXX
```

Requirements:
- Your final deliverable is the creation of `/home/user/analyze_sensors.sh`.
- The script must be executable (`chmod +x`).
- Running the script should automatically create `/home/user/analysis_report.txt` with the correct metrics. 
- You may embed Python code within your Bash script using heredocs (e.g., `python3 -c ...` or `python3 << 'EOF' ... EOF`).