You are tasked with analyzing the configuration drift of a multi-language software system over time. 

A configuration manager has been taking periodic backups of configuration files. These backups often contain comments in multiple languages (including Unicode characters like Japanese and accented French) and have varying values.

The backup files are located in `/home/user/configs/`. Each file is named using the pattern `config_YYYYMMDD_HHMM.txt`.

Write a Python script at `/home/user/analyze_configs.py` and run it to perform the following pipeline:
1. **Extraction & Tokenization**: Read all `.txt` files in the directory (they are UTF-8 encoded). Tokenize the content to extract all contiguous alphabetical words. 
   * A "word" is defined strictly as a contiguous sequence of alphabetic characters (including Unicode letters). 
   * Digits, underscores, punctuation, and whitespaces must be completely excluded and act as delimiters. (Hint: in Python's `re` module, you can use `[^\W\d_]+`).
   * Convert all extracted tokens to lowercase.
2. **Time-Based Bucketing**: Aggregate all unique tokens present in all files for a given *day* (the `YYYYMMDD` part of the filename) into a single mathematical set per day.
3. **Mathematical Aggregation**: Calculate the Jaccard Similarity Index between consecutive days (sorted chronologically). The Jaccard Index of Day A and Day B is the size of the intersection of their token sets divided by the size of the union of their token sets.
4. **Output**: Save the results into a CSV file at `/home/user/drift_metrics.csv`.
   * The CSV must have exactly two columns: `Date` and `Jaccard_Index`.
   * The `Date` should be the *later* date of the consecutive pair being compared (e.g., if comparing 20231001 and 20231002, the row should be for 20231002).
   * The `Jaccard_Index` must be rounded to exactly 4 decimal places.
   * Include the header row: `Date,Jaccard_Index`.

Ensure you run your script so the final CSV is generated.