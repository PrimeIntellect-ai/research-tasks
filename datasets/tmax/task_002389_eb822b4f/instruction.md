You are a data analyst tasked with building an ETL sanitization pipeline for a new batch of sensor telemetry CSV files. Our downstream statistical models are highly sensitive to numerical instability, missing values, and adversarial data poisoning.

Your objective is to create a robust Python command-line tool at `/home/user/etl_pipeline.py` that processes a single CSV file, sanitizes it, and decides whether to accept or reject it based on strict numerical accuracy rules.

Here are the requirements:

1. **Rule Extraction (Image Processing):** 
   You have been provided with an image of a whiteboard containing the acceptable clamping ranges for our three sensor columns: `Alpha`, `Beta`, and `Gamma`. The image is located at `/app/validation_specs.png`. You must use a tool like Tesseract OCR to read these thresholds.

2. **ETL Pipeline & Data Sanitization:**
   Write a Python script `/home/user/etl_pipeline.py` that accepts arguments like this:
   `python /home/user/etl_pipeline.py --input <input_csv_path> --output <output_csv_path>`

   The script must read the input CSV and perform the following handling:
   - **Missing Values:** Impute any missing numerical values (empty cells or standard pandas NaNs) using the median of that column.
   - **Outlier Clamping:** Clamp any out-of-bounds values to the exact minimum and maximum acceptable bounds you extracted from the whiteboard image.

3. **Adversarial Detection (Accept/Reject):**
   The script must protect the pipeline from "evil" CSVs designed to break our numerical models. 
   - **Reject:** If any column in the CSV contains a value whose absolute magnitude is greater than 10 times the absolute maximum bound for that specific sensor (as defined in the image), or if a column contains structural anomalies (e.g., completely unparseable strings where floats are expected), the script must **exit with code 1** and not write the output file.
   - **Accept:** If the CSV is successfully sanitized and contains no malicious extremes, save the sanitized data to the specified `--output` path and **exit with code 0**.

Note: You can install any standard Python data science or OCR packages (like `pandas`, `pytesseract`, `Pillow`) you need. The output CSV should maintain the original headers (`Alpha`, `Beta`, `Gamma`).