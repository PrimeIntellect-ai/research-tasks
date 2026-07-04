You are a Database Reliability Engineer responsible for the automated backup pipeline of our multi-model datastore. Our system uses a combination of relational structures, NoSQL documents, and a dependency graph to represent customer infrastructure. 

You have two main objectives:

**1. Fix the Vendored Backup Extractor**
We use a custom, in-house Go tool called `graph-backup-extractor` to materialize our graph relationships into JSON documents for backup. The source code for this package is pre-vendored at `/app/graph-backup-extractor-v2.1.0`. 
Recently, a junior developer made a commit that broke the tool. It no longer builds due to a broken `Makefile` and a missing environment variable mapping in `config.go` for the `NEO4J_URI` connection string, causing it to fail during initialization.
Your task is to:
- Identify and fix the perturbation in the `Makefile` and `config.go` inside `/app/graph-backup-extractor-v2.1.0`.
- Ensure `make build` successfully compiles the binary `bin/extractor`.

**2. Create a Backup Sanitizer (Result Processing)**
The extracted JSON backup documents occasionally contain malicious injection payloads (simulating NoSQL injection attempts) or sensitive PII that violates our retention policies. 
Write a Go program at `/app/sanitizer.go` that implements a detector/classifier. It must accept a directory path as an argument and process all `.json` files within it. 
For each file, it should evaluate the backup document. If it contains known malicious NoSQL operators (e.g., `$where` clauses with javascript, or nested `$ne` brute-forcing patterns) or exposed unencrypted SSNs (formatted as `XXX-XX-XXXX`), it must reject the file (outputting `REJECTED: <filename>` to stdout). If the file is safe, it must output `ACCEPTED: <filename>`.

We have provided two test corpora:
- `/app/corpora/clean/`: Contains 50 safe backup documents.
- `/app/corpora/evil/`: Contains 50 documents with NoSQL injection patterns and exposed SSNs.

Compile your sanitizer to `/app/sanitizer`.
Our automated tests will run:
`/app/sanitizer /app/corpora/clean/`
`/app/sanitizer /app/corpora/evil/`

Your sanitizer must ACCEPT 100% of the clean corpus and REJECT 100% of the evil corpus. Write the results of your tests to `/app/sanitizer_results.log`.