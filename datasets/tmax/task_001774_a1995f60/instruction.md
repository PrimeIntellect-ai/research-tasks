You are a data scientist analyzing the molecular vibrational spectrum of a novel compound. You need to combine theoretical graph-based predictions with noisy experimental spectroscopy data to fit and evaluate your model.

Your task consists of the following steps:

1. **Compile Scientific Software:**
   In `/home/user/workspace/`, there is a C source file `calc_peaks.c` and an edge list `molecule.edges` representing the molecular graph. 
   Compile `calc_peaks.c` into an executable named `calc_peaks` (it requires linking the math library). 
   Run it with `molecule.edges` as the only argument. It will output a set of theoretical peak wavenumbers based on the graph's structural properties. Keep the top 3 highest theoretical peak wavenumbers.

2. **Signal Processing on Experimental Data:**
   You have a file `/home/user/workspace/spectrum.csv` containing two columns: `Wavenumber` and `Intensity`. The signal is noisy.
   Write a script in your language of choice to:
   - Apply a 5-point centered moving average filter to the `Intensity` column. For a given index $i$, the smoothed value is the average of the intensities at indices $i-2$, $i-1$, $i$, $i+1$, and $i+2$. Leave the first two and last two points of the smoothed signal as NaN (or drop them).
   - Find all local maxima (peaks) in the smoothed signal. A point is considered a peak if its smoothed intensity is strictly greater than the smoothed intensities of the 2 points immediately before it and the 2 points immediately after it.
   - Select the 3 peaks with the highest smoothed intensity. Note their corresponding `Wavenumber` values.

3. **Model Evaluation:**
   - Sort both the 3 theoretical peak wavenumbers (from step 1) and the 3 experimental peak wavenumbers (from step 2) in ascending order.
   - Calculate the Mean Squared Error (MSE) between the sorted theoretical and experimental peaks: $\frac{1}{3} \sum_{k=1}^{3} (Theoretical_k - Experimental_k)^2$.

4. **Reporting and Visualization:**
   - Create a JSON file `/home/user/workspace/results.json` with the following structure:
     ```json
     {
       "theoretical_peaks": [val1, val2, val3],
       "experimental_peaks": [val1, val2, val3],
       "mse": 12.345
     }
     ```
     *(Make sure the lists are sorted in ascending order. Round all floats to 3 decimal places).*
   - Generate a plot named `/home/user/workspace/spectrum_plot.png` that overlays the raw `Intensity` (as points or a light line) and the smoothed `Intensity` (as a solid line) against `Wavenumber`. Add vertical dashed lines at the locations of the 3 theoretical peaks.

Ensure all outputs are exactly at the specified paths. You may write your processing script in Python, R, Julia, or any other language available in the environment.