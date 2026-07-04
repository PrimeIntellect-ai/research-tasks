You are tasked with porting and modernizing a legacy query engine into a minimal containerized environment. As part of this, you must migrate an old SQLite database, compile a legacy C component as a shared library, and expose the combined functionality via a REST API. You can write the API in any language available in the environment (e.g., Python, Node.js).

Here are the specific steps:

1. **Shared Library Management**:
   There is a C file located at `/home/user/app/userhash.c` containing a legacy hashing function. 
   Compile this C file into a shared library named `/home/user/app/libuserhash.so`. Ensure it is compiled correctly as a position-independent shared object.

2. **Schema Migration**:
   There is an SQLite database at `/home/user/app/data.db`. It has a single table `employees` with the schema:
   `CREATE TABLE employees (id INTEGER PRIMARY KEY, full_name TEXT, age INTEGER);`
   
   Perform a schema migration to update the table structure to:
   `CREATE TABLE employees (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, age_years INTEGER);`
   
   You must migrate the existing data. Split the `full_name` by the space character to populate `first_name` and `last_name`. Rename `age` to `age_years`. You may use temporary tables as is standard in SQLite. Drop the old table format completely.

3. **REST API Construction**:
   Write a REST API server in `/home/user/app/server` (you can add an extension like `.py` or `.js` depending on the language you choose) that listens on `127.0.0.1` port `8080`.
   The API must expose a single endpoint:
   `GET /api/employees/<id>`
   
   When queried, the API must:
   - Retrieve the employee record from `/home/user/app/data.db`.
   - Load the `libuserhash.so` shared library using FFI (e.g., `ctypes` in Python).
   - Call the C function `int compute_hash(int id)` from the shared library passing the employee's ID.
   - Return a JSON response exactly like this:
     `{"id": 1, "first_name": "Alice", "last_name": "Smith", "age_years": 30, "hash": 131}`
   Return a 404 HTTP status code if the employee ID does not exist.

4. **Testing / Verification**:
   Start your API server in the background. Once running, use `curl` to make a request to `http://127.0.0.1:8080/api/employees/1` and save the raw JSON response to `/home/user/result.json`.
   Ensure your API handles the request successfully and outputs valid JSON.