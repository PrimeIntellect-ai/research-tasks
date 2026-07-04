You are tasked with building a core component of our ETL pipeline for digitizing legacy scientific records. 

We have a scanned document containing the exact business logic and schema transformations required for our raw sensor data. This document is located at `/app/schema_rules.png`. 

Your objective is to:
1. Set up an environment capable of extracting the text from this image (you may install tesseract-ocr, Pillow, pytesseract, etc.).
2. Extract the data cleaning rules from the image.
3. Write a Python script at `/home/user/cleaner.py` that acts as our row-level data transformer.

The script `/home/user/cleaner.py` must accept a single command-line argument representing a single raw comma-separated string (e.g., `"12,,A,2021-05-01"`) and print the transformed comma-separated string to standard output. 

The raw input string will always have exactly 4 fields corresponding to `ID,Temperature,Status,Date`. You must apply the rules exactly as written in the scanned image. Do not print any extraneous debugging information in your final script, only the final cleaned CSV string.