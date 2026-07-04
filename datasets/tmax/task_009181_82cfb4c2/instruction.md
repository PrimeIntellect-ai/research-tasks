You are a data scientist tasked with cleaning a messy log file from our laboratory's sensor network. 

The raw data is located at `/home/user/raw_sensors.log`. It contains unstructured text lines logged by different machines. Some lines contain valid sensor readings, while others are just system messages or corrupted logs.

You need to write a Python script (e.g., at `/home/user/cleaner.py`) to parse this file, extract the relevant data, normalize it, and produce a clean CSV alongside a pipeline processing log.

**Data Extraction Rules:**
A valid sensor reading line contains all of the following elements (though other text may surround them):
1. **Date**: Enclosed in square brackets. It will either be in `[YYYY/MM/DD]` or `[MM-DD-YYYY]` format.
2. **Unit Name**: A string matching the pattern `Unit-[A-Za-z]+` (e.g., Unit-Alpha).
3. **Temperature**: A number (integer or float) immediately followed by either `F` or `C` (e.g., `104F` or `40C`). It may be preceded by words like "Temp:" or "temp is".
4. **Pressure**: A number (integer or float) immediately followed by either `psi` or `kPa` (e.g., `14.5psi` or `100kPa`).

**Normalization Rules:**
1. Convert all dates to standard `YYYY-MM-DD` format.
2. Convert all Temperatures to Celsius (C). If the reading is in Fahrenheit (F), convert it using the formula: `C = (F - 32) * 5/9`. Round the final Celsius value to exactly 1 decimal place.
3. Convert all Pressures to Kilopascals (kPa). If the reading is in psi, convert it using the formula: `kPa = psi * 6.89476`. Round the final kPa value to exactly 1 decimal place.

**Outputs Required:**
1. **Clean Data**: Write the successfully parsed and normalized records to `/home/user/clean_data.csv`. 
   - The CSV must have the following header: `date,unit,temperature_c,pressure_kpa`
   - Order the rows in the exact order they appeared in the input file.
2. **Pipeline Log**: Write a JSON log file to `/home/user/pipeline.json` summarizing the pipeline's execution. It must contain exactly this structure:
   ```json
   {
       "total_lines_processed": <int>,
       "successful_parses": <int>,
       "failed_parses": <int>
   }
   ```
   A line is considered a "failed parse" if it does not contain all four required elements (Date, Unit Name, Temperature, Pressure) matching the rules above.

Please create the Python script, run it, and generate the required output files.