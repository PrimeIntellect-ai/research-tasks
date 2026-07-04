You are a data scientist taking over a data cleaning pipeline. The previous engineer wrote a pandas script to process a dataset of high-frequency sensor readings, but the script is producing incorrect covariance matrices due to a silent data type conversion bug.

The pipeline processes `/home/user/sensor_data.csv`, which contains four columns: `timestamp_ns`, `sensor_A`, `sensor_B`, and `sensor_C`. 

The current script (`/home/user/process_data.py`) looks like this:
```python
import pandas as pd
import numpy as np

def process_and_compute():
    # Load data
    df = pd.read_csv('/home/user/sensor_data.csv')
    
    # Clean data: replace missing value placeholders and convert to float
    df = df.replace('MISSING', np.nan)
    df = df.astype(float)
    
    # Drop rows with missing timestamps
    df = df.dropna(subset=['timestamp_ns'])
    
    # Aggregate duplicate timestamps by taking the mean of the sensors
    df_grouped = df.groupby('timestamp_ns').mean()
    
    # Compute the covariance matrix of the aggregated sensors
    cov_matrix = df_grouped[['sensor_A', 'sensor_B', 'sensor_C']].cov()
    
    # Calculate the sum of all elements in the covariance matrix
    cov_sum = cov_matrix.to_numpy().sum()
    
    with open('/home/user/cov_sum.txt', 'w') as f:
        f.write(f"{cov_sum:.4f}\n")

if __name__ == "__main__":
    process_and_compute()
```

**The Problem:**
The `timestamp_ns` column contains nanosecond-resolution epoch timestamps (e.g., `1680000000000000001`). Because the previous engineer used `.astype(float)` to handle the `NaN` values introduced by the missing data placeholder, pandas converts the 64-bit integers into IEEE 754 64-bit floats. This causes catastrophic precision loss (float64 can only perfectly represent integers up to $2^{53}-1$). Distinct timestamps are being silently rounded to the same floating-point value, improperly grouping unrelated sensor readings together and skewing the covariance matrix.

**Your Task:**
1. Install any necessary numerical libraries.
2. Fix the `/home/user/process_data.py` script. You must prevent the `timestamp_ns` column from losing precision while still correctly handling the `'MISSING'` strings in the dataset.
3. Drop any rows where `timestamp_ns` is `'MISSING'`.
4. Ensure `timestamp_ns` remains a perfect 64-bit integer equivalent (or nullable pandas `Int64`) so the `groupby` operation groups *only* exact nanosecond matches.
5. The sensor columns (`sensor_A`, `sensor_B`, `sensor_C`) should be treated as standard floats.
6. Compute the covariance matrix of the three sensor columns on the grouped data, and save the sum of all elements in the covariance matrix to `/home/user/cov_sum.txt` formatted to exactly 4 decimal places.

Run your fixed script to produce the final `/home/user/cov_sum.txt`.