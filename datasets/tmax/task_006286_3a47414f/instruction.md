You are an automation specialist tasked with creating a robust data harmonization and validation workflow for a manufacturing company. The company receives IoT sensor data from two different factory units. Unfortunately, the data pipelines were built by different teams, resulting in different schemas and formats. 

Your objective is to write and execute a Python script that reads, reshapes, merges, validates, and cleans the datasets, producing a single, unified, and validated CSV file.

**Input Files (You must assume these exist when your script runs):**
1. **`/home/user/data/factory_wide.csv`**: Data from Factory 1 in wide format.
   - Columns: `timestamp`, `factory`, `temp`, `pressure`, `humidity`
2. **`/home/user/data/factory_long.csv`**: Data from Factory 2 in long format.
   - Columns: `time_log`, `fid`, `metric`, `val`
   - The `metric` column contains strings: `"temp"`, `"pressure"`, or `"humidity"`.
3. **`/home/user/data/rules.json`**: A JSON file containing valid ranges for each metric.

**Processing Requirements:**
1. **Reshape & Harmonize**: 
   - Convert `factory_long.csv` into a wide format so it matches the structure of Factory 1.
   - The unified schema must have exactly these columns (all lowercase): `timestamp`, `factory_id`, `temp`, `pressure`, `humidity`.
2. **Union**: Combine the harmonized Factory 1 and Factory 2 datasets into a single DataFrame.
3. **Data Completeness**: Drop any rows that are missing one or more sensor readings (i.e., if a timestamp has a `temp` and `pressure` but no `humidity`, drop the entire row).
4. **Constraint-based Validation**: Read `rules.json`. It contains `"min"` and `"max"` boundaries for each metric. Filter the unified dataset to strictly include ONLY rows where ALL three metrics fall *inclusively* within their specified valid ranges. If even one metric in a row is out of bounds, drop the entire row.
5. **Formatting & Output**: 
   - Sort the final dataset primarily by `timestamp` (ascending) and secondarily by `factory_id` (ascending).
   - Format all floating-point numbers to exactly 1 decimal place.
   - Save the result to **`/home/user/output/validated_sensors.csv`** without the index.

Ensure your script creates the output directory if it does not exist. Use the `pandas` library to accomplish this. You can run your script directly in the terminal to produce the final output file.