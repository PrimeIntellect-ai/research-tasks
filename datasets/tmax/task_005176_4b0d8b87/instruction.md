You are tasked with fixing a broken data ingestion pipeline for our analytics platform. The pipeline receives daily CSV files, but recently, malformed and anomalous data (outliers, missing values, and data leakage) has been slipping through, crashing our storage workers.

Your objective is to create a pre-filter script and integrate it into our multi-service ingestion architecture. 

System Architecture:
- We have a multi-service setup located in `/home/user/app/`.
- Services include a Redis instance (port 6379), a Flask API (port 8080) that receives uploaded CSVs, and a Storage Worker that consumes from Redis.
- The startup script is `/home/user/app/start_services.sh`.

Task Requirements:
1. **Create a Filter Script**: Write a Bash script at `/home/user/filter.sh` that takes a single argument (the path to a CSV file). The script must evaluate the CSV and exit with `0` if the file is completely valid ("clean"), and exit with `1` if the file is invalid ("evil").
   
   A CSV is considered "clean" ONLY if all the following conditions are met for every row (excluding the header):
   - The header is exactly: `id,feature_A,feature_B,target`
   - `id` is an integer.
   - `feature_A` and `feature_B` are valid floating-point numbers or integers. There must be no missing values in these columns.
   - `feature_A` must be within the range [-1000, 1000] (inclusive). Any value outside this range is a severe outlier.
   - `target` must be either `0` or `1`. It cannot be missing.

2. **Configure the API**: The Flask API reads its configuration from `/home/user/app/config.ini`. Update this file to set the `PRE_FILTER_CMD` variable to the absolute path of your script (`/home/user/filter.sh`).

3. **Start the Services**: Run `/home/user/app/start_services.sh` to bring up Redis, the API, and the Storage Worker. Ensure they are running and correctly using your filter.

4. **Validation**: We have provided two corpora of CSV files to test your script:
   - `/home/user/corpora/clean/` contains valid CSVs.
   - `/home/user/corpora/evil/` contains invalid CSVs with anomalies, missing values, or outliers.
   Your `/home/user/filter.sh` must correctly identify 100% of the clean files (exit 0) and reject 100% of the evil files (exit 1).

Ensure your script is executable (`chmod +x /home/user/filter.sh`). You can test your script against the corpora before integrating it into the pipeline.