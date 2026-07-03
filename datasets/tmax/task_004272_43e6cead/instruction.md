You are an algorithmic performance engineer. We have an audio processing pipeline that is failing and producing incorrect results. 

The pipeline consists of a Python script (`/app/processor.py`) that reads time intervals from a SQLite database (`/app/events.db`), extracts those intervals from an audio file (`/app/data.wav`), and calculates the RMS (Root Mean Square) power of the signal in each interval using a custom C extension.

Currently, the pipeline has several issues:
1. **Compilation Failure:** The C extension in `/app/c_src/` fails to compile and link. You need to fix the compiler/linker errors in `/app/setup.py` or the C code itself.
2. **Buffer Overflow/Crash:** Even when forced to compile, the C extension occasionally causes a segmentation fault on specific intervals due to an out-of-bounds array access.
3. **Formula Error:** The C extension calculates the power incorrectly (it does not implement the RMS formula properly).
4. **Query Bug:** The SQL query in `processor.py` has a logic error that causes it to fetch duplicate intervals, severely degrading performance.

Your task:
1. Fix the `setup.py` and C extension code so it compiles cleanly (`python3 setup.py build_ext --inplace`).
2. Correct the C code's memory issue and its RMS mathematical formula.
3. Fix the SQL query in `processor.py` so it strictly gets one unique `(start_sample, end_sample)` pair per `event_id`.
4. Run `python3 processor.py` to generate `/app/output.json`.

The final `/app/output.json` will contain a dictionary mapping `event_id` to the computed `rms_power` (a float). Automated tests will grade your submission by calculating the Mean Squared Error (MSE) between your output and the true RMS values. To pass, the MSE must be less than `0.001`.