You are acting as a release manager preparing deployments for a polyglot microservice architecture. You need to automate the build process by parsing a release manifest, evaluating version codes, and orchestrating the builds.

In your home directory (`/home/user`), there is a build manifest file named `manifest.b32`. This file is Base32 encoded. When decoded, it is a CSV file containing the following columns:
`service_name,language,source_file,version_expr`

The `version_expr` column contains a mathematical expression as a string (e.g., `(4+6)*2-3`). 

Your task is to write a Python script at `/home/user/builder.py` that accomplishes the following:
1. Reads and decodes the `/home/user/manifest.b32` file.
2. Parses the decoded CSV data.
3. Evaluates the `version_expr` for each service to compute an integer version number. You must correctly handle standard mathematical order of operations and parentheses.
4. Orchestrates the builds for the services based on the `language` column:
   - If the language is `c`, compile the `source_file` using `gcc` into an executable named `<service_name>_<evaluated_version>`.
   - If the language is `go`, compile the `source_file` using `go build -o <output_name>` into an executable named `<service_name>_<evaluated_version>`.
5. Creates a directory named `/home/user/release/` and places all the successfully compiled executables inside it.
6. Writes a JSON log file to `/home/user/release_log.json` containing a dictionary mapping the `service_name` to its integer evaluated version. For example: `{"my_c_svc": 17, "my_go_svc": 42}`.

Once you have written `builder.py`, you must execute it so that the `/home/user/release/` directory is populated with the compiled binaries and `/home/user/release_log.json` is created. 

Assume that `gcc` and `go` are already installed and available in the system PATH. The source files referenced in the manifest are located in `/home/user/`.