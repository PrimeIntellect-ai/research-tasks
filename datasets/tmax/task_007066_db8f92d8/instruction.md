You are a data engineer building a localized ETL pipeline for an international e-commerce platform.

Your task is to write a Rust application that processes a stream of product data, validates it, generates localized SEO text, and exports it as a CSV file ready for database bulk import.

**Input Data:**
There is a JSON Lines (JSONL) file located at `/home/user/products.jsonl`. 
Each line contains a JSON object with the following schema:
- `id` (integer)
- `names` (object/dictionary: locale string -> localized name string)
- `price` (integer)
- `stock` (integer)

**Requirements:**
1. **Setup:** Create a new Cargo project at `/home/user/etl_pipeline`. You may add necessary standard crates like `serde`, `serde_json`, and `csv` to your `Cargo.toml`.
2. **Streaming:** Read the file `/home/user/products.jsonl` line-by-line to avoid loading the entire large file into memory.
3. **Data Validation:** Filter out and ignore any products that fail ANY of these constraints:
   - `price` is less than 0
   - `stock` is exactly 0
   - The `names` object does NOT contain the key `"ja-JP"`
4. **Template-Based Generation:** For each valid product, generate a Japanese SEO text string using exactly this template:
   `【大特価】<NAME>がたったの<PRICE>円！`
   Replace `<NAME>` with the `"ja-JP"` localized name, and `<PRICE>` with the product's price.
5. **Bulk Export:** Write the valid, processed records to a CSV file at `/home/user/bulk_import.csv`.
   - The CSV must include a header row: `id,name_ja,seo_text,price`
   - Use standard commas for delimiters and double quotes if quoting is necessary.

Compile and run your Rust program so that `/home/user/bulk_import.csv` is completely generated before you finish the task.