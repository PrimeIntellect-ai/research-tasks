As a localization engineer, you need to extract and prepare a batch of user reviews for our translation vendors. The vendor requires exactly 3 samples per `locale` and `category` combination to calibrate their models.

I have an SQLite database at `/home/user/loc_data.db` with a table named `reviews` that has the following schema:
`id INTEGER PRIMARY KEY, locale TEXT, category TEXT, user_email TEXT, review_text TEXT`

Write and execute a Go program at `/home/user/export_locales.go` that does the following:
1. **Stratified Sampling:** For every unique combination of `locale` and `category` present in the database, extract exactly 3 records. To select the records, first sort the available rows for that group by `id` in ascending order.
2. **Resampling / Gap-filling:** If a (locale, category) group has fewer than 3 records, you must repeat the available records to reach exactly 3. Do this by cycling through the sorted available records (e.g., if a group has records A and B, your sequence of 3 should be A, B, A. If a group has only record C, it should be C, C, C). If a group has more than 3 records, just take the first 3.
3. **Data Anonymization:** For privacy compliance, anonymize the `user_email` field in the extracted records. Replace the local part of the email (everything before the `@` symbol) with exactly `***`. Keep the domain intact (e.g., `john.doe@example.com` becomes `***@example.com`).
4. **Export:** Write the final prepared dataset to a CSV file at `/home/user/export.csv`. 
    - The CSV must include a header row: `id,locale,category,user_email,review_text`
    - The rows in the CSV must be sorted primarily by `locale` (ascending), secondarily by `category` (ascending), and finally by the order they were sampled within that group.

You are encouraged to use standard Go libraries or standard SQLite drivers (e.g., `github.com/mattn/go-sqlite3`). Use standard console commands to initialize your Go module and run the program.