You are a performance engineer investigating a spectroscopy simulation tool that is reportedly producing non-reproducible results. The simulation is supposed to generate a synthetic absorption spectrum, but scientists are complaining that the exact peak of the spectrum shifts slightly between runs, breaking their automated calibration pipelines.

You suspect the issue is caused by floating-point non-associativity combined with a non-deterministic reduction order in the tool's multi-threaded C code.

Your task is to empirically prove this by compiling the tool, collecting data, performing signal processing to locate the peaks, and running a statistical hypothesis test.

Here are your instructions:

1. **Compile the Simulation**:
   A C source file is located at `/home/user/spectro_sim.c`.
   Compile it using GCC with OpenMP support enabled (`-fopenmp`). Name the output binary `/home/user/spectro_sim` and link the math library (`-lm`).

2. **Generate Data**:
   Run the compiled `/home/user/spectro_sim` 100 times. Each run outputs 1000 floating-point numbers (one per line) representing the spectral intensities across 1000 wavelength bins. Save the output of each run to a directory `/home/user/sim_data/` (e.g., `run_0.txt` to `run_99.txt`).

3. **Analyze the Data (Write `/home/user/analyze.py`)**:
   Write a Python script that reads all 100 runs. For each run:
   - Treat the line index (0 to 999) as the x-axis (wavelength bin).
   - Treat the floating-point value as the y-axis (intensity).
   - Fit a smoothing spline to the data using `scipy.interpolate.UnivariateSpline` with a smoothing factor (`s`) of `0.5`.
   - Find the exact peak location (a floating-point x-value) by finding the roots of the first derivative of the spline. Keep the root that corresponds to the global maximum of the spline in the domain [0, 999].
   
   Once you have the 100 peak locations, calculate:
   - The mean peak location.
   - The variance of the peak locations.
   
   Finally, use `scipy.stats.shapiro` to perform a Shapiro-Wilk test on the 100 peak locations to determine if the non-deterministic floating-point errors result in a normally distributed peak shift.

4. **Generate Report**:
   Your Python script must create a file at `/home/user/report.json` containing exactly the following JSON structure:
   ```json
   {
       "mean_peak": <float>,
       "variance_peak": <float>,
       "shapiro_statistic": <float>,
       "shapiro_p_value": <float>,
       "is_reproducible": <boolean>
   }
   ```
   *Note: Set `is_reproducible` to `true` if `variance_peak` is exactly `0.0`, otherwise `false`.*

Run your workflow and ensure `/home/user/report.json` is generated correctly.