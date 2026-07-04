A background service running on this system, `run_sensor.sh`, has a known bug: it creates a SQLite database for temporary sensor data, opens it, and immediately unlinks (deletes) the file from the filesystem. Because the file descriptor is kept open, it causes a hidden storage leak.

Your task is to investigate and recover the lost data.

1. Locate the running `run_sensor.sh` process and identify the file descriptor for the deleted SQLite database.
2. Recover the database file and save it to `/home/user/recovered.db`.
3. The recovered database contains a single table named `measurements` with a column `value` (which contains floating-point numbers). 
4. Because of floating-point precision errors during the daemon's calculations, some values have drift (e.g., `0.30000000000000004`). Sum all the numbers in the `value` column, fix the floating-point precision issue by rounding the final sum to exactly 2 decimal places, and save this final formatted sum to `/home/user/result.txt`.

Ensure `/home/user/result.txt` contains only the final rounded sum (e.g., `12.34`). Do not kill the running service.