You are a data engineer tasked with building an ETL pipeline to analyze software package vulnerabilities. You have been provided with three CSV files in `/home/user/data/`:

1. `/home/user/data/packages.csv` 
   Columns: `pkg_id`, `pkg_name`
2. `/home/user/data/dependencies.csv`
   Columns: `pkg_id`, `depends_on_pkg_id`
   (This means `pkg_id` requires `depends_on_pkg_id` to run)
3. `/home/user/data/vulnerabilities.csv`
   Columns: `pkg_id`, `vulnerability_score`

Your objective is to calculate the "Total Risk Score" for every package. The Total Risk Score of a package is defined as its own `vulnerability_score` PLUS the sum of the `vulnerability_score`s of ALL its transitive dependencies (direct and indirect). 

Important constraints:
- If a package depends on the same transitive dependency through multiple paths, that dependency's score should only be counted ONCE for the root package.
- If a package has no vulnerabilities listed, its base score is 0.
- You must write a Python script at `/home/user/etl_pipeline.py` that performs this calculation. You can use any standard library modules or install external libraries like `pandas`, `networkx`, or use `sqlite3` to perform recursive CTEs.
- The pipeline should output the final aggregated results to `/home/user/package_risk.json`.

The output file `/home/user/package_risk.json` must strictly be a JSON array of objects, with each object having exactly two keys:
- `"pkg_name"`: The name of the package (string)
- `"total_risk"`: The aggregated total risk score (integer)

The JSON array must be sorted by `total_risk` in descending order. If there is a tie in `total_risk`, sort by `pkg_name` in ascending alphabetical order.

Please set up your environment, write the script, run it, and ensure the output JSON is correctly formatted.