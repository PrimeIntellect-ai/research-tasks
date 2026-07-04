You are a localization engineer managing an ETL pipeline for translation updates. You need to process time-series events indicating when certain translation keys were updated across different regions. 

We have an audio memo from the lead engineer detailing the timezone offsets for specific regions. This audio file is located at `/app/loc_config.wav`.

Your task is to write a Rust program that acts as a robust data transformation and sorting tool in our pipeline. 

Requirements:
1. Determine the timezone offsets in seconds for each region mentioned in the audio file `/app/loc_config.wav`.
2. Write a Rust program in `/home/user/src/main.rs` and compile it to exactly `/home/user/loc_processor`.
3. The program must read CSV data from standard input (STDIN) with no header. Each incoming line will have the format: `unix_timestamp,region_code,translation_key,word_count` (e.g., `1672531200,ES,ui.button.save,5`). All columns except `translation_key` and `region_code` are integers.
4. For each row:
   - Filter out and discard any row where the `region_code` is NOT one of the regions explicitly mentioned in the audio file.
   - For valid regions, calculate the `local_timestamp` by adding the region's specific offset (in seconds) to the `unix_timestamp`.
5. After reading all input, sort the records:
   - First, by `region_code` (alphabetically ascending).
   - Second, by `local_timestamp` (descending, latest first).
   - Third, by `translation_key` (alphabetically ascending).
6. Output the sorted records to standard output (STDOUT) in the following CSV format (no header):
   `region_code,local_timestamp,translation_key,word_count`

Your binary must be completely self-contained, statically compiled or compiled via standard `cargo build --release`, and explicitly copied/moved to `/home/user/loc_processor`. It should cleanly handle up to 1,000,000 lines of STDIN efficiently.