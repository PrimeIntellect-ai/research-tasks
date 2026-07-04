We are building a time-series ETL pipeline and have discovered a critical data leakage issue: our current scaling step applies `fit_transform` across the entire dataset, leaking future information into past data points. 

To fix this, the quantitative research team has designed an "Expanding Window Scaler". They left the mathematical specification for this scaler as an image file located at `/app/math_spec.png`.

Your task is to implement this mathematical specification exactly as a Python command-line tool.

Requirements:
1. Write a Python script at `/home/user/scaler.py`.
2. The script must read a single JSON array of floats from `stdin`.
3. It must apply the mathematical transformation exactly as specified in the image `/app/math_spec.png`.
4. It must output the transformed data as a JSON array of floats to `stdout`.
5. To avoid floating-point discrepancies across different environments, **round every float in your final output array to exactly 4 decimal places** using Python's built-in `round(val, 4)` before dumping to JSON.
6. The script should not print any additional text, debugging information, or logging to `stdout`—only the valid JSON array.

Please carefully read the formula in the image (you may need to use OCR or an image processing tool, `tesseract` is installed) and ensure your implementation matches it perfectly. Our testing framework will fuzz your script with thousands of random time-series arrays to verify exact equivalence against a reference implementation.