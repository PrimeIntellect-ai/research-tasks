I need your help organizing a massive, messy archive of historical sensor logs for my climate research. The dataset is located at `/app/sensor_logs.tar.gz`. 

The archive contains thousands of log files from different stations, but it's a mess:
1. **Mixed Encodings:** The logs were collected by different legacy systems. Some are in UTF-8, but many are in ISO-8859-1, Windows-1252, or MacRoman. You will need a reliable way to detect these. I've included the source code for the `chardet` package at `/app/chardet`, which I want you to use. However, I tried to install it earlier and it failed with a syntax error in its build configuration—you'll need to fix the package and install it in your environment.
2. **Corrupted Headers:** Randomly throughout the files, there are corrupted system diagnostic blocks. These blocks always start with the exact line `[DIAGNOSTIC_START]` and end with the exact line `[DIAGNOSTIC_END]`. You must strip out these lines and everything between them before parsing the data.
3. **Data Format:** Once cleaned and properly decoded to UTF-8, the files follow a strict line-by-line key-value format (e.g., `StationID: 402`, `Temperature: 22.4`, `Humidity: 55.1`). 

Your objective is to:
1. Fix and install the vendored `chardet` package.
2. Extract the archive.
3. Convert all files to UTF-8, stripping out the diagnostic blocks.
4. Parse the cleaned logs to calculate the mean `Temperature` and `Humidity` for each unique `StationID`.
5. Write the final aggregated results to `/home/user/station_averages.csv`.

The output file `/home/user/station_averages.csv` must contain exactly three columns with a header row: `StationID,AvgTemp,AvgHumid`. The station IDs should be sorted numerically. Round the averages to 4 decimal places.

I will evaluate your results by comparing your calculated averages against my verified ground-truth spreadsheet using a Mean Absolute Error (MAE) metric. You need an MAE of less than 0.05 to pass. Good luck!