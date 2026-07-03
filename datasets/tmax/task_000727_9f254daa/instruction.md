You are a machine learning engineer preparing a training dataset. Some of the feature tensors (saved as `.npy` files) in your data pipeline have been corrupted by anomalies. You need to write a data sanitization script to filter out these corrupted files.

Your task is to create a Python script at `/home/user/filter.py` that processes a single `.npy` file and determines whether it should be accepted or rejected based on strict statistical criteria.

Here are your instructions:
1. **Extract Specifications**: We have provided an image containing the statistical thresholds for the filter at `/app/spec_chart.png`. You must use OCR (e.g., `tesseract`, which is installed) or another computer vision tool to read the text in this image. The image specifies two constraints:
   - The maximum allowed absolute Pearson correlation coefficient between any two *distinct* features.
   - The minimum allowed p-value from a two-sided 1-sample t-test (testing if the population mean of a feature is exactly 0.0).

2. **Implement the Filter**: 
   Write `/home/user/filter.py` such that it takes exactly one command-line argument: the path to a `.npy` file.
   - The `.npy` file contains a 2D numpy array of shape `(N_samples, D_features)`.
   - Your script must compute the Pearson correlation matrix. If the absolute correlation between *any* two distinct features is strictly greater than the threshold from the image, the file must be rejected.
   - Your script must perform a two-sided 1-sample t-test for each of the `D` features. If the p-value for *any* feature is strictly less than the threshold from the image, the file must be rejected.
   - The script must be optimized using `numpy` and `scipy` to ensure it runs efficiently for benchmarking purposes (under 200ms per file).

3. **Output Behavior**:
   - If the file passes both checks, your script must exit with status code `0` (ACCEPT).
   - If the file fails one or both checks, your script must exit with status code `1` (REJECT).
   - You can print whatever you like to standard output; only the exit code will be evaluated.

Make sure your code is robust and handles numerical precision reasonably.