You are acting as a data science assistant for a researcher organizing a massive dataset of video frame analyses. You need to accomplish two interrelated tasks: extracting tabular data from a video file and building a robust schema validator to filter out corrupted or incorrectly formatted datasets submitted by external collaborators.

**Part 1: Video Data Extraction**
There is a video file located at `/app/experiment_record.mp4`. You must extract the first 10 frames (frame indices 0 through 9) from this video. 
For each frame, convert it to grayscale and calculate the average pixel intensity (as a float). 
Save the results in a CSV file at `/home/user/first_10_frames.csv`.
The CSV must have a header row and exactly these columns in order:
1. `frame_id` (integer)
2. `intensity` (float, rounded to 2 decimal places)
3. `event_flag` (boolean string: set this to exactly "False" for all 10 rows)

**Part 2: Schema Validator Script**
The researcher is receiving thousands of CSV files and needs to automatically discard those that do not match the exact data schema.
Create a Python script at `/home/user/validate_csv.py`.
The script should accept a single command-line argument: the path to a CSV file.
`python3 /home/user/validate_csv.py <path_to_csv>`

The script must exit with code `0` (success) if the CSV strictly adheres to the following rules, and exit with code `1` (failure) if it violates ANY of them:
- The CSV must contain exactly a header row and one or more data rows.
- The header must exactly match: `frame_id,intensity,event_flag`.
- `frame_id` must be parseable as an integer and must be >= 0.
- `intensity` must be parseable as a float and must be between 0.0 and 255.0 (inclusive).
- `event_flag` must be exactly the string "True" or "False" (case-sensitive).
- There must be no missing values, no empty rows, and no extra columns.

Please ensure the script relies only on standard Python libraries or `pandas`/`numpy` (which you may install if needed).