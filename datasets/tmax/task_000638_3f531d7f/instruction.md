You are a data engineer tasked with building an ETL pipeline to extract hierarchical product data (Bill of Materials) from an undocumented SQLite database and export it to a structured JSON format.

We have a legacy Rust tool located at `/app/bom_extractor`. It is supposed to connect to a SQLite database, reverse engineer the data model to find the hierarchical part relationships, execute a recursive query to build the full Bill of Materials (BOM) for a given top-level product ID, and output the result as JSON. 

However, the vendored package is currently broken. It fails to build or run correctly.

Your tasks are:
1. Inspect the vendored Rust package at `/app/bom_extractor` and fix any build or configuration issues.
2. Analyze the provided sample SQLite database at `/app/data/sample.db` to reverse engineer the schema. The database contains tables for `parts` and `assemblies` (which links a parent part to multiple child parts with quantities).
3. Update the SQL query in the Rust tool to use a Recursive CTE (Common Table Expression) that computes the full expanded BOM for a given parent part ID. The CTE must calculate the accumulated quantity for each sub-part (e.g., if assembly A requires 2 of B, and B requires 3 of C, A requires 6 of C).
4. The tool must accept two arguments: the SQLite database path and the target top-level part ID.
5. The output must be written to standard output as a JSON array of objects, sorted by `part_id` ascending. Each object must have the following format:
   `[{"part_id": 123, "part_name": "Screw", "total_quantity": 6}, ...]`
6. Ensure the Rust binary can be built cleanly with `cargo build --release`. The final executable will be at `/app/bom_extractor/target/release/bom_extractor`.

You are expected to fix the Rust project and implement the logic so that it matches this exact output format for any valid database matching the inferred schema.