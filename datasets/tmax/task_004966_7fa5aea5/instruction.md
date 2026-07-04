You are a localization engineer managing the translation telemetry pipeline for a global software product. Over the last month, we have received daily snapshot exports of our translation database, but we suspect an automated spambot has vandalized several translation strings over time. 

You must build an end-to-end Python-based ETL pipeline DAG that extracts, reshapes, sanitizes, and exports these translations. 

**Your Objective:**
Create an orchestration script `Makefile` or `pipeline.py` in `/home/user/` that automates the following workflow sequentially:

1. **Wide-to-Long Reshaping:**
   Read all daily snapshot CSV files located in `/app/data/snapshots/`. These files are in a wide format: `date, msg_id, en_US, fr_FR, es_ES, de_DE`. 
   Combine and reshape them into a single long-format time series CSV: `/home/user/reshaped_long.csv` with columns: `date, msg_id, locale, translation`.

2. **Adversarial Spam Filtering:**
   Write a Python script `sanitiser.py` that processes a long-format CSV and drops any rows containing "vandalized" translations.
   To detect vandalism, you must use the proprietary anomaly detection binary located at `/app/bin/eval_metric`. This tool evaluates a string and outputs a drift/spam score. You must reverse-engineer or query this black-box oracle to determine the exact threshold at which a translation is considered "spam" and filter those rows out.
   Save the sanitized output to `/home/user/sanitized_long.csv`.

3. **Database Bulk Import:**
   Bulk load the `sanitized_long.csv` data into a SQLite database located at `/home/user/locales.db` under a table named `translations_ts`. Optimize for bulk insertion speed.

4. **Template-Based Text Generation:**
   Write a Python script `generate_templates.py` that queries `locales.db` to extract only the *most recent* translation (by `date`) for each `msg_id` and `locale`.
   Using these latest clean translations, generate a Gettext `.po` file for each locale in `/home/user/templates/`. The files must be named `locale_<locale>.po`.
   Each `.po` file must follow this exact template structure:
   ```
   msgid "<msg_id>"
   msgstr "<translation>"
   ```

**Execution:**
The automated verifier will trigger your entire workflow by running your pipeline orchestrator (e.g., `make all` or `python pipeline.py`). 
Ensure all output files are generated precisely at the specified paths. Your `sanitiser.py` will also be independently evaluated against a hidden corpus of clean and evil translation CSVs to ensure your filtering logic is perfectly tuned to the `/app/bin/eval_metric` oracle.