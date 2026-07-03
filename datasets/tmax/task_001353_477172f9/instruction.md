You are an AI assistant acting as a compliance officer auditing an internal financial tracking system. Recently, analysts have been submitting poorly constructed SQL queries that cause severe performance degradation and potential cross-tenant data leakage. Specifically, they are submitting queries with implicit cross joins and failing to parameterize sensitive tenant filters.

Your task is to build a Go-based query validator that can automatically audit SQL queries and reject non-compliant ones.

Here is your workflow:
1. **Extract Compliance Schema:** There is an image located at `/app/schema_rules.png`. It contains the exact table names and the strict compliance rules for querying them (you have `tesseract` installed to read it). You must base your validation logic on the exact text hidden in this image.
2. **Reverse Engineer the Data Model:** Based on the rules and table names extracted from the image, determine the patterns of implicit cross joins that are occurring.
3. **Build the Validator in Go:** 
   - Create a Go program at `/home/user/validator.go` and compile it to `/home/user/validator`.
   - The CLI signature must be: `./validator <path_to_sql_file>`
   - The program must print any validation errors to standard output and exit with code `1` if the query is non-compliant ("evil").
   - It must exit with code `0` if the query is fully compliant ("clean").
4. **Test against the Corpora:** You have been provided with test data:
   - `/app/corpus/clean/`: Contains perfectly formatted, compliant SQL queries. Your validator MUST accept 100% of these.
   - `/app/corpus/evil/`: Contains queries violating the rules (e.g., implicit cross joins, hardcoded tenant IDs). Your validator MUST reject 100% of these.

A successful task completion means `./validator` correctly processes both directories according to the exact rules specified in `/app/schema_rules.png`. You may use standard Go libraries or download third-party SQL parsers (like `github.com/xwb1989/sqlparser`) if you prefer, but standard string matching/regex is sufficient given the predictable formatting of the corpus.