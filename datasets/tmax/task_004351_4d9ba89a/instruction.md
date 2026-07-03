You are acting as a data analyst and C developer. We are processing large batches of coordinate data from sensors. Some of the data points are erroneous and must be filtered out, and the sensitive sensor IDs must be anonymized before downstream parallel processing.

Your task is to write a C program that validates, filters, masks, and sorts this CSV data.

1.  **Determine the Validity Threshold:**
    There is an image file located at `/app/formula.png`. It contains a mathematical inequality determining whether a data point is "valid" based on its `val_A` and `val_B` values. Read or OCR this image to find the exact threshold.

2.  **Write the Filter Program:**
    Create a C program at `/home/user/filter.c` and compile it to `/home/user/filter`.
    The program must accept exactly two arguments: an input CSV file path and an output CSV file path.
    Usage: `/home/user/filter <input.csv> <output.csv>`

3.  **Data Processing Rules:**
    *   **Input format:** The input CSV will have the header `id,val_A,val_B,payload`. `val_A` and `val_B` are integers.
    *   **Filtering:** Only keep rows where `val_A` and `val_B` satisfy the mathematical inequality found in `/app/formula.png`. Reject all other rows.
    *   **Masking:** For the rows that pass the filter, replace the entire `id` field with the exact string `MASKED`.
    *   **Sorting:** Sort the surviving rows in ascending numerical order based on `val_A`. If there's a tie, preserve the original relative order (stable sort).
    *   **Output format:** The output must be a valid CSV including the header `id,val_A,val_B,payload`, followed by the filtered, masked, and sorted rows.

Ensure your C program is robust and can handle standard CSV formatting. We will test your compiled `/home/user/filter` binary against an extensive suite of valid and invalid datasets.