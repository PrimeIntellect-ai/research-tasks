You are a data engineer tasked with building a small mathematical ETL pipeline. You need to process a set of messy mathematical expressions, evaluate them, join them with metadata, and generate a final localized report using a specific template.

You have two input datasets:
1. `/home/user/raw_expressions.csv`: A CSV file with headers `id,expression`. The expressions are poorly formatted strings containing two numbers and a word-based operator.
2. `/home/user/metadata.json`: A JSON file containing an array of objects with `id`, `category`, and `author`.

Your pipeline must perform the following steps:
1. **Tokenization and Normalization:** 
   Parse the `expression` field. Convert the word-based operators to standard mathematical symbols:
   - `x` becomes `*`
   - `div` becomes `/`
   - `plus` becomes `+`
   - `minus` becomes `-`
   Format the normalized expression so there is exactly one space before and after the operator (e.g., "  15   x 3 " becomes "15 * 3").
   Evaluate the mathematical result of the normalized expression. (All divisions will be clean integer divisions).

2. **Joins:** 
   Merge the evaluated expression data with the metadata from the JSON file using the `id` field.

3. **Stratification / Filtering:** 
   Group the joined data by `category`. For each category, select exactly the top 2 records with the **highest evaluated result**. If there is a tie, pick the one with the higher `id`.

4. **Template-based Generation:** 
   For each selected record, generate a text string using the exact following template:
   `Category {category} - Author {author} created expression {normalized_expr} which evaluates to {result}.`

Write the final generated strings to a file named `/home/user/report.txt`. 
The lines in `/home/user/report.txt` must be sorted alphabetically by `category` (A-Z). If records have the same category, sort them by the evaluated `result` in descending order (highest first).

You may use any programming language available in the standard Linux environment (Python, bash, etc.) to accomplish this.