You are acting as a localization engineer. We have a batch of translation files from our vendors in `/home/user/inputs/`. The previous pipeline script used to silently drop rows containing embedded newlines, which corrupted our cost estimations.

We need you to build a reliable data processing pipeline that correctly parses these CSV files, filters out invalid translations based on mathematical constraints, and calculates the total cost per locale. 

Here are the requirements:
1. Parse all CSV files in the `/home/user/inputs/` directory. The CSVs have the following columns: `id,locale,source_text,target_text,rate_per_char`.
2. Ensure rows with quoted embedded newlines in `source_text` or `target_text` are processed correctly and NOT dropped.
3. Validate and filter the data. A row is considered **INVALID** and must be dropped if:
   - `source_text` is empty (length 0).
   - `target_text` is empty (length 0).
   - The ratio of the target length to the source length ($R = \frac{\text{length of target\_text}}{\text{length of source\_text}}$) falls outside the inclusive range `[0.2, 5.0]`.
4. For all **VALID** rows, calculate the cost: `cost = length(target_text) * rate_per_char`.
5. Aggregate the total cost for each `locale` across all input files.
6. Write the aggregated results to `/home/user/locale_costs.json` as a JSON dictionary mapping the locale string to the total cost (rounded to exactly 2 decimal places). Example: `{"es": 15.42, "fr": 12.00}`
7. Write the `id` of every **INVALID** row to a log file at `/home/user/dropped_ids.log`. The file should contain one ID per line, sorted in ascending numerical order.

Ensure your script handles streaming efficiently and deals with the CSVs properly. You can use Python, bash, or any standard Linux utilities available.