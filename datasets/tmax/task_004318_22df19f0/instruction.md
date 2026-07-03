You are an AI assistant helping a data science researcher organize and validate a new experimental dataset. 

The researcher has an experimental video recording located at `/app/experiment_record.mp4`. Unfortunately, due to a recording glitch (similar to a misconfigured plotting backend that spits out blank images), many frames in this video are corrupted and appear as nearly uniform or blank images.

We need to build a robust statistical feature extraction script that filters out these corrupted frames and extracts key statistical features (including confidence intervals) for the valid frames.

Your task has two parts:

**Part 1: Create the Feature Extraction Script**
Write a Python script at `/home/user/analyze_frame.py` that takes exactly one argument (the file path to an image frame) and prints a comma-separated list of five statistical features to standard output.

The script must do the following:
1. Open the image using the `PIL` (Pillow) library and convert it to grayscale using `.convert('L')`.
2. Convert the image to a flattened NumPy array of floats. Let `N` be the total number of pixels.
3. Calculate the population `mean`, population standard deviation (`std`, with `ddof=0`), and `median` of the pixel intensities.
4. **Outlier/Missing Value Handling:** If the `std` is strictly less than `5.0`, consider this a corrupted "blank" frame. In this case, the script must print exactly: `0.00,0.00,0.00,0.00,0.00` and exit.
5. **Confidence Intervals:** For valid frames (`std` >= 5.0), compute the 95% confidence interval for the mean. Use the standard normal distribution approximation:
   `ci_lower = mean - 1.96 * (std / sqrt(N))`
   `ci_upper = mean + 1.96 * (std / sqrt(N))`
6. Print the results to stdout as exactly 5 comma-separated values in this order: `mean,std,median,ci_lower,ci_upper`. Format each value to exactly two decimal places using standard float formatting (e.g., `"{:.2f}".format(val)`). Do not print anything else.

**Part 2: Process the Video**
1. Extract the frames from `/app/experiment_record.mp4` at exactly 1 frame per second (1 fps).
2. Run your `/home/user/analyze_frame.py` script on each extracted frame.
3. Count how many frames are valid (i.e., they do NOT output the `0.00,0.00,0.00,0.00,0.00` outlier string).
4. Write this single integer count to a file located at `/home/user/valid_frames.txt`.

Ensure your script is strictly deterministic and perfectly follows the mathematical formulas and formatting rules provided, as it will be heavily tested against random inputs.