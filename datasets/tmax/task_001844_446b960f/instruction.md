We are building a new REST API backend for our web application in C++, but the current authentication prototype has a critical security vulnerability and is missing a schema update. 

Your task is to secure the endpoint logic and apply a database migration.

Here is the setup in `/home/user/auth_service`:
- `auth_api.cpp`: Contains a mock REST API handler that parses the username and password, then checks them against a SQLite database.
- `Makefile`: Builds the `auth_api` binary.
- `db.sqlite`: The local SQLite database containing a `users` table.
- `test_auth.sh`: An integration test script that tests the API with both valid credentials and a SQL injection payload.

Please perform the following steps:
1. **Schema Migration**: Update the `users` table in `/home/user/auth_service/db.sqlite` by adding a new column named `role` of type `TEXT` with a default value of `'user'`.
2. **Fix SQL Injection**: Open `/home/user/auth_service/auth_api.cpp`. The `authenticate_user` function currently builds a SQL query using string concatenation, making it vulnerable to SQL injection. Rewrite this function to use SQLite parameterized queries (`sqlite3_prepare_v2`, `sqlite3_bind_text`, `sqlite3_step`, etc.). The function should return `true` if the user exists and the password matches, and `false` otherwise.
3. **Build**: Run `make` in `/home/user/auth_service` to compile the updated binary.
4. **Integration Testing**: Run `/home/user/auth_service/test_auth.sh` and redirect its standard output to `/home/user/security_test.log`. 

The integration test will attempt to log in as `admin` using the password `password123`, and then attempt a SQL injection login using the username `admin' --`. If your fix is correct, the injection attempt should fail.