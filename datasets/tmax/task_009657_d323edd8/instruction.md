You are a data analyst tasked with processing an international customer feedback dataset. You must orchestrate a multi-stage pipeline using shell commands and write a custom C program to handle text anonymization, Unicode text processing, and windowed aggregation.

The raw dataset is located at `/home/user/raw_data.csv`. It has the following columns (with a header row):
`Timestamp,CustomerName,FeedbackText,PurchaseAmount`

Your task:
1. **Pipeline Logging:** Create a shell script `/home/user/pipeline.sh` that echoes "Started", "Sorted", "Processed", and "Done" to `/home/user/pipeline.log` at the appropriate stages of your pipeline.
2. **Sorting:** Sort the raw CSV by the `Timestamp` column (column 1) in ascending numeric order, preserving or removing the header as needed for your C program, but ensuring the data rows are sorted by time.
3. **C Program Processing:** Write a C program at `/home/user/process.c` that reads the time-sorted data and performs the following:
   - **Data Masking (Anonymization):** Transform the `CustomerName`. Keep the first and last ASCII characters, and replace everything in between with exactly three asterisks `***`. (e.g., `Alice` becomes `A***e`, `Bob` becomes `B***b`, `A` becomes `A***A`).
   - **Unicode Processing:** The `FeedbackText` contains UTF-8 characters (including emojis and non-Latin scripts). Count the exact number of Unicode code points in the `FeedbackText`.
   - **Rolling Aggregation:** Calculate a 3-row moving average for the `PurchaseAmount`. For the first row, it's just the first amount. For the second row, it's the average of the first two. For the third row and beyond, it's the average of the current and previous two rows.
4. **Output:** Your C program should write to `/home/user/output.csv` with the following format (no header row):
   `MaskedName,CodePointCount,RollingAverage`
   *Note: Format the RollingAverage to exactly 2 decimal places.*

Execute your pipeline script so that `/home/user/output.csv` and `/home/user/pipeline.log` are generated correctly.