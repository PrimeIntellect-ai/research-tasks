You are acting as a data scientist cleaning a set of mathematical measurements and product metadata. You have received two datasets from international teams, located at `/home/user/measurements.csv` and `/home/user/metadata.csv`. 

Your task is to write a C++ program that performs an ETL process to join, validate, and clean these datasets.

**Dataset 1: /home/user/measurements.csv**
Format: `id,length,width,height,stated_volume`
All values (except id) are floating-point numbers.

**Dataset 2: /home/user/metadata.csv**
Format: `id,name,price_string`
* `name` contains UTF-8 encoded text (including Japanese, Arabic, and French characters).
* `price_string` contains a Unicode currency symbol followed immediately by a floating-point number (e.g., "€45.50", "¥1500.00", "£20.75"). 

**Requirements for your C++ program:**
1. **Join:** Merge the two datasets on the `id` field.
2. **Constraint-based Validation (Math):** For each joined record, calculate the actual volume (`length * width * height`). A record is considered *valid* only if the absolute difference between the calculated volume and the `stated_volume` is less than or equal to 3.0% of the calculated volume. Drop any records that fail this constraint.
3. **Unicode Processing:** For the valid records, parse the `price_string`. You must strip the leading Unicode currency symbol (which may be multiple bytes in UTF-8, specifically '€', '¥', or '£') and extract the numeric value as a float.
4. **Output:** Write the cleaned, valid records to `/home/user/cleaned_products.jsonl` (JSON Lines format), ordered by `id` ascending.

**Output Format:**
Each line in `/home/user/cleaned_products.jsonl` must be a valid JSON object matching exactly this structure:
`{"id": "A1", "name": "Café", "calculated_volume": 120.50, "numeric_price": 45.50}`

Note: `calculated_volume` and `numeric_price` should be formatted to exactly 2 decimal places in the JSON output.

Write your C++ code to `/home/user/etl.cpp`, compile it (using `g++ -std=c++17 -o etl etl.cpp`), and execute it to generate the final JSONL file.