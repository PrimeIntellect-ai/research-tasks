You are a Machine Learning Engineer preparing a training dataset of spectroscopic signals. The raw sensor data is noisy and contains varying background baseline drifts. You must clean the data, normalize it, and filter out highly corrupted samples by comparing them to a reference ideal spectrum.

Your task is to write a C program and accompanying shell pipeline to perform this data preparation.

**Raw Data Location**: 
- Raw samples: `/home/user/spectra_raw/` containing several CSV files (`sample_1.csv`, `sample_2.csv`, etc.).
- Reference ideal spectrum: `/home/user/reference_spectrum.csv`.
- Each CSV file has 100 rows. Each row contains two comma-separated float values: `wavelength,intensity`. Wavelengths are identical across all files.

**Processing Steps**:
For every sample in the raw directory, as well as the reference spectrum, perform the following mathematical steps in order:

1. **Baseline Correction**:
   - Extract the first point $(x_0, y_0)$ and the last point $(x_{99}, y_{99})$ of the spectrum.
   - Calculate a linear baseline equation $B(x) = m \cdot x + c$ that passes exactly through these two points.
   - Subtract this baseline from the entire signal: $S_{corrected}(x_i) = y_i - B(x_i)$.

2. **Floor Clipping**:
   - To avoid zero or negative values in subsequent probability calculations, if any $S_{corrected}(x_i) < 10^{-6}$, set it to $10^{-6}$.

3. **Normalization (Probability Distribution)**:
   - Normalize the corrected signal so that the sum of all intensities equals 1.0. Let's call this distribution $P$ for a sample, and $Q$ for the reference.
   - $P(x_i) = S_{corrected}(x_i) / \sum_{j=0}^{99} S_{corrected}(x_j)$.

4. **Filtering via Kullback-Leibler (KL) Divergence**:
   - Compute the KL divergence from the reference distribution $Q$ to the sample distribution $P$: 
     $D_{KL}(P \parallel Q) = \sum_{i=0}^{99} P(x_i) \log_e \left( \frac{P(x_i)}{Q(x_i)} \right)$
   - Use the natural logarithm (`log` in math.h).

**Requirements**:
1. Write your processing logic in C (`/home/user/processor.c`). You may use standard C libraries (`stdio.h`, `stdlib.h`, `math.h`, `string.h`).
2. Compile it using `gcc`.
3. Process all samples in `/home/user/spectra_raw/`.
4. Create an output log file at `/home/user/valid_samples.log`.
5. For every sample where the calculated $D_{KL} < 0.15$, append a line to `/home/user/valid_samples.log` in the exact format:
   `filename.csv,0.XXXXXX`
   *(where 0.XXXXXX is the KL divergence rounded to 6 decimal places, e.g., `sample_3.csv,0.041235`)*.
6. Sort the final `/home/user/valid_samples.log` alphabetically by filename.

Ensure your code handles the CSV parsing correctly and applies the baseline correction to both the reference spectrum and the raw samples before computing the KL divergence.