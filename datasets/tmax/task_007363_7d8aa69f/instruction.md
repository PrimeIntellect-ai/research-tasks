You are a data analyst working with IoT sensor data. You have received a raw dataset in `/home/user/raw_sensors.csv` containing time-series readings of temperature and humidity from various sensors. The data is noisy: it has missing rows (gaps in the expected 1-minute interval timestamps) and missing values (empty strings).

You need to build a C++ data processing pipeline to clean, impute, and extract features from this dataset.

**Task Requirements:**

Write and execute a C++ program (e.g., `process.cpp`, compile it, and run it) that reads `/home/user/raw_sensors.csv` and produces `/home/user/processed_sensors.csv`.

**Input Format (`/home/user/raw_sensors.csv`):**
A CSV with the header: `timestamp,sensor_id,temperature,humidity`
- `timestamp`: Integer Unix epoch time. The expected interval between readings is exactly 60 seconds.
- `sensor_id`: String identifier (e.g., "S1").
- `temperature`: Float (may be empty).
- `humidity`: Float (may be empty).

*Note: The first and last timestamp for each sensor will always have valid, non-empty temperature and humidity values.*

**Pipeline Steps:**
1. **Regularization & Imputation:** For each `sensor_id`, ensure there is a row for every 60-second interval between its minimum and maximum timestamp. If a timestamp is missing, or if `temperature` or `humidity` is empty, fill in the missing values using **linear interpolation** based on the nearest preceding and succeeding valid values for that sensor.
2. **Feature Extraction:** After imputation, calculate a **5-minute rolling average** for both temperature and humidity. The rolling average at time $T$ should be the arithmetic mean of the values at $T, T-60, T-120, T-180,$ and $T-240$. If fewer than 5 data points are available (i.e., near the start of a sensor's timeline), average all available points up to that time.
3. **Output Generation:** Write the final dataset to `/home/user/processed_sensors.csv`.

**Output Format (`/home/user/processed_sensors.csv`):**
Header: `timestamp,sensor_id,temperature,humidity,temp_rollavg,hum_rollavg`
- Sort the output primarily by `sensor_id` (alphabetically) and secondarily by `timestamp` (ascending).
- Print all floating-point numbers rounded to exactly **2 decimal places** (e.g., `21.50`).

Write the C++ program, compile it (you can use `g++ -O3 -std=c++17`), and run it to produce the final CSV.