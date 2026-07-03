You are a data analyst working with an academic network dataset. You have been provided with a set of CSV files representing a knowledge graph of researchers, their publications, and institutions.

The files are located in `/home/user/data/`:
1. `researchers.csv`: `id`, `name`, `institution_id`, `interest`
2. `publications.csv`: `paper_id`, `title`, `year`
3. `authorships.csv`: `paper_id`, `researcher_id`
4. `institutions.csv`: `institution_id`, `name`, `country`

Your task is to write a Python script at `/home/user/analyze_graph.py` that processes these CSV files to identify cross-institutional collaborations based on specific criteria. 

The script must accept exactly two command-line arguments:
1. `interest` (string): A specific research interest to filter by.
2. `min_year` (integer): The minimum publication year (inclusive).

Usage example:
`python3 /home/user/analyze_graph.py "Machine Learning" 2018`

The script must find all pairs of researchers who:
1. Co-authored at least one paper published in or after `min_year`.
2. Belong to strictly different institutions (`institution_id` must differ).
3. At least one of the two researchers in the pair must have an `interest` exactly matching the `interest` argument.

Your script must execute a parameterized query (do not use string concatenation for the arguments to avoid injection risks, use proper parameter binding if using SQL). You may use standard libraries like `sqlite3`, or install and use `pandas` or `duckdb`.

The output must be saved to `/home/user/cross_institutional_collabs.csv` with exactly the following columns, including the header row:
`researcher_1,researcher_2,paper_title,inst_1,inst_2`

Rules for the output format:
- For each valid pair, `researcher_1` must be the name of the researcher that comes first alphabetically between the two, and `researcher_2` is the other.
- `inst_1` is the name of the institution for `researcher_1`.
- `inst_2` is the name of the institution for `researcher_2`.
- `paper_title` is the title of the co-authored paper.
- The results must be sorted alphabetically by `researcher_1`, then `researcher_2`, then `paper_title`.
- Ensure there are no duplicate rows in the final output.

Once your script is complete, test it by running:
`python3 /home/user/analyze_graph.py "Data Science" 2020`
This will generate the required output file `/home/user/cross_institutional_collabs.csv` for verification.