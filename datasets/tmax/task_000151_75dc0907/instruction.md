You are a data analyst tasked with building an automated data processing pipeline. You need to process a CSV file containing user location data, validate it, anonymize it, compute a metric, and schedule this task. 

Write a Go program located at `/home/user/process.go` that does the following:
1. Reads `/home/user/raw_data.csv` which has the header: `id,email,latitude,longitude`.
2. **Validates** the data: Drops any rows where latitude or longitude are missing, not valid numbers, or out of valid bounds (-90 to 90 for latitude, -180 to 180 for longitude).
3. **Anonymizes** the email address by replacing everything before the `@` symbol with `***` (e.g., `user.name@example.com` becomes `***@example.com`).
4. **Computes** the Manhattan distance from the coordinates (0.0, 0.0) for each valid row. The formula is `abs(latitude) + abs(longitude)`.
5. **Sorts** the valid records by the computed distance in ascending order. If distances are equal, sort by `id` ascending.
6. Writes the results to `/home/user/processed_data.csv` with the header: `id,masked_email,distance`. Format the distance to 2 decimal places.

After writing and testing your Go program, schedule it to run automatically. Create a bash script at `/home/user/setup_cron.sh` that, when executed, installs a cron job for the current user to run `cd /home/user && go run /home/user/process.go` every day at exactly 02:00 AM. 

Execute your Go program once to generate the output file, and run your `setup_cron.sh` script so the cron job is installed.