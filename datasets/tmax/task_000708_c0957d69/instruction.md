You are a data analyst tasked with building a reproducible data processing pipeline that detects anomalous datasets based on correlation analysis.

You have been provided with an image file at `/app/specs.png` which contains the data quality specifications, specifically the minimum acceptable Pearson correlation coefficient between two metrics. 

Your task is to write a Bash script at `/home/user/analyze.sh` that takes a single argument: the path to a directory. 
Each directory passed to your script will contain two files:
- `table1.csv` (columns: `user_id`, `metric_x`)
- `table2.csv` (columns: `user_id`, `metric_y`)

Your script must:
1. Join the two datasets on the `user_id` column.
2. Compute the Pearson correlation coefficient between `metric_x` and `metric_y` across the joined records.
3. Extract the minimum acceptable correlation threshold from the text inside the `/app/specs.png` image (you may install and use tools like `tesseract-ocr` to read the image).
4. Evaluate the computed correlation against the threshold:
   - If the computed correlation is **strictly less than** the threshold, the dataset is considered anomalous ("evil"). Your script must exit with status code `1`.
   - If the computed correlation is **greater than or equal to** the threshold, the dataset is considered valid ("clean"). Your script must exit with status code `0`.

Requirements:
- Your script must be written in Bash (`#!/bin/bash`), though you may call Python, `awk`, `join`, or other command-line tools from within it to handle the mathematical computation and data joining.
- Ensure your script is executable (`chmod +x /home/user/analyze.sh`).
- Do not hardcode the threshold in your script; it must be extracted programmatically or read accurately. 

The evaluation system will test your script against multiple hidden directories containing clean and anomalous datasets to verify its accuracy.