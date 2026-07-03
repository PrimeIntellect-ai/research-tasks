Hello! I am a researcher organizing some datasets, and I need your help building a reproducible data processing pipeline in Bash. 

I have an image file containing important preprocessing parameters and model coefficients from a previous study. The image is located at `/app/model_params.png`. Please use OCR (Tesseract is available) to read the contents of this image. It contains:
1. The default imputation value for missing data in column 2.
2. The outlier threshold for column 3 (any value greater than this should be clamped to the threshold).
3. The weights for a linear combination of column 2 and column 3 to produce a final score.

Your task is to write a Bash script at `/home/user/pipeline.sh` that takes exactly one argument (a CSV string formatted as `id,col2,col3`) and prints a single processed CSV string formatted as `id,processed_col2,processed_col3,final_score`.

The pipeline must perform the following:
- Parse the input CSV string.
- If `col2` is empty or exactly `NaN`, replace it with the imputation value extracted from the image.
- If `col3` is strictly greater than the outlier threshold extracted from the image, clamp it to the threshold.
- Compute the `final_score` by multiplying the processed `col2` and `col3` by their respective weights extracted from the image, and adding them together. Use `awk` or `bc` for floating-point math, rounding the final score to 2 decimal places.
- Print the result to stdout.

The script must be executable (`chmod +x /home/user/pipeline.sh`). Make sure the output format exactly matches `id,processed_col2,processed_col3,final_score`.