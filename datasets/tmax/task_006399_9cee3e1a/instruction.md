As a localization engineer, I need to process a batch of translations, but our current tools keep breaking on rows with embedded newlines. I need you to build a robust data processing pipeline in Go.

Write a Go program at `/home/user/process.go` that implements a concurrent pipeline using goroutines and channels to process `/home/user/translations.csv`. The CSV has three columns: `id`, `english`, and `translated`.

Your pipeline must consist of the following stages connected by channels:
1. **Reader Stage**: Read the CSV file, correctly parsing fields even if they contain embedded newlines.
2. **Computation Stage**: For each row, calculate the Levenshtein distance between the `english` text and the `translated` text. You must implement the Levenshtein distance algorithm yourself in Go (case-sensitive, standard dynamic programming approach where insertions, deletions, and substitutions cost 1).
3. **Filter Stage**: Drop any row where the Levenshtein distance is strictly less than 5. We suspect these are either untranslated or just minor typos of the English source.
4. **Database Writer Stage**: Bulk insert the remaining valid rows into a SQLite database at `/home/user/valid_translations.db`. Create a table named `translations` with the following schema:
   `id` (TEXT PRIMARY KEY)
   `english` (TEXT)
   `translated` (TEXT)
   `distance` (INTEGER)

Make sure your Go program uses `github.com/mattn/go-sqlite3` for database operations. You can initialize the module in `/home/user` and run `go mod init process` and `go get github.com/mattn/go-sqlite3`.
After writing the code, run it so that the SQLite database is populated correctly.