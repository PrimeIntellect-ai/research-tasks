You are a performance engineer working on a scientific data processing pipeline. You have been given raw observational data and a legacy C application that processes this data. Your goal is to reshape the observational data, orchestrate a profiling workflow using a Jupyter notebook, and identify the main performance bottleneck in the C application.

Here are the requirements for the task:

1. **Observational Data Reshaping**: 
   You have a raw dataset at `/home/user/raw_sensor_data.csv` with columns `timestamp,sensor_id,value`. 
   Write a script to extract only the rows where `sensor_id` is exactly `42`. Sort these rows in ascending order based on the `timestamp`. Extract the `value` column from these sorted rows and save it as a flat, uncompressed binary file of 64-bit IEEE 754 floats (`double` in C) at `/home/user/filtered_signal.bin`.

2. **C Application Profiling Preparation**:
   The source code for the scientific processing engine is located at `/home/user/signal_processor.c`. 
   Compile this C code into an executable named `signal_processor` at `/home/user/signal_processor`. You must compile it such that it includes profiling instructions suitable for `gprof`. Disable any compiler optimizations (use `-O0`).

3. **Notebook-based Workflow Orchestration**:
   Create a Jupyter Notebook file located at `/home/user/profile_workflow.ipynb`. This notebook must contain cells that programmatically execute the following sequence:
   - Run the compiled `./signal_processor` executable, passing `/home/user/filtered_signal.bin` as the only command-line argument.
   - Run `gprof` on the executable and its generated profiling output (`gmon.out`), redirecting the human-readable report to `/home/user/profile_results.txt`.
   - Parse `/home/user/profile_results.txt` to identify the name of the function that consumes the highest percentage of time. 
   - Write ONLY the exact name of this slowest function (e.g., `main` or `compute_fft`) to `/home/user/slowest_function.txt`. No extra whitespace or characters.

4. **Execution**:
   Once your notebook is complete, execute it programmatically in the terminal using `jupyter nbconvert --execute /home/user/profile_workflow.ipynb`. 

Ensure all packages needed (like `jupyter`, `nbconvert`, `build-essential`) are installed if not already present. You have `sudo` privileges if needed to install packages via `apt` or `pip`. The final success condition relies on `/home/user/filtered_signal.bin` having the correct binary data, and `/home/user/slowest_function.txt` containing the correct function name determined by the notebook orchestration.