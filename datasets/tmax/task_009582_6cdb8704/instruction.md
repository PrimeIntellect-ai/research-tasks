You are an automation specialist managing a customer feedback ingestion pipeline. Recently, the data team noticed that feedback files containing multiline text (e.g., CSV records with embedded newlines in the feedback column) are silently dropping rows or breaking downstream processors that naively read files line-by-line.

Your task is to create a robust data processing pipeline script that correctly handles mixed-format files (CSV and JSON) and aggregates the data. You can write your solution in Python, Node.js, or a combination of Bash and a scripting language.

**Source Data:**
You have a directory `/home/user/data/feedback/` containing incoming feedback files in both `.csv` and `.json` formats. 
- CSV files have the header: `id,product_category,rating,feedback_text`
- JSON files contain an array of objects with the exact same keys.
- Some CSV files contain embedded newlines inside the `feedback_text` fields (which are properly wrapped in double quotes). 

**Requirements:**
1. Create a script that reads all `.csv` and `.json` files in `/home/user/data/feedback/`.
2. **Handle embedded newlines:** Ensure that CSV records with multiline `feedback_text` are parsed as single valid records, not split or dropped.
3. **Aggregation:** Calculate the average `rating` for each `product_category` across all files. Round the average to exactly 2 decimal places.
4. **Summary Output:** Write the aggregated averages to `/home/user/output/summary.json` as a single JSON object mapping categories to their average rating (e.g., `{"electronics": 4.5, "home": 3.67}`).
5. **Pipeline Logging:** Create a log file at `/home/user/output/pipeline.log`. For every file successfully processed, append a line with the exact format:
   `[INFO] Processed <filename>: <N> records`
   (where `<filename>` is just the basename of the file, e.g., `batch1.csv`, and `<N>` is the number of valid records parsed from that file). Sort the log entries alphabetically by filename.

Make sure your script creates the `/home/user/output/` directory if it does not exist, and then execute your script to generate the final artifacts.