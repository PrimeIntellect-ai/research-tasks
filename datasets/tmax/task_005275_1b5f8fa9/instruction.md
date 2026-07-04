You are a data analyst tasked with processing messy IoT weather sensor data. You need to write a Rust program to clean the data, normalize it, and find correlations between sensors based on their temperature profiles and physical locations.

You have two input files:
1. `/home/user/locations.txt`: A messy field-notes text file containing the physical coordinates of the sensors.
2. `/home/user/readings.csv`: A CSV containing hourly temperature readings, but it has missing data points due to network drops.

Your objective is to write and run a Rust program in `/home/user/sensor_analysis/` that performs the following steps:

1. **Structured Extraction**: Parse `/home/user/locations.txt` to extract the sensor IDs and their (x, y) coordinates. The file contains narrative text, but you must extract the ID (e.g., `S1`) and the coordinates which are always written in the format `(x.x, y.y)`.
2. **Resampling & Gap-Filling**: Read `/home/user/readings.csv` (columns: `hour`, `sensor`, `temperature`). The `hour` column spans integers from 0 to 9, representing a 10-hour window. Some hours are missing for some sensors. You must create a complete 10-hour profile (hours 0 through 9) for each sensor using **forward fill** (if a reading for hour `h` is missing, use the value from the most recent available hour `< h`). You are guaranteed hour 0 is present for all sensors.
3. **Standardization**: Standardize the 10-hour temperature profile for each sensor independently. Calculate the Z-score for each hour's value: `z = (x - mean) / std_dev`. Use the *population* standard deviation $\sigma = \sqrt{\frac{\sum (x-\mu)^2}{10}}$.
4. **Distance & Similarity Computation**: 
   - Compute the Euclidean distance between the *standardized* temperature profiles of all pairs of sensors (A, B) where A < B alphabetically.
   - Also, compute the spatial Euclidean distance between the physical coordinates of those same pairs of sensors.
5. **Output**: Identify the pair of sensors that have the **most similar** temperature profiles (i.e., the *minimum* profile distance).
   Write the result to `/home/user/analysis_output.json` exactly in this format:
   ```json
   {
     "most_similar_profiles": ["S1", "S2"],
     "profile_distance": 0.1234,
     "spatial_distance": 1.2345
   }
   ```
   *Note: Round both distance values to exactly 4 decimal places.*

Create the Rust project, implement the logic, run it, and generate the final JSON file.