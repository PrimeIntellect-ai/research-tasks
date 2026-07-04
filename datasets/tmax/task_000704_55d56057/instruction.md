You are an AI assistant helping a data researcher clean and analyze a corrupted dataset. 

A data processing pipeline recently failed, silently injecting `NaN` values into our integer columns and creating extreme outliers. We need you to build a Bash-based pipeline to fix this, analyze the data statistically, and retrieve specific records based on text similarity.

You have been given a dataset at `/home/user/dataset.csv` with the following columns:
`record_id,measurement,notes`

Please write a Bash script named `/home/user/run_analysis.sh` that performs the following steps (you may use inline Python within your Bash script to help with the heavy lifting, but the pipeline must be executable via this single Bash script):

1. **Missing Value & Outlier Handling:**
   Read `/home/user/dataset.csv`. Filter out any rows where `measurement` is missing (`NaN`, empty, or null) AND any rows where `measurement` is an outlier (defined as `measurement > 100.0` or `measurement < 0.0`). 
   Save the cleaned data to `/home/user/cleaned_dataset.csv` (keep the header).

2. **Confidence Intervals:**
   Calculate the 95% Confidence Interval for the mean of the cleaned `measurement` column. Assume a normal distribution (you can use `scipy.stats` or standard math). 
   Save the output strictly as `lower_bound,upper_bound` (rounded to 2 decimal places) in `/home/user/ci.txt`.

3. **Embedding Computation & Retrieval:**
   Using the `notes` column of the *cleaned* dataset, compute TF-IDF vectors (which serve as sparse embeddings) for each row's notes. Compute the cosine similarity between these notes and the query string: `"stable baseline reading"`. 
   Find the `record_id` of the row with the highest cosine similarity to the query. 
   Save this single `record_id` (as an integer) to `/home/user/retrieved_id.txt`.

Make sure your script `/home/user/run_analysis.sh` is executable (`chmod +x`) and runs without user intervention. Run your script to generate the required output files.