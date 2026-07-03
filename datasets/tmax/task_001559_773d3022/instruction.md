You are an Operations Engineer triaging an incident. A backend Python service recently crashed. A partial memory dump was taken during the crash, and we have a copy of the local SQLite database the service was querying. 

Your task is to identify the root cause from the memory dump, locate the problematic record in the database, write a regression test to prevent future occurrences, and patch the application logic.

Here are the details and your objectives:

1. **Memory Dump Analysis**:
   - The memory dump is located at `/home/user/memory.dump`.
   - The crash logger writes the ID of the user being processed just before crashing in the format `FATAL_USER_ID=<ID>`.
   - Extract this user ID from the binary memory dump.

2. **Query Debugging**:
   - The service uses an SQLite database located at `/home/user/users.db`.
   - The database has a table named `users` with columns: `id` (INTEGER), `username` (TEXT), and `metadata` (TEXT - JSON format).
   - Query the database to retrieve the `metadata` JSON string for the user ID you extracted from the memory dump.
   - Analyze the JSON string. You will notice a logical anomaly in the data (e.g., an invalid value for a specific field that caused the business logic to crash).

3. **Patching Application Logic**:
   - The validation logic is located in `/home/user/app.py`.
   - It contains a function `validate_user_data(metadata_str: str) -> bool`.
   - Currently, this function has a flaw and allows the anomalous data to pass (returning `True`).
   - Modify `validate_user_data` in `/home/user/app.py` so that it parses the JSON and raises a `ValueError("Invalid data")` if the anomaly you found is present (specifically, if the `"points"` field is less than 0). Otherwise, it should return `True`.

4. **Regression Test Construction**:
   - Create a Python test file at `/home/user/test_regression.py`.
   - Use the standard `unittest` framework.
   - Import `validate_user_data` from `app`.
   - Write a test class `TestUserValidation` with a test method `test_negative_points_raises_error`.
   - The test must assert that calling `validate_user_data` with the exact metadata string you retrieved from the database raises a `ValueError`.
   - Run your test suite and save the output to `/home/user/test_result.log` using the following command: `python3 -m unittest /home/user/test_regression.py > /home/user/test_result.log 2>&1`

Ensure all requested files are in place and correctly implemented.