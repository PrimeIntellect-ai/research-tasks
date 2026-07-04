You are acting as a data scientist cleaning a messy dataset of sensor readings. You have been given a dataset in a "wide" format that contains missing values. You need to write a C++ program to reshape the data, impute missing values, process the sensors in parallel, and generate formatted text reports.

The input data is located at `/home/user/sensor_data_wide.csv`. 
The format is: `sensor_id,t_0,t_1,t_2,...,t_99`. 
Missing values are represented by the string `NaN`.

Your objective is to write and execute a C++ program (saved as `/home/user/clean_data.cpp`) that performs the following steps:

1. **Wide-to-Long Reshaping:**
   Read the CSV and convert it into a "long" format dataset in memory, where each record represents a single time point for a sensor (i.e., `sensor_id`, `time_index`, `value`). 

2. **Interpolation and Imputation:**
   For each sensor, replace `NaN` values using linear interpolation between the nearest valid data points. 
   - If `NaN` values appear at the very beginning of the series, replace them with the first valid value (Next Observation Carried Backward).
   - If `NaN` values appear at the very end, replace them with the last valid value (Last Observation Carried Forward).
   - For `NaN` values in the middle, use standard linear interpolation: `V_t = V_start + (V_end - V_start) * (t - t_start) / (t_end - t_start)`.

3. **Parallel Data Processing:**
   The imputation and report generation for each sensor MUST be processed in parallel using standard C++ threading (`std::thread`, `std::async`, or parallel execution policies). 

4. **Output 1: Cleaned Data CSV:**
   Save the fully imputed, long-format data to `/home/user/cleaned_long_data.csv`. 
   The file must have the header `sensor_id,time_index,value` and the values must be formatted to 4 decimal places. The rows should be sorted by `sensor_id` (alphabetically) and then by `time_index` (ascending integer, 0 to 99).

5. **Output 2: Template-based Text Generation:**
   Create a directory `/home/user/reports/`.
   For each sensor, generate a text file named `/home/user/reports/sensor_<sensor_id>_report.txt` using the exact template below.

   Template:
   ```
   Report for Sensor: [sensor_id]
   Total Data Points: 100
   Imputed Points: [count of NaN values imputed for this sensor]
   Average Value: [average of all 100 points post-imputation, 4 decimal places]
   Max Value: [maximum value post-imputation, 4 decimal places]
   ```

Requirements:
- Use C++17 or C++20.
- Compile your program using `g++ -std=c++17 -pthread /home/user/clean_data.cpp -o /home/user/clean_data`.
- Execute the compiled program.