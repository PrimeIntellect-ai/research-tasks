You are assisting a researcher who is organizing a massive dataset of astronomical observations. They have a custom query language (AstroDSL) used by their team to query the dataset. These queries are compiled into SQL by a proprietary, stripped binary located at `/app/astro_dsl_compiler`.

Recently, junior researchers have been writing inefficient AstroDSL queries that, when compiled to SQL and executed against the SQLite database (`/app/astro_data.db`), cause severe performance issues (e.g., full table scans on multi-gigabyte tables, missing pagination).

Your task is to create a Rust-based query classifier that prevents bad queries from executing.

1. **Investigate the Binary and Database:**
   - The SQLite database is located at `/app/astro_data.db`. Inspect its schema and indexes.
   - The compiler binary `/app/astro_dsl_compiler` takes a single argument (the path to a `.astro` file) and prints the compiled SQL to `stdout`.

2. **Create the Classifier in Rust:**
   - Initialize a new Rust project at `/home/user/classifier`.
   - Write a CLI tool that takes exactly one argument: the path to a `.astro` file.
   - The tool must:
     a) Execute `/app/astro_dsl_compiler <file>` to get the generated SQL.
     b) Connect to `/app/astro_data.db` and use `EXPLAIN QUERY PLAN` to evaluate the query's execution plan.
     c) Parse the SQL or the plan to enforce the following rules:
        - The query **must** include a `LIMIT` clause, and the limit value must be strictly less than or equal to `100`.
        - The execution plan **must not** perform a full table scan (`SCAN TABLE`) on the `stars` or `observations` tables. Searches using indexes (`SEARCH TABLE`) are required for these.
   - The program must exit with status code `0` if the query is compliant ("clean"), and exit with status code `1` if it violates any of the rules ("evil").

3. **Build the Tool:**
   - Ensure your Rust project is compiled in release mode (`cargo build --release`).
   - The final binary must be located at `/home/user/classifier/target/release/classifier`.

You can test your logic by creating your own dummy `.astro` files and passing them to the compiler. Ensure your Rust program correctly classifies queries based on the database's query planner output.