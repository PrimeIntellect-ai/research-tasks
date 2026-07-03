You are a Machine Learning Engineer preparing training data for a predictive maintenance model. You are given high-frequency spatio-temporal vibration logs from an industrial beam. You must process this data to extract spectral features, validate them against a theoretical model, and compare them to a healthy baseline dataset.

Complete the following tasks:

1. **Environment Setup**:
   Create a Python virtual environment at `/home/user/ml_env`. Install `numpy`, `pandas`, and `scipy` inside it. Use this environment for all subsequent Python execution.

2. **Data Processing & Domain Decomposition**:
   A raw sensor reading file is located at `/home/user/data/sensor_readings.csv`.
   - The first column is `time` (in seconds).
   - The remaining 100 columns (`x_0` to `x_99`) represent spatial vibration measurements at equally spaced points along the beam.
   - Decompose the spatial domain into 4 equal segments: 
     - `seg_0` corresponds to `x_0` through `x_24`
     - `seg_1` corresponds to `x_25` through `x_49`
     - `seg_2` corresponds to `x_50` through `x_74`
     - `seg_3` corresponds to `x_75` through `x_99`
   - For each time step, calculate the mean signal across the spatial points within each segment. You will now have 4 aggregated time-series signals.

3. **Spectral Analysis**:
   - The data is sampled uniformly. Determine the sampling interval $\Delta t$ from the `time` column.
   - For each of the 4 aggregated segment signals, perform a Fast Fourier Transform (FFT) to find the **dominant frequency** (the frequency with the maximum amplitude). 
   - *Note*: Ignore the DC component (0 Hz) when finding the peak. Round the dominant frequency to 1 decimal place.

4. **Analytical Solution Validation**:
   - The theoretical fundamental frequency for the second segment (`seg_1`) under nominal conditions is exactly $f_{th} = 12.5$ Hz.
   - Create a boolean flag `is_valid_analytical` that is `true` if the dominant frequency of `seg_1` is within $\pm 1.0$ Hz of $f_{th}$, and `false` otherwise.

5. **Reference Dataset Comparison**:
   - A healthy baseline reference is located at `/home/user/data/baseline.json`. It contains the expected dominant frequencies for all 4 segments.
   - Calculate the absolute difference between your extracted dominant frequencies and the baseline frequencies for each segment. Round the differences to 1 decimal place.

6. **Output**:
   Write a single JSON file to `/home/user/training_features.json` with the exact following structure and calculated values:
   ```json
   {
     "dominant_frequencies": {
       "seg_0": <float>,
       "seg_1": <float>,
       "seg_2": <float>,
       "seg_3": <float>
     },
     "is_valid_analytical": <boolean>,
     "baseline_differences": {
       "seg_0": <float>,
       "seg_1": <float>,
       "seg_2": <float>,
       "seg_3": <float>
     }
   }
   ```