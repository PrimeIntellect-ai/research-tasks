You are an ETL data engineer. We have a pipeline that processes historical weather data from multiple sources.

We have two input data sources:
1. `/app/weather_wide.csv`: A CSV file containing weather data in wide format. Columns are `Date`, and several columns like `Temp_London`, `Temp_Moscow`, `Temp_Tokyo`. The data has missing dates and missing temperature values.
2. `/app/historical_weather.png`: An image of a scanned historical record. It contains a table with columns `Date`, `City`, and `Temperature`. The city names in the image are in their native scripts (e.g., Russian, Japanese, German) and may contain OCR artifacts.

Your tasks:
1. Run OCR (e.g., using `tesseract`) on `/app/historical_weather.png` to extract the records.
2. Process the extracted text. The dates are in `YYYY-MM-DD` format. Temperatures are floats. 
3. Match the extracted city names to our standard English names (`London`, `Moscow`, `Tokyo`) by comparing them against the known aliases provided in `/app/aliases.json`. Use a string similarity metric (like Levenshtein distance) to handle OCR typos and unicode variations. Match each extracted city to the standard name whose alias has the smallest distance.
4. Reshape `/app/weather_wide.csv` from wide to long format (columns: `Date`, `City`, `Temperature`). The `City` should be just the city name (e.g., `London`).
5. Combine the data from the CSV and the OCR-extracted data into a single DataFrame. If there are duplicates for a `Date` and `City`, average the temperatures.
6. Set the DataFrame index to a `DatetimeIndex` and group by `City`.
7. For each city, resample the time series to a daily frequency (`D`) from `2023-01-01` to `2023-01-10`.
8. Fill any missing `Temperature` values using linear interpolation.
9. Save the final cleaned, long-format, daily-resampled data to `/app/clean_weather.parquet` with columns `Date` (datetime), `City` (string), and `Temperature` (float). 

Ensure the parquet file is sorted by `Date` and `City`.

Your output will be evaluated by computing the Mean Squared Error (MSE) of your interpolated temperatures against the hidden ground truth.