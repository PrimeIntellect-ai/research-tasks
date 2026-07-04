You are a build engineer responsible for modernizing an artifact generation pipeline. The current system relies on a legacy C program with a broken build configuration and an outdated SQLite database. You need to fix the build, migrate the database, and wrap the C tool in a modern Python gRPC service that uses a state machine to parse the tool's custom log format.

Complete the following objectives:

1. **Fix the Makefile and Compile the Legacy Builder**
   - The directory `/home/user/legacy_builder` contains `main.c` and a broken `Makefile`.
   - Fix the `Makefile` so that running `make` successfully compiles `main.c` into an executable named `/home/user/legacy_builder/builder`.

2. **Migrate the Artifact Database**
   - There is an existing SQLite database at `/home/user/db/artifacts.db`.
   - The current schema is `CREATE TABLE artifacts (id INTEGER PRIMARY KEY, name TEXT, size INTEGER)`.
   - Write and execute a Python script at `/home/user/db/migrate.py` to perform a schema migration. 
   - The new schema must replace the old table with `artifacts_v2` having the following columns: `id INTEGER PRIMARY KEY, name TEXT, size INTEGER, checksum TEXT, status TEXT`.
   - Migrate any existing records from `artifacts` into `artifacts_v2` (leaving `checksum` and `status` as NULL), and drop the old `artifacts` table.

3. **Define and Generate the gRPC Service**
   - Create a Protocol Buffers file at `/home/user/grpc/builder.proto`.
   - Define a package `buildsys` containing a service `ArtifactBuilder`.
   - The service must have an RPC method `BuildArtifact` that takes an empty `BuildRequest` message and returns a `BuildResponse` message with a `success` boolean field.
   - Generate the corresponding Python gRPC code inside `/home/user/grpc/` using `grpcio-tools`.

4. **Implement the State Machine Parser and gRPC Server**
   - Write a gRPC server in Python at `/home/user/grpc/server.py` that listens on `localhost:50051`.
   - When the `BuildArtifact` RPC is called, the server must:
     a) Execute the compiled `/home/user/legacy_builder/builder` subprocess.
     b) Parse the standard output of the builder using a state machine pattern. The output has a custom format containing multiple artifact records. A record starts with `>>> BEGIN_ARTIFACT` and ends with `<<< END_ARTIFACT`. Between these markers, there will be lines formatted as `NAME: <string>`, `SIZE: <integer>`, and `HASH: <string>`. Ignore all other output lines outside these blocks.
     c) For each successfully parsed artifact block, insert a new record into the `/home/user/db/artifacts.db` database (table `artifacts_v2`), setting `name`, `size`, `checksum` (from HASH), and `status` to the string `'BUILT'`.
     d) Return `success=True` in the response.

5. **Implement the Client and Export Data**
   - Write a Python script at `/home/user/grpc/client.py`.
   - The client must connect to the running gRPC server on `localhost:50051`, call `BuildArtifact`, and wait for the response.
   - After the RPC call completes successfully, the client must query the `/home/user/db/artifacts.db` database, retrieve all rows from `artifacts_v2`, and dump the result as a JSON array of objects to `/home/user/final_artifacts.json`.
   - The JSON objects should have keys: `"id"`, `"name"`, `"size"`, `"checksum"`, and `"status"`.

You may use standard Python libraries, `grpcio`, and `grpcio-tools`. Assume `grpcio-tools` is already installed.