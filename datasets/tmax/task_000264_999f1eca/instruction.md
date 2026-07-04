You are a data scientist taking over a partially completed data cleaning and reporting pipeline. 

We have a SQLite database located at `/app/sales.db` containing two tables:
1. `customers` (`id` INTEGER PRIMARY KEY, `name` TEXT)
2. `transactions` (`tx_id` INTEGER PRIMARY KEY, `customer_id` INTEGER, `amount` REAL)

The lead data analyst left a voice note with a crucial business rule for calculating our summary statistics. This audio file is located at `/app/analyst_note.wav`.

Your task is to:
1. Transcribe the audio file `/app/analyst_note.wav` to discover the specific filtering rule for transactions. You have access to `whisper.cpp` located at `/opt/whisper.cpp/main` with a model at `/opt/whisper.cpp/models/ggml-tiny.en.bin` (or you may use standard tools like `ffmpeg` if you prefer).
2. Create a Bash script at `/home/user/generate_report.sh` that takes a single Customer ID (integer) as its first argument (`$1`).
3. The script must execute a query against `/app/sales.db` that joins the `customers` and `transactions` tables, applies the filtering rule heard in the audio file, and calculates the total (sum) and average transaction amounts for that customer.
4. The output printed to `stdout` by your Bash script must EXACTLY match the following format:
   `Customer <Name> (ID: <id>): Total=<Sum>, Avg=<Average>`
   *Note: Both `<Sum>` and `<Average>` should be formatted to exactly 2 decimal places.*
5. If the customer exists but has no valid transactions remaining after applying the filter rule, the script should instead output:
   `Customer <Name> (ID: <id>): No valid transactions`
6. If the customer does not exist in the database at all, the script should output nothing and exit with code 1.

Your script will be tested against many different customer IDs automatically. Ensure it is robust, handles SQL queries cleanly within Bash, and produces bit-exact string matches. Make sure the script has executable permissions.