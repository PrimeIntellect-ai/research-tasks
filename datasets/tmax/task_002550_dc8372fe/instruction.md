You are an integration developer tasked with upgrading a legacy API authentication system. The old system stored API keys in plain text, and we need to migrate these to a secure, hashed format in a new SQLite database while providing integration tests for the new auth flow.

You must write two Python scripts to complete this task.

**Part 1: The Migration Script (`/home/user/migrate.py`)**
Write a Python script that performs the following schema migration and data transformation:
1. Reads a legacy JSON export of users and their plain-text API keys from `/home/user/legacy_keys.json`. The JSON is a list of objects, e.g., `[{"user_id": 1, "legacy_key": "raw_string"}]`.
2. Reads an HMAC secret key from `/home/user/hmac_secret.txt`.
3. Creates a new SQLite database at `/home/user/api_db.sqlite` with a table named `api_credentials`.
   The table schema must be:
   - `user_id` (INTEGER PRIMARY KEY)
   - `hmac_hash` (TEXT)
   - `migrated_at` (TEXT) - Hardcode this to the string `'2024-01-01T00:00:00Z'` for all rows.
4. For each entry in the JSON, compute the HMAC-SHA256 hash of the `legacy_key` using the secret from `hmac_secret.txt`. The resulting hash should be a lowercase hex string.
5. Insert the `user_id`, `hmac_hash`, and `migrated_at` values into the `api_credentials` table.

**Part 2: The Integration Test (`/home/user/test_api_auth.py`)**
Write a Python `unittest` test file that verifies the new database works correctly for API authentication.
The test script should:
1. Connect to `/home/user/api_db.sqlite`.
2. Include at least one test method that dynamically computes the HMAC-SHA256 hash of the string `"alpha123"` using the secret from `/home/user/hmac_secret.txt`.
3. Query the `api_credentials` table for `user_id = 1` and assert that the queried `hmac_hash` exactly matches the dynamically computed hash.
4. Include an `if __name__ == '__main__': unittest.main()` block so the tests can be executed directly.

Execute `/home/user/migrate.py` to generate the database, and then run `/home/user/test_api_auth.py` to ensure your test passes. Leave all created files in `/home/user/`.