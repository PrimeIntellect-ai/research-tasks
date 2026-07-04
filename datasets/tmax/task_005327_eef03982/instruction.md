You are an integration developer testing a new telemetry API. We have captured a large JSON response payload from the staging environment and saved it at `/home/user/api_response.json`. The file contains a single JSON array of objects.

Your task is to:
1. Write a script in the programming language of your choice that reads `/home/user/api_response.json`.
2. Parse the structured data and filter for objects where the `"status"` key is exactly `"SUCCESS"`.
3. Implement a numerical calculation to find the **population variance** of the `"value"` field for only those successful records.
4. Output the resulting population variance, rounded to exactly 4 decimal places (e.g., `123.4567`), and save it to `/home/user/variance_result.txt`.
5. We need to ensure your script is somewhat efficient. Profile the memory usage of your script execution by running it under `/usr/bin/time -v`. Redirect the profiling output (which is written to stderr by `time`) to `/home/user/memory_profile.txt`.

Example expected state:
- `/home/user/variance_result.txt` containing only the variance number.
- `/home/user/memory_profile.txt` containing the output of `/usr/bin/time -v` including the `Maximum resident set size`.