You are assisting a technical writer in organizing and safely compiling raw documentation notes into a structured format for a static site generator.

The writer has a raw text file located at `/home/user/raw_docs.txt`. The file contains multiple documentation entries separated by a specific delimiter.

The format of `/home/user/raw_docs.txt` is as follows:
```
==DOC==
Title: <title text>
Author: <author name>
Body:
<multi-line body text until the next ==DOC== or EOF>
```

Your task is to create a Rust utility that reads this custom format from **Standard Input (stdin)**, converts it to a structured JSON file, and writes it to disk safely using an atomic write process.

Perform the following steps:
1. Initialize a new Rust executable project at `/home/user/doc_converter` using Cargo. You may add any standard dependencies like `serde` and `serde_json` to your `Cargo.toml`.
2. Write the Rust code in `/home/user/doc_converter/src/main.rs` to read the entire input from `stdin`.
3. Parse the custom format into a JSON array of objects. Each object must have the following string keys: `title`, `author`, and `body`. The `body` must retain its original newlines (excluding the newline immediately following `Body:` and stripping any trailing newlines before the next `==DOC==`).
4. **Safety requirement:** The writer's automated build system might read the output file at any time. To prevent it from reading a partially written file, your Rust program MUST perform an **atomic write**. You must write the JSON output to `/home/user/docs_final.json.tmp` first, and then use `std::fs::rename` to atomically rename it to `/home/user/docs_final.json`.
5. Compile your Rust program.
6. Execute your compiled Rust program by piping the contents of `/home/user/raw_docs.txt` into it.

When you are finished, the file `/home/user/docs_final.json` must exist, contain the properly formatted JSON array, and your source code must demonstrably use file renaming to achieve atomic writing.