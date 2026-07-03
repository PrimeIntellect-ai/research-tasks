You are tasked with organizing a legacy Python project, managing its dependencies, performing a database schema migration based on semantic versioning, and writing a mock-based test suite.

The legacy files are currently located in `/home/user/project_legacy`. You need to structure them into a new directory `/home/user/app` and complete the following steps:

1. **Dependency Management**:
   Create a Python virtual environment at `/home/user/venv`.
   Activate it and install `pytest` and `packaging`.
   Create a `/home/user/app/requirements.txt` file listing these two dependencies.

2. **Project Organization**:
   Create the directories `/home/user/app/src` and `/home/user/app/tests`.
   Move `/home/user/project_legacy/data_reader.py` to `/home/user/app/src/data_reader.py`.
   Copy `/home/user/project_legacy/db.sqlite3` to `/home/user/app/db.sqlite3`.

3. **Schema Migration & Version Comparison**:
   Write a Python script `/home/user/app/src/migrate.py`. This script must:
   - Import `data_reader` from the same directory and call `data_reader.get_latest_data()`.
   - Connect to the SQLite database at `/home/user/app/db.sqlite3`.
   - The database contains a `users` table with columns `id`, `name`, and `app_version` (text).
   - Use the `packaging.version.parse` function to parse the `app_version` of each user.
   - Delete all users whose `app_version` is strictly less than `2.1.0`.
   - Create a new table `schema_info` (if it doesn't exist) with a single integer column `version`.
   - Insert a row into `schema_info` with the value `2`.
   - Commit the changes and close the connection.

4. **Test Fixture and Mock Setup**:
   Write a test file `/home/user/app/tests/test_migrate.py`.
   - Use `pytest` and `unittest.mock`.
   - Write a test `test_migration_process` that imports and runs your migration script.
   - You must patch `data_reader.get_latest_data` during the test so it returns `{"status": "mocked"}` instead of its actual behavior.
   - Assert that the mock was called exactly once.
   - Note: You may want to configure your Python path or run tests so `src` is accessible.

5. **Execution**:
   - Run your tests to ensure they pass.
   - Run the migration script `/home/user/app/src/migrate.py` against the database `/home/user/app/db.sqlite3`.
   - Output the count of the remaining users in the `users` table to a file named `/home/user/report.txt`. The file should contain only the integer count.

Ensure all file paths and names match exactly.