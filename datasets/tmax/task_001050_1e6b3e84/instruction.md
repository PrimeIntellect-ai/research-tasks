You are a data engineer responsible for building an ETL pipeline that extracts mathematical formulas from unstructured text, evaluates them, anonymizes sensitive user data, performs stratified filtering, and generates a formatted report.

Your input data is located at `/home/user/raw_data.csv`.
The CSV has the following columns: `id`, `email`, `category`, `notes`.

Please perform the following steps to process the data:

1. **Structured Information Extraction**: Parse the CSV. For each row, extract the mathematical expression hidden in the `notes` column. The expression always immediately follows the exact string `"Equation: "` and ends immediately before the next period `"."`.
2. **Mathematical Evaluation**: Evaluate the extracted mathematical expression using Python's default evaluation rules. Convert the result to a string using Python's `str()` function.
3. **Data Masking and Anonymization**: Anonymize the `email` field. Replace all characters in the username (the part before the `@`) with `***` EXCEPT for the very first character. For example, `john.doe@example.com` becomes `j***@example.com`.
4. **Data Sampling and Stratification**: Group the records by `category`. For each category, select exactly the top 2 records that have the highest evaluated mathematical results (treat the evaluated results as numbers for the comparison). If there is a tie in the evaluated results, prioritize the record with the lower `id`.
5. **Large-scale Sorting and Grouping**: Sort the final dataset so that categories are in alphabetical order. Within each category, sort the records by their evaluated result in descending order.
6. **Template-based Text Generation**: Generate a Markdown report at `/home/user/report.md` using the exact structure below. Output a header for each category, followed by a bulleted list of the selected records. Leave an empty line between different categories.

Format for `/home/user/report.md`:
```markdown
# Category {category}
* {masked_email} computed {result}
```

Example of desired output structure:
```markdown
# Category A
* a***@example.com computed 50
* b***@test.com computed 45.5

# Category B
* c***@domain.org computed 100
* d***@xyz.com computed 20
```

Write and execute the necessary scripts (e.g., Python, Bash) to process the data and generate the report. Ensure the final file is saved exactly at `/home/user/report.md`.