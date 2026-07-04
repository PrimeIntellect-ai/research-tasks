You are a localization engineer managing an ETL pipeline for translation files. Your goal is to process new English strings, merge them with existing French translations, fill in missing gaps using a legacy Translation Memory (TM) file, and schedule the process.

We have a vendored C library for localization processing at `/app/libloc-0.1.0`. However, the vendor shipped it with a broken build configuration, so it currently fails to compile. 

Your tasks:
1. **Fix the Vendored Package**: Inspect `/app/libloc-0.1.0`. Find and fix the intentional perturbation in the package (a misconfigured `Makefile` preventing compilation). Build and install it so you can link against `libloc.a` and include `loc.h`.
2. **Develop the C ETL Tool**: Write a C program at `/home/user/localize.c` that uses `<regex.h>` and the fixed `libloc` library to:
   - Read the base English strings from `/home/user/base_en.csv` (Format: `Key,String`).
   - Read the current French translations from `/home/user/updates_fr.csv` (Format: `Key,String`). This file is incomplete (contains gaps).
   - Read the legacy TM file `/home/user/tm_fr.txt`. This file uses a non-standard format that you must parse using C POSIX regex: `[[KEY]] === {{TRANSLATION}}`. 
   - **Normalize**: Standardize whitespace in all loaded strings (replace multiple contiguous spaces with a single space, strip leading/trailing spaces).
   - **Join and Gap-Fill**: For every key in `base_en.csv`, try to find its translation in `updates_fr.csv`. If it is missing, search the parsed `tm_fr.txt` to gap-fill the translation. If still missing, leave the translation empty.
   - **Output**: Write the merged and filled translations to `/home/user/final_fr.csv` in the format `Key,Translation`.
3. **Pipeline Scheduling**: Create a wrapper bash script `/home/user/run_etl.sh` that compiles (if necessary) and runs your C program. Then, write a valid crontab line into `/home/user/cron.txt` that schedules `/home/user/run_etl.sh` to run at 2:00 AM every Monday through Friday.

The success of your task will be evaluated using an automated metric script that calculates the extraction and gap-filling accuracy of `/home/user/final_fr.csv` against a hidden golden dataset. You must achieve an Accuracy >= 0.95.