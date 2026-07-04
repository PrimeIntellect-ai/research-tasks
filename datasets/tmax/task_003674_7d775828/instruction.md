You are a developer tasked with fixing a broken Go application that resolves package dependencies. The project is located in `/home/user/api-version-resolver`. 

Currently, the application fails to compile and has logical bugs. It is supposed to act as a small REST API that parses two JSON files containing dependency versions, compares them using Semantic Versioning (SemVer), and returns a sorted list of packages that need to be updated.

Here is what you need to do:
1. Fix the Go code in `/home/user/api-version-resolver/main.go`. 
2. The code must provide an HTTP REST API listening on port `8080`.
3. It should expose a single `GET` endpoint at `/updates`.
4. When `/updates` is called, the program must read `/home/user/api-version-resolver/current.json` and `/home/user/api-version-resolver/wanted.json`. Both files contain key-value pairs mapping package names to version strings (e.g., `"1.2.3"`).
5. The endpoint must compare the versions using proper Semantic Versioning logic (MAJOR.MINOR.PATCH). Do not use simple string comparison, as "1.10.0" is greater than "1.2.0".
6. The endpoint must return a JSON array of objects representing packages where the `wanted` version is strictly *greater* than the `current` version.
7. The returned JSON array MUST be sorted alphabetically by the `package` name.
8. The JSON response structure must look exactly like this:
   `[{"package": "pkgA", "from": "1.0.5", "to": "1.1.0"}, {"package": "pkgC", "from": "0.9.9", "to": "1.0.0"}]`
9. Once the code is fixed, compile and run the server in the background.
10. Fetch the result by running `curl -s http://localhost:8080/updates > /home/user/updates.json`.
11. You can then terminate the Go server.

Ensure the final output file `/home/user/updates.json` exists, contains valid JSON, and correctly identifies all outdated packages according to SemVer rules.