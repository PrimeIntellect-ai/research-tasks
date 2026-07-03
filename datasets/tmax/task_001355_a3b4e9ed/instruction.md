You are a localization engineer managing a high-volume translation pipeline. You receive a continuous stream of translation string updates from various contractors, but recently, some automated translation tools have been injecting poor quality, overly verbose translations that break the UI layout. 

Your task is to write a Go program that processes a log of translation updates, applies quality control gates, groups the data, and computes rolling statistics to detect anomalous string expansions.

The input data is located at `/home/user/loc_updates.jsonl`. Each line is a JSON object representing a single translation update:
`{"ts": <unix_timestamp_int>, "lang": "<language_code_string>", "mod": "<module_name_string>", "id": "<string_id>", "old": "<old_text>", "new": "<new_text>"}`

Write a Go program (e.g., `process_loc.go`) that performs the following steps:

1. **Validation & Quality Gate:** Read the JSONL file. Reject any update that meets ANY of the following conditions:
   - `lang` is not exactly two lowercase letters (e.g., `en`, `fr` are valid; `EN`, `eng`, `e1` are invalid).
   - `new` is an empty string.
   - `old` and `new` are exactly identical strings.
   Write the total number of rejected lines to `/home/user/rejected_count.txt` (just the integer).

2. **Sorting and Grouping:** For all valid updates, group them by `lang` and `mod`. Within each `lang` + `mod` group, sort the updates chronologically by `ts` in ascending order. If two updates have the exact same `ts` in the same group, sort them alphabetically by `id`.

3. **Rolling Statistics for Anomaly Detection:** For each sorted group, we want to track how much the translations are expanding over time.
   - For every valid update, calculate the length ratio `R = byte_length(new) / (byte_length(old) + 1)`. Use standard byte length (not rune count).
   - Maintain a rolling average of `R` over the **last 5 valid updates** in that specific `lang` + `mod` group (i.e., the current update and up to 4 previous ones). If a group currently has fewer than 5 updates, calculate the average using the available updates.
   - If the rolling average strictly exceeds `2.500`, flag the string `id` of the current update.

4. **Output:** Extract the unique `id`s of all flagged updates. Sort these `id`s alphabetically and write them to `/home/user/flagged_ids.txt`, one `id` per line.

Ensure your Go program is completely self-contained, compiles, and runs using the standard Go toolchain. Execute your program so that the output files (`rejected_count.txt` and `flagged_ids.txt`) are generated in `/home/user/`.