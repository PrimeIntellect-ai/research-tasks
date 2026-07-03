You are an IT support technician responding to an escalated ticket (Ticket #4928). 

**Ticket Details:**
"Our Predictive Pipeline script is crashing. It processes daily batch data from our sensors, but the containerized job has been failing for the last two days. We checked the logs, and it seems to be failing on certain edge-case data, but we also noticed some encoding errors in the logs right before the math errors. Please investigate and fix the pipeline."

**Environment:**
- The application resides in `/home/user/app/`.
- The main script is `/home/user/app/processor.py`.
- The input data files (JSON format) are located in `/home/user/app/data/`.
- The logs from the last failed run are in `/home/user/app/logs/pipeline.log`.

**Your Tasks:**
1. **Diagnose the Crashes:** Inspect the logs and the script. The script is currently failing to process all files in the `data` directory. 
2. **Fix Serialization/Encoding Errors:** Some data files are failing to load due to encoding and serialization mismatches. Modify `/home/user/app/processor.py` to robustly handle these files. You may find that some files are encoded in UTF-16, while others are UTF-8. The script needs to automatically handle both and parse the JSON.
3. **Fix Numerical Instability:** Once the data is loaded, the math operations in the `compute_activation` function are crashing with `OverflowError` on certain extreme edge-case data points. Fix the function so it is numerically stable and never overflows (e.g., implement a mathematically equivalent stable version of the sigmoid function).
4. **Run the Pipeline:** After fixing `processor.py`, execute it. It takes no arguments and processes all `.json` files in the `data` directory.
5. **Output Verification:** The script writes its successful results to `/home/user/app/output.json`. Make sure this file is generated successfully and contains all processed keys.

**Constraints:**
- Do not change the underlying mathematical intent of the `compute_activation` function (it is a standard sigmoid function). Just make it mathematically stable for all float inputs.
- You must use Python.
- Do not modify the input files in `/home/user/app/data/`; you must fix the code to handle them.