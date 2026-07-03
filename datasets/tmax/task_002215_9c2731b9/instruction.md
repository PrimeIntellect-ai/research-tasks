You are a localization engineer tasked with modernizing a translation update pipeline. We have a batch of legacy binary resource files in `/home/user/data/resources/` that contain our application's strings. 

Unfortunately, the only tool that can read these files is an old, undocumented, stripped binary located at `/app/legacy_extractor`. When you pass a resource file to this binary (e.g., `/app/legacy_extractor /home/user/data/resources/app_v1.bin`), it outputs a CSV to `stdout` containing the translation keys and columns for multiple languages (`key`, `en_US`, `es_ES`, `fr_FR`, `ja_JP`). 

However, there are several issues you must fix by building a Python-based processing pipeline orchestrated via a bash script (`/home/user/run_pipeline.sh`):

1. **The Newline Bug**: The `legacy_extractor` has a known bug. If a translation string contains an embedded newline, the CSV output breaks, often splitting rows improperly or dropping the trailing quotes. Your pipeline must capture the binary's stdout and repair these broken CSV rows before parsing.
2. **Reshaping**: The data is currently in wide format (one column per locale). You must reshape this into a long format CSV saved at `/home/user/data/processed/long_translations.csv` with columns: `key`, `locale`, `translation`.
3. **Imputation**: Some translations are missing (empty strings). You must impute missing values by falling back to the `en_US` string, but prefixing it with `[UNTRANSLATED] `.
4. **Stratified Sampling**: For our QA team, create a stratified sample of the translations. Select exactly 10% of the keys (random seed 42) and export all their locale variants into `/home/user/data/processed/qa_sample.csv`.
5. **Translation Service**: Finally, you must write and start a Python HTTP server listening on `127.0.0.1:8080`. The server must expose a GET endpoint `/api/v1/strings?locale=<locale_code>` which returns a JSON object mapping translation keys to their imputed translated strings for the requested locale. 

Your bash script `/home/user/run_pipeline.sh` must execute the entire DAG: running the binary on all `.bin` files in the resources directory, combining the outputs, repairing the data, reshaping/imputing/sampling, and finally launching the HTTP server in the background. Write logs to `/home/user/pipeline.log`.