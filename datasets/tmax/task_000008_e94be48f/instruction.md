You are a data scientist working on a sensor network. You need to clean and join two datasets using a high-performance C program, as the real datasets will be massive.

The datasets are located in `/home/user/data/`:
1. `sensors.csv`: Contains sensor metadata.
   Format: `sensor_id,location,calibration_factor`
2. `readings.csv`: Contains raw sensor readings.
   Format: `timestamp,sensor_id,raw_value,status`

Your task is to write a C program at `/home/user/clean_join.c` that performs the following steps:
1. **Tokenization & Schema Enforcement**: Parse both CSV files (ignoring the header rows). 
   - `sensor_id` must parse as an unsigned 32-bit integer (`uint32_t`).
   - `calibration_factor` and `raw_value` must parse as single-precision floats (`float`).
   - `timestamp` must parse as an unsigned 64-bit integer (`uint64_t`).
   - `status` is a string up to 7 characters.
   - If any field fails to parse correctly or is missing, drop that record.
2. **Multi-source Data Joining**: Join the readings with the sensors on `sensor_id`. If a reading's `sensor_id` does not exist in `sensors.csv`, drop the reading.
3. **Numerical Accuracy Testing**: Calculate the `adjusted_value` for each joined reading as `raw_value * calibration_factor`. The `adjusted_value` must be strictly greater than `0.0` to be considered valid. If it is `<= 0.0` or NaN, drop the reading.
4. **Large-scale Data Storage**: Write the valid, joined records into a binary file `/home/user/data/cleaned.bin`. The binary file should contain sequentially written structs defined exactly as follows (no padding issues expected on standard x86_64, but ensure it matches this layout):

```c
#include <stdint.h>

struct CleanedRecord {
    uint64_t timestamp;
    uint32_t sensor_id;
    float adjusted_value;
    char status[8];
};
```
Make sure `status` is null-terminated or padded with null bytes up to 8 chars.

Finally, write a bash script `/home/user/process.sh` that compiles your C program (using `gcc`), runs it, and then writes the total number of successfully joined and valid records to `/home/user/data/summary.txt`.

Ensure your scripts and code are robust. Run `/home/user/process.sh` to generate the final `cleaned.bin` and `summary.txt`.