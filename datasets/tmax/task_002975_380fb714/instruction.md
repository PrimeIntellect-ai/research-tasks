You are acting as a Release Manager building an automated deployment verification tool. You need to deploy a C++ microservice that verifies dependency graphs to ensure no peer dependency conflicts exist before a release is cut. 

We have decided to use a lightweight, bespoke HTTP server library called `tinyhttp` for this microservice. The source code for this library has been vendored into your environment at `/app/tinyhttp`. However, the vendored package has some deliberate issues you need to fix:
1. It fails to build/link out of the box due to a broken `Makefile` (missing thread linking).
2. There is a bug in its internal state machine in `parser.cpp` that causes it to miscalculate the `Content-Length` header, leading to truncated POST bodies. 

Your tasks are to:
1. Debug and fix the `/app/tinyhttp` library so it builds correctly and parses HTTP requests accurately.
2. Create a new C++ project in `/home/user/verifier` that links against your fixed `libtinyhttp.a`.
3. Implement an HTTP server listening on `127.0.0.1:9000`.
4. Create an endpoint `POST /verify` that accepts a plain-text payload representing a concrete dependency graph and verifies if all semantic versioning constraints are satisfied.

### Payload Format
The POST body will contain a list of resolved packages, followed by a `---` separator, followed by a list of dependency constraints.

Example:
```text
A 1.2.3
B 2.1.0
C 3.0.5
---
A -> B ^2.0.0
B -> C ~3.0.0
C -> D = 1.0.0
```

### Semantic Versioning Rules
You must implement a parser for versions (`X.Y.Z`) and three constraints:
* `= X.Y.Z` : Exact match required.
* `^ X.Y.Z` : Major version must match, and the resolved version must be greater than or equal to `X.Y.Z`. (e.g., `^2.1.0` allows `2.1.0`, `2.5.2`, but NOT `3.0.0` or `2.0.9`).
* `~ X.Y.Z` : Major and Minor versions must match, and the resolved version must be greater than or equal to `X.Y.Z`. (e.g., `~3.0.0` allows `3.0.5`, but NOT `3.1.0`).

### Endpoint Behavior
* If all constraints are satisfied by the provided packages, return HTTP status `200 OK` with the body `VALID\n`.
* If a package requires a dependency that is completely missing from the resolved list, return HTTP `400 Bad Request` with the body `MISSING <PkgName>\n` (e.g., `MISSING D`).
* If a package requires a dependency but the resolved version does not satisfy the constraint, return HTTP `400 Bad Request` with the body `CONFLICT <SourcePkg> -> <TargetPkg>\n` (e.g., `CONFLICT B -> C`). If there are multiple conflicts, returning the first one encountered is sufficient.

Start your server as a background process and leave it running on port 9000.