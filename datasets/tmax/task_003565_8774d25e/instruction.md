You are a data analyst tasked with processing an irregular, wide-format CSV file containing server cluster logs. The file is located at `/home/user/data/raw_metrics.csv`.

Your task is to write a C++ program that reads this file, reshapes the data, extracts specific features from text fields, aggregates the results, and writes them to a new CSV file at `/home/user/data/summary.csv`.

Here are the details of the requirements:

1. **Input Format**: 
   The input CSV (`/home/user/data/raw_metrics.csv`) has a header and contains the following columns: `Date`, `EventDescription`, `NodeAlpha`, `NodeBeta`, `NodeGamma`.
   The `EventDescription` column contains text strings that start with an event code enclosed in square brackets, followed by a message (e.g., `"[E-404] Resource not found"`).
   The Node columns contain integer counts of how many times that event occurred on that specific node on that date.

2. **Data Processing Steps**:
   - **Wide-to-Long Reshaping**: Unpivot the node columns. Instead of one row with three node counts, you should conceptually reshape it into rows representing `Date`, `EventDescription`, `NodeName`, and `Count`.
   - **Feature Extraction**: Extract the event code from the `EventDescription` string. The event code is strictly the alphanumeric text inside the first pair of square brackets (e.g., extract `E-404` from `"[E-404] Resource not found"`).
   - **Aggregation**: Group the data by `NodeName` and the extracted `EventCode`. Calculate the sum of `Count` for each group.

3. **Output Format**:
   - Write the aggregated results to `/home/user/data/summary.csv`.
   - The output CSV must have exactly this header: `NodeName,EventCode,TotalCount`
   - Filter out any groups where the `TotalCount` is exactly 0.
   - Sort the output alphabetically by `NodeName` (ascending), and then alphabetically by `EventCode` (ascending).
   - Use standard comma separation. Do not quote the output fields unless strictly necessary.

4. **Implementation details**:
   - Create your C++ source file at `/home/user/process_logs.cpp`.
   - Compile it into an executable named `/home/user/process_logs`. You may use modern C++ (e.g., `-std=c++17`).
   - Run the executable to generate the `summary.csv` file.

Make sure the final output file exists and strictly adheres to the requested format and sorting order.