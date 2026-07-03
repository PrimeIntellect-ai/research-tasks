You are an automation specialist tasked with digitizing and cleaning historical sensor logs. 

We have a scanned image of a data table located at `/app/data_table.png`. The image contains a two-column table representing a time series: the first column is the time index (an integer `X` from 0 to 10) and the second column is the sensor reading (a float `Y`). Due to damage, several `Y` values in the image are completely obscured by smudges or read as invalid text.

Your objective is to extract the data, automatically detect and impute the missing values, and generate a standardized JSON report.

You must implement the core logic in a C program.

**Workflow Requirements:**
1. **OCR Extraction**: Use `tesseract` to extract the raw text from `/app/data_table.png`.
2. **Data Parsing (in C)**: Write a C program that reads the OCR output. You must use POSIX Regex (`regex.h`) in your C program to parse the text line-by-line and identify valid `X Y` pairs. Robustly ignore noise or headers.
3. **Interpolation & Imputation (in C)**: Your C program must detect missing `X` indices in the expected sequence from `0` to `10`. For any missing `Y` values, apply linear interpolation based on the nearest valid bounding `X` values.
4. **Template-Based Output (in C)**: Your C program must generate a JSON file using a template-based approach (e.g., formatting strings manually to match the exact schema). 

**Output Requirements:**
Save the final output to `/home/user/imputed_data.json`.
The format must strictly be a JSON array of objects:
```json
[
  {"time": 0, "value": 10.0},
  {"time": 1, "value": 12.0},
  ...
]
```
Ensure floating-point values are printed to one decimal place. 

An automated verification script will compute the Mean Squared Error (MSE) between your reconstructed `Y` values and the hidden ground truth values. Your output must be highly accurate to pass.