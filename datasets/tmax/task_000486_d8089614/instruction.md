You are an AI assistant helping a bioinformatics researcher organize and secure their query infrastructure for a massive dataset of genomic graphs represented as NoSQL document collections.

The researcher uses a custom vendored Go package called `go-graphdoc` to translate high-level graph relationship queries into NoSQL aggregation pipelines. However, the system has two major issues:

1. **Broken Package**: The vendored package located at `/app/vendor/go-graphdoc` is currently failing to build and parse valid queries due to a recent bad patch. You need to investigate the package, find the perturbation (it's related to a broken regex or hardcoded environment variable in `parser.go` or `Makefile`), and fix it so the package compiles and functions correctly.
2. **Malicious Queries**: External collaborators submit JSON-formatted NoSQL query definitions. Some collaborators have submitted poorly constructed or malicious queries that cause unbounded graph traversals (DoS) or attempt to project unauthorized schema fields (e.g., `_internal_patient_id` or `auth_token`). 

Your task:
1. Fix the `go-graphdoc` package in `/app/vendor/go-graphdoc`. 
2. Write a Go command-line tool at `/home/user/detector.go` (which compiles to `/home/user/detector`) that uses the fixed `go-graphdoc` package to parse incoming JSON queries.
3. The tool must analyze the queries and act as a sanitiser/detector. It should inspect the schema mappings and aggregation pipelines.
4. The tool must reject queries that:
   - Access restricted fields: `_internal_patient_id`, `auth_token`, or `admin_notes`.
   - Contain `$lookup` or `$graphLookup` operations with a `maxDepth` greater than 5 or missing `maxDepth` entirely.
5. The tool must accept all other valid queries.

Usage of your tool must strictly be:
`/home/user/detector -input <directory_path> -output <log_file_path>`

For each `.json` file in the `<directory_path>`, your tool should write a single line to `<log_file_path>` in the exact format:
`[FILENAME] : [CLEAN|EVIL]`
(e.g., `query_12.json : CLEAN` or `query_14.json : EVIL`)

We have placed test queries in `/home/user/corpus/clean/` and `/home/user/corpus/evil/`. 
Ensure your detector correctly identifies 100% of the clean files as `CLEAN` and 100% of the evil files as `EVIL`. Output your final results for these corpora to `/home/user/results.log`.