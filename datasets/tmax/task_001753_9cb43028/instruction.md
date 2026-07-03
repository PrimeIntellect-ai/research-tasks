You are helping us maintain our localization pipeline. We process translation updates in bulk from various external services. Occasionally, our ETL system retries failed jobs, which produces duplicate translation update records with newer timestamps. 

We have a vendored C library, `loc-processor-1.0.0`, located at `/app/loc-processor-1.0.0`. It is supposed to compile into a static library and a CLI tool that deduplicates translation updates (keeping the latest timestamp), joins them with a base localization dictionary, calculates summary statistics (e.g., completeness percentage per language per day), and reshapes the data from a wide format (one column per language) to a long format (key, language, translation, timestamp).

However, the vendored package is currently broken. Due to a deliberate perturbation in its build system (a broken Makefile), it fails to compile correctly, preventing the deduplication logic from working. 

Your task is to:
1. Fix the build system in `/app/loc-processor-1.0.0` so that it correctly compiles the CLI tool `loc_tool`.
2. Write a C program at `/home/user/format_translations.c` that parses the output of `loc_tool` and reshapes the data. Your C program must read from stdin (which will be a CSV with columns: `timestamp, key, lang_es, lang_fr, lang_de`) and output to stdout in long format (`timestamp, key, lang, translation`). It must accurately handle missing values (empty strings) by skipping them, and it must bucket the timestamps to the nearest hour (e.g., `2023-10-14T15:32:00` becomes `2023-10-14T15:00:00`).

Your `format_translations` executable must behave EXACTLY identically to our reference binary when given various random inputs.

Constraints:
- You must write the final formatter in C.
- The output CSV must not contain header rows, just the raw data.
- Do not use external libraries other than standard C libraries.