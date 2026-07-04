You are a data engineer tasked with building an automated ETL pipeline that performs basic similarity search and correlation analysis on user activity data, then archives the raw logs.

We have a raw dataset located at `/home/user/raw_data/user_features.csv`.

Create a single Bash orchestration script at `/home/user/pipeline.sh` that, when executed, performs the following tasks:
1. Ensures that required analytical Python packages (e.g., `pandas`, `scipy`) are installed.
2. Uses Python (invoked by your Bash script) to read `/home/user/raw_data/user_features.csv` and finds the top 3 users most similar to user `U001` based on the cosine similarity of their features `f1`, `f2`, and `f3`.
3. Writes the `user_id`s of these top 3 most similar users, one per line in descending order of similarity, to `/home/user/output/top_similar.txt` (excluding `U001` itself).
4. Calculates the Pearson correlation coefficient between the `f1` and `f2` features across all users in the dataset. Write this single numerical value (rounded to exactly 3 decimal places) to `/home/user/output/correlation.txt`.
5. Finally, archives the original raw data by compressing it into a tarball located at `/home/user/archive/data_archive.tar.gz`.

After writing `/home/user/pipeline.sh`, run it to process the data and generate the output files. Make sure the output directories exist.