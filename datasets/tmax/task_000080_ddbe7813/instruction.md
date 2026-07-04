You are a log analyst investigating a recent system degradation. You have two sparse log files from different subsystems that you need to merge and normalize into a single, second-by-second timeline.

The two input files are located at:
1. `/home/user/temperature.csv`: Contains intermittent temperature readings.
   Format: `timestamp,temperature` (where timestamp is an integer second, and temperature is a float).
2. `/home/user/state.csv`: Contains system state changes.
   Format: `timestamp,state` (where timestamp is an integer second, and state is a string).

Both logs start at timestamp `1` and end at timestamp `15`. 

Your task is to write a C program at `/home/user/processor.c` that performs the following data processing steps:
1. **Resample and Join**: Generate a continuous timeline for every second from `1` to `15` (inclusive), joining data from both files on the `timestamp`.
2. **Interpolate**: For the `temperature` values, perform strict **linear interpolation** for missing timestamps between the known data points. 
3. **Impute/Gap-fill**: For the `state` strings, perform **forward-filling** (use the last known state for missing timestamps).
4. **Output**: Write the joined, interpolated, and gap-filled data to `/home/user/merged.csv`.

**Output Format Rules:**
- The output file must be a CSV with no header line.
- Each line must be formatted exactly as `timestamp,temperature,state`.
- Format the temperature to exactly one decimal place (e.g., `%.1f`).
- Do not add extra spaces.

Once you have written `/home/user/processor.c`, compile it using `gcc /home/user/processor.c -o /home/user/processor` and run it to generate `/home/user/merged.csv`.