You are tasked with fixing a broken configuration management pipeline. Our legacy ETL job produces duplicate configuration records upon retry, and we need a robust deduplication filter written in C.

Additionally, the output format for the deduplicated records has been updated. The new format template is embedded in an image file left by the previous engineer at `/app/watermark.png`.

Your objectives are:
1. Extract the exact output template string from the image at `/app/watermark.png`. Tesseract is installed on the system.
2. Write a C program at `/home/user/dedup_processor.c` and compile it to an executable named `/home/user/dedup_processor`.
3. The executable must read a stream of comma-separated values (CSV) from standard input (`stdin`). 
   - The CSV format is strictly: `timestamp,config_id,revision,value`
   - `timestamp`: Integer
   - `config_id`: 3-character uppercase string (e.g., "ABC")
   - `revision`: Integer
   - `value`: String (up to 32 alphanumeric characters)
4. The program must deduplicate the records. If multiple records share the same `config_id`, your program must ONLY keep the record with the highest `timestamp`. (You can assume timestamps for a given ID are unique).
5. After reading `EOF`, the program must print the deduplicated records to standard output (`stdout`).
6. The output records must be sorted alphabetically by `config_id`.
7. Each output record must be formatted EXACTLY according to the template string you extracted from `/app/watermark.png`. Replace the placeholders in the template with the `config_id`, `revision`, and `value` respectively. (Note: The timestamp is used for deduplication but is not printed).
8. Ensure your program handles up to 5,000 input lines efficiently. 

Do not print any debug information to stdout; only print the final formatted records, each on a new line. The executable will be heavily fuzzed against a reference implementation to ensure exact bit-for-bit equivalence in output.