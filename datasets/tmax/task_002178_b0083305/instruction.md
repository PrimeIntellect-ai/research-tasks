You are assisting a technical writer in organizing a massive archive of legacy documentation logs. We have a proprietary, undocumented documentation compiler located at `/app/legacy_doc_parser` (a stripped binary). Unfortunately, the archives contain corrupted or "maliciously" formatted log entries that cause this legacy compiler to crash (segfault) or hang indefinitely.

Your task is to create a Rust-based sanitization tool that filters out these bad documentation logs before they reach the compiler. 

Here is what you need to do:
1. Analyze the `/app/legacy_doc_parser` binary against the provided sample data to determine exactly what triggers a crash. You have two sample corpora available:
   - `/app/corpus/clean.tar.gz`: Contains valid `.doclog` files that parse successfully.
   - `/app/corpus/evil.tar.gz`: Contains corrupted `.doclog` files that crash the parser.
2. Extract these archives and investigate the `.doclog` files. Each file contains a multi-line metadata header block (e.g., `Author:`, `Date:`, `Revision-History:`) followed by the documentation body. 
3. Write a Rust command-line tool in `/home/user/sanitizer/` (initialize it with `cargo new sanitizer`).
4. Your Rust tool must accept an input directory and an output directory:
   `cargo run --release -- --input <input_dir> --output <output_dir>`
5. The tool must recursively traverse the `<input_dir>`, find all `.doclog` files, parse their multi-line metadata headers, and copy ONLY the safe files to the identical relative path in the `<output_dir>`. It must entirely skip files that would crash the legacy parser.

The validation suite will run your Rust tool against a hidden test corpus containing both clean and evil files. To succeed, your tool must preserve 100% of the clean files and reject (not copy) 100% of the evil files.