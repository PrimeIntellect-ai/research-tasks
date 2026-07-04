You are acting as a data engineer for a tech company. We have a batch of customer feedback data that needs to be parsed, transformed, and sampled for manual review. You need to write a C++17 program to handle this ETL pipeline.

Here are the details of the task:

1. **Input Data**: 
There is an input CSV file at `/home/user/input/feedback.csv` containing raw customer logs in a "wide" and unstructured format. 
The columns are: `UserID,Region,LogText`
The `LogText` column contains multiple daily entries separated by a pipe `|`. Each daily entry follows this pattern:
`Day: [ProductID] sentiment - ErrorCode`
For example: `Mon: [AppX] positive - none | Tue: [AppY] negative - E404`

2. **C++ Program Requirements**:
Write a C++ program at `/home/user/process.cpp` and compile it to `/home/user/process`. The program must perform the following:

**A. Structured Information Extraction & Wide-Long Reshaping:**
Parse the `LogText` for each row using standard C++ regex. Extract the `Day`, `ProductID`, `Sentiment`, and `ErrorCode`.
Reshape the data from the wide/nested format into a "long" format CSV where each daily entry is its own row.
The output columns should be exactly: `UserID,Region,Day,ProductID,Sentiment,ErrorCode`
Ignore any daily entries that do not perfectly match the extraction pattern. Save this full long-format dataset to `/home/user/output/long_format.csv`.

**B. Data Sampling and Stratification:**
From the long format data, create a stratified sample for our QA team. 
- Group the data by `Region` and `Sentiment` (this is your stratum).
- For each stratum, sort the available records first by `UserID` (ascending, lexicographical), and then by `Day` (ascending, lexicographical).
- Select exactly the first 2 records from each stratum. If a stratum has fewer than 2 records, take all of them.
Save this sample to `/home/user/output/sample.csv` with the same columns as the long format.

**C. Pipeline Logging:**
The program must append logs to `/home/user/pipeline.log`. Write exactly the following lines (replace bracketed values with actual integers):
`[INFO] Processed <N> input rows.` (Number of rows in feedback.csv, excluding header)
`[INFO] Generated <M> long records.` (Total valid daily entries extracted)
`[INFO] Stratified sample size: <K>.` (Total rows in sample.csv, excluding header)

Please write the code, compile it, and run it. Do not use any external C++ libraries (like Boost) — only standard C++17 library headers are permitted. Ensure the output directory exists before writing to it.