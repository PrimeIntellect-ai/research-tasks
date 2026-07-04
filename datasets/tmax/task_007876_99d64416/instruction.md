You are a data analyst working for a multinational retail company. You have been given a dataset of store locations with names in various languages. The data is messy, contains subtle duplicates due to Unicode encoding inconsistencies, and needs to be analyzed to find stores closest to a new distribution center.

Your task is to process this data using Python and standard Linux tools.

**Input Files:**
1. `/home/user/raw_stores.csv`: A CSV file containing the store data. Columns are `store_id`, `name_native`, `latitude`, and `longitude`.
2. `/home/user/config.json`: A JSON file containing the reference point of the distribution center (`ref_lat`, `ref_lon`).

**Processing Requirements:**

1. **Multi-language/Unicode Normalization:** 
   Read the `name_native` from the CSV. Normalize it using the NFKC Unicode normalization form, and convert it to lowercase.

2. **Hash-based Deduplication:**
   Some stores were recorded multiple times with slight GPS drift and different Unicode normalizations of the same characters (e.g., composed vs. decomposed 'é').
   A row is considered a duplicate if it yields the same MD5 hash for the following string combination:
   `<normalized_lowercase_name>|<lat_rounded>,<lon_rounded>`
   * `lat_rounded` and `lon_rounded` must be the latitude and longitude rounded to exactly 2 decimal places (e.g., `48.86`).
   * When encountering duplicates, keep only the **first** occurrence based on the order in the CSV file.

3. **Distance Computation:**
   For each deduplicated store, calculate the distance from the store's exact coordinates (unrounded) to the reference point specified in `/home/user/config.json`.
   * Use the **Haversine formula**.
   * Assume the Earth's radius is exactly `6371.0` km.

4. **Output Generation:**
   Write the processed data to `/home/user/closest_stores.json`.
   The output must be a JSON array of objects, sorted in **ascending order of distance**.
   Each object must follow this exact format:
   ```json
   {
     "store_id": "101",
     "name_normalized": "café de paris",
     "distance_km": 12.34
   }
   ```
   * `distance_km` must be rounded to exactly 2 decimal places.

Ensure the final JSON file is properly formatted and written to the exact path specified.