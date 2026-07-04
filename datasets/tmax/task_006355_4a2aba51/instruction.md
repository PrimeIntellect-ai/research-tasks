You are a localization engineer tasked with building an automated Python ETL pipeline to process and update translation files. 

Our application's raw translations are stored in a simulated "remote" directory at `/tmp/remote_l10n_source/`. We need you to pull these files, process them to impute missing translations, group them by application context, log the pipeline metrics, and deploy the final archive to a destination directory `/tmp/remote_l10n_dest/`.

Here are the specific requirements for your Python script (save it as `/home/user/l10n_pipeline.py` and run it):

1. **Source Data**:
   - Directory `/tmp/remote_l10n_source/` contains `en.json`, `es.json`, and `fr.json`.
   - `en.json` is the source of truth. Every valid translation object has three keys: `id`, `context`, and `text`.
   - `es.json` and `fr.json` may have missing translation objects (missing `id`s compared to `en.json`), or objects where the `text` value is `null` or empty `""`.

2. **Imputation Rules (for languages other than 'en')**:
   - If a translation text is missing (either the whole object is missing, or `text` is `null`/empty), you must impute it.
   - First, check the glossary CSV file at `/home/user/glossary.csv`. The CSV has headers: `id,lang,text`. If a translation exists for the missing `id` and language, use it.
   - If it is NOT in the glossary, interpolate it by taking the `text` from `en.json` and prefixing it with `[TBD] ` (e.g., if English is "Hello", use `[TBD] Hello`).

3. **Sorting and Grouping**:
   - Processed files must be saved locally first in `/home/user/processed_l10n/`.
   - Group the translations by language, and then by `context`.
   - The directory structure should be: `/home/user/processed_l10n/<lang>/<context>.json`
   - Within each `<context>.json` file, the output should be a JSON array of objects (just `{"id": "...", "text": "..."}` - drop the context key in the output objects to save space).
   - The objects in the JSON array MUST be sorted alphabetically by `id`.
   - Use standard JSON formatting with a 2-space indent.

4. **Pipeline Logging**:
   - Configure Python's standard `logging` module to output to `/home/user/pipeline.log` at the `INFO` level.
   - For every language processed (including English), log: `INFO: Processing language <lang>`
   - For languages other than English, log a warning with the exact number of imputed keys: `WARNING: Imputed <N> missing keys for <lang>`
   - After processing a language, log: `INFO: Exported <M> context groups for <lang>`

5. **Remote Transfer**:
   - After processing, compress the entire `/home/user/processed_l10n/` directory into a tarball named `l10n_release.tar.gz`.
   - Transfer (copy) this tarball to the simulated remote destination: `/tmp/remote_l10n_dest/l10n_release.tar.gz`.

Run your script to complete the pipeline. The final system state should have the log file, the intermediate processed files, and the final deployed tarball.