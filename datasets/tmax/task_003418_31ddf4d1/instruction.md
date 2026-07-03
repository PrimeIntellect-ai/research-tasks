I need you to complete a data processing pipeline for our research team. We have a set of raw text and numeric data, but the exact parameters for our statistical filters and tokenization thresholds were only provided to us as a screenshot of a presentation slide.

First, extract the data cleaning parameters from the image located at `/app/cleaning_parameters.png`. The image contains text specifying the alpha level for hypothesis testing, the outlier removal threshold (Z-score), and the minimum token frequency. 

Next, write a Python ETL script located at `/home/user/pipeline.py` that accepts exactly two arguments: an input CSV file path and an output JSON file path. The script must do the following:
1. Read the input CSV.
2. For the `numeric_val` column, calculate the mean and standard deviation, and remove any rows where the Z-score exceeds the threshold found in the image.
3. For the remaining rows, perform a one-sample t-test on `numeric_val` against a population mean of 0.0. If the p-value is strictly less than the alpha level found in the image, create a new boolean feature `is_significant` set to True; otherwise False.
4. For the `text_data` column, tokenize the text by splitting on whitespace and converting to lowercase. Remove any tokens that appear fewer times than the minimum token frequency (calculated across the entire remaining dataset). Join the surviving tokens back into a space-separated string.
5. Save the resulting data as a JSON list of dictionaries to the output file path.

Ensure your script is perfectly deterministic and runs without user interaction. It must be executable as `python /home/user/pipeline.py <input> <output>`.