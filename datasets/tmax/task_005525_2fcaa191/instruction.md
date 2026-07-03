You are a localization engineer managing a translation pipeline. We have a Go-based ETL tool that processes translated CSV files, validates them against a source English CSV, and extracts features for our frontend.

Currently, the pipeline has several issues:
1. It silently drops or mangles strings with embedded newlines because it uses a naive line-by-line scanner.
2. It lacks constraint validation to ensure format specifiers (like `%s`, `%d`, `%f`) in translations match the source strings exactly.
3. It doesn't automate processing across multiple languages.

Your task is to fix the Go code, implement the required validation and extraction logic, and orchestrate the pipeline.

**Files provided (assume they exist in `/home/user/`):**
- `/home/user/locales/en_US.csv`: The source strings. Format: `id,text`
- `/home/user/locales/fr_FR.csv`: French translations. Format: `id,translation`
- `/home/user/locales/es_ES.csv`: Spanish translations. Format: `id,translation`
- `/home/user/processor.go`: A broken Go script that attempts to process a target locale against the source.

**Requirements:**

1. **Fix CSV Parsing**: Modify `/home/user/processor.go` to correctly handle CSV fields with embedded newlines. Use Go's standard `encoding/csv` package instead of `bufio.Scanner`.
2. **Constraint-based Validation**: For every string ID, count the occurrences of `%s`, `%d`, and `%f` in the source string. The target translation MUST have the exact same count for each of these placeholders. 
   - If a translation fails this validation, it should NOT be included in the output.
   - Instead, append the failing `id` on a new line to an error log named `/home/user/errors_<locale>.log` (e.g., `errors_fr_FR.log`).
3. **Feature Extraction**: For valid translations, extract the string length (number of bytes) of the target translation. Output a single JSON object mapping the string `id` to its integer byte length, saved to `/home/user/output_<locale>.json` (e.g., `output_fr_FR.json`).
4. **Pipeline Orchestration**: Create a bash script at `/home/user/run_pipeline.sh` that:
   - Compiles `processor.go`.
   - Discovers all CSV files in `/home/user/locales/` EXCEPT `en_US.csv`.
   - Executes the compiled Go program for each discovered translation file, passing `en_US.csv` as the source and the target CSV as the translation input. (You can define the CLI arguments for your Go program however you like, as long as `run_pipeline.sh` calls it correctly).

Make sure your bash script is executable and run it to produce the final `.json` and `.log` files in `/home/user/`.