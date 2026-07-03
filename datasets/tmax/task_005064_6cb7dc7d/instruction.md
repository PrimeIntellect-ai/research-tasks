You are a data analyst debugging a legacy pipeline. We have a set of obfuscated CSV files in `/home/user/data/`: `T1.csv`, `T2.csv`, and `T3.csv`. 

There is a legacy compiled executable located at `/app/legacy_calc` which processes these files and outputs a summary report. However, the legacy binary contains a severe bug: due to an implicit cross join in its internal logic, it massively inflates the calculated totals for certain records. 

Your goals are to:
1. Reverse engineer the data model and relationships between `T1.csv`, `T2.csv`, and `T3.csv`.
2. Understand what calculation the legacy binary is *trying* to perform (it attempts to group by a primary entity and sum a converted value).
3. Identify the cross-join bug that inflates the results.
4. Write a Python script `/home/user/generate_report.py` that correctly maps the relationships, avoids the cross join, and calculates the true totals.
5. Run your script to produce `/home/user/correct_totals.csv`. 

The output file `/home/user/correct_totals.csv` must contain a header with exactly two columns: `entity_id` and `total_value`. The values should be rounded to 2 decimal places.

An automated grader will evaluate your `/home/user/correct_totals.csv` against the ground-truth values using Mean Absolute Error (MAE). You must achieve an MAE of less than 0.01 to pass.