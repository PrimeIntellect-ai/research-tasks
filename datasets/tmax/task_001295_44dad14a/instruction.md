As a localization engineer, you are tasked with updating and verifying a new batch of localized time-series data files before they are ingested into our analytics pipeline. Recently, malicious actors and broken translation tools have been injecting invalid mathematical placeholders and extreme outliers into our missing-data gaps.

We have received an image containing the exact, updated mathematical and structural rules for validating these files. The image is located at `/app/loc_rules.png`.

Your task:
1. Extract the text from `/app/loc_rules.png` (using `tesseract` or similar tools). This image outlines specific rules for gap-filling missing numeric data and explicitly lists thresholds and forbidden localization strings.
2. Write a C program at `/home/user/loc_check.c` that implements these rules. The program must:
   - Read a CSV file where each line is formatted as: `Timestamp,NumericValue,TranslationString`
   - Handle "MISSING" in the `NumericValue` column by mathematically interpolating it as described in the image rules.
   - Scan the `TranslationString` for any forbidden patterns.
   - Enforce the threshold rules on the interpolated numbers.
3. Compile your program to `/home/user/loc_check`. 
   - It must take exactly one argument: the path to the CSV file to inspect.
   - If the file is perfectly valid (clean), the program must exit with status code `0`.
   - If the file violates ANY of the mathematical thresholds or string rules (evil), the program must exit with status code `1`.

You have access to a large dataset of these files to test your logic if you wish to create your own samples, but the final evaluation will test your compiled `/home/user/loc_check` binary against a hidden adversarial corpus of "evil" and "clean" files to ensure your filter is perfect.