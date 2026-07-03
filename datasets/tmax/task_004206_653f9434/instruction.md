You are a Database Reliability Engineer (DBRE) responsible for managing a complex web of database backup dependencies. Your organization's backup manifests are exported as RDF graphs (Turtle format). These graphs describe `Full` and `Differential` backups, and how they depend on each other via the `db:dependsOn` property.

Your task is to build an automated backup manifest validator. 

**Requirements:**
1. **Fix the vendored RDF library:** We provide a vendored copy of the `rdflib` package at `/app/vendor/rdflib`. However, a previous developer accidentally introduced a breaking change in its source code that prevents it from being imported or installed properly. You must find the perturbation, fix the source code, and install the library in your environment (e.g., using `pip install /app/vendor/rdflib`).
2. **Analyze the Backup Schema:** A backup graph contains nodes of type `db:Backup`. They have a `db:backupType` of either `"Full"` or `"Differential"`. Differential backups point to their parent backup via the `db:dependsOn` property.
3. **Write the Validator:** Create a Python script at `/home/user/validate_manifest.py`. The script must take exactly one argument: the path to a `.ttl` backup manifest file.
4. **Validation Logic:** 
   - A manifest is **VALID** if *every* `Differential` backup in the graph eventually traces back to a `Full` backup through a directed acyclic chain of `db:dependsOn` properties.
   - A manifest is **INVALID** if any `Differential` backup chain hits a dead end (no `Full` backup) or if there are circular `db:dependsOn` dependencies (which makes restoration impossible).
5. **Output:** Your script must print exactly the string `VALID` or `INVALID` to standard output (and nothing else) depending on the analysis of the provided `.ttl` file.

You must build this validator to successfully process the test manifests located in the system (which you do not have direct access to during development, but must anticipate). Rely on SPARQL queries or graph traversal in Python to ensure robustness.