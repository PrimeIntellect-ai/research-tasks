You are an AI assistant helping a data researcher organize and analyze a large collection of dataset metadata files. The researcher wants to build a lightweight, trackable pipeline to validate these datasets, find similarities between them to power a recommendation system, and track each execution of this pipeline.

Your objective is to write a Bash script `/home/user/run_pipeline.sh` that performs the following tasks:

**1. Experiment Tracking Setup**
The script must accept exactly one argument: a "run name" (e.g., `run_alpha`).
It should create a directory for this run at `/home/user/runs/<run_name>/`. All output files for this execution must be saved inside this directory.

**2. Data Schema Enforcement**
The researcher's metadata files are located in `/home/user/datasets/` as `.json` files.
Your script must validate each JSON file against the following schema requirements:
- Must contain an `id` field (string).
- Must contain a `name` field (string).
- Must contain a `tags` field, which must be an array of strings containing at least one element.

Files that fail this validation should have their filenames (just the basename, e.g., `data4.json`) logged to `/home/user/runs/<run_name>/invalid.log`, one per line, sorted alphabetically. 

**3. Similarity Search and Recommendation**
For the valid datasets, you need to compute the Jaccard similarity coefficient between all pairs of datasets based on their `tags`. 
The Jaccard similarity is defined as the size of the intersection of the tags divided by the size of the union of the tags.

For each valid dataset, find the *single most similar* other valid dataset (highest Jaccard score). If there is a tie, pick the dataset whose `id` comes first alphabetically. 
Output these recommendations to `/home/user/runs/<run_name>/recommendations.tsv`.
The format of this file must be exactly three columns separated by tabs:
`<dataset_id> \t <recommended_dataset_id> \t <similarity_score>`
The similarity score must be formatted to exactly two decimal places (e.g., `0.50`, `0.33`).
Sort the lines in the TSV alphabetically by the `<dataset_id>`.

**4. Metrics Logging**
Finally, create a file `/home/user/runs/<run_name>/metrics.txt` containing exactly three lines:
```
Total: <total_number_of_json_files>
Valid: <number_of_valid_files>
Invalid: <number_of_invalid_files>
```

**Constraints & Notes:**
- You must write the main logic in Bash (`/home/user/run_pipeline.sh`), though you may use standard command-line tools (like `jq`, `awk`, `sed`) or inline Python/Ruby if needed to compute the combinations and Jaccard similarities.
- Make sure your bash script is executable.
- Run your script once with the argument `test_run` so the outputs are generated in `/home/user/runs/test_run/` for verification.