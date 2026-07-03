You are a data engineer responsible for building a robust, high-performance ETL pipeline that cleans and normalizes multi-language text data for bulk database import. 

There are two main parts to your task: fixing a broken local library, and writing the ETL pipeline in Go.

**Part 1: Fix the Vendored Package**
We rely on a local, pre-vendored Go package located at `/app/go-nlp-utils` (module name: `github.com/dataeng/go-nlp-utils`). It provides specialized multi-language tokenization and Unicode normalization functions.
However, a recent botched commit broke the package. It currently fails to compile.
Your task is to:
1. Navigate to `/app/go-nlp-utils`.
2. Identify and fix the issues (there are dependency and configuration issues in the module setup, and a minor typo in `tokenizer.go`).
3. Ensure `go build` and `go test` pass successfully within that directory.

**Part 2: Build the ETL Pipeline**
Write a Go program at `/home/user/etl.go` and compile it to an executable at `/home/user/etl`. 
The program must read a CSV stream from `stdin` and write a transformed CSV to `stdout`.

**Input Format:**
Standard CSV from `stdin` with the header: `id,timestamp,lang,raw_text,score`
*   `id`: Integer.
*   `timestamp`: Integer (Unix epoch).
*   `lang`: String (ISO language code, may be empty).
*   `raw_text`: String (Arbitrary Unicode text, may contain newlines or commas quoted properly).
*   `score`: Float (May be empty/missing).

**Processing Rules:**
1.  **Imputation (lang):** If `lang` is empty, replace it with the string `"unknown"`.
2.  **Imputation (score):** If `score` is empty, interpolate it by "forward-filling" using the *most recently seen valid score* from the previously processed rows. If no valid score has been seen yet in the stream, use `0.00`.
3.  **Text Normalization:** Pass the `raw_text` through the fixed vendored package's function: `nlp.NormalizeAndTokenize(raw_text)`. (Make sure to import `github.com/dataeng/go-nlp-utils` in your code and set up your `go.mod` with a `replace` directive pointing to `/app/go-nlp-utils`).
4.  **Parallelism:** You should implement a parallel processing pattern (e.g., worker pool) to process the rows efficiently, but **CRITICALLY**, your final output to `stdout` must remain strictly ordered by the `id` column.

**Output Format:**
Write the cleaned data to `stdout` as a CSV (with header): `id,lang,clean_text,score`
*   `score` must be formatted to exactly 2 decimal places.
*   Make sure CSV rules are respected (quoting if necessary).

**Verification:**
Your compiled binary `/home/user/etl` will be rigorously tested against a reference implementation using fuzz testing. We will feed it thousands of randomly generated CSV rows to ensure your text processing, missing value imputation, and output ordering are bit-exact. Ensure you compile your final binary exactly to `/home/user/etl`.