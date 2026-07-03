You are an AI assistant acting as a data analyst. You have been given a messy data extract from an old internal database containing product reviews.

The file is located at `/home/user/raw_reviews.csv`.

Your objective is to build a data pipeline that processes this file, validates its contents, and computes aggregate statistics. You should write a Python script to perform this task. 

Here are the requirements:

1. **Character Encoding Handling:**
   The source system export is notoriously buggy and exports the file in a non-UTF-8 encoding (specifically UTF-16LE). Your process must correctly read this file and process the text as standard UTF-8.

2. **Validation Checkpoints (Quality Gates):**
   The CSV contains the following columns: `ID,Category,Rating,Date,Review`
   Many rows contain corrupted data. You must filter out any row that fails *any* of the following validation rules:
   * `ID`: Must be exactly 8 alphanumeric characters.
   * `Category`: Must not be empty.
   * `Rating`: Must be an integer exactly between 1 and 5 (inclusive). Reject any empty, non-integer, or out-of-bounds values.
   * `Date`: Must strictly follow the `YYYY-MM-DD` format.
   * `Review`: Must contain at least one non-whitespace character (cannot be empty or just spaces).

3. **Aggregation and Sorting:**
   For all *valid* rows, group the data by `Category`.
   Calculate the total number of valid reviews and the average rating for each category.
   
4. **Output Generation:**
   Write the aggregated results to a new CSV file at `/home/user/category_stats.csv`.
   * The file must use standard UTF-8 encoding.
   * The file must have the exact header: `Category,Valid_Review_Count,Average_Rating`
   * `Average_Rating` must be rounded to exactly 2 decimal places (e.g., 4.10, 3.85).
   * The rows must be sorted descending by `Valid_Review_Count`. If counts are tied, sort ascending alphabetically by `Category`.

Process the file and generate `/home/user/category_stats.csv` as specified.