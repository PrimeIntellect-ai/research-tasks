You are a localization engineer processing an automated data dump. An ETL job that extracts translation strings failed and retried, resulting in duplicate records in our raw data file. We need to clean this data, reshape it, and prepare a sample for the Quality Assurance (QA) team.

Write a C program (e.g., `/home/user/process.c`) and run it to process the file `/home/user/translations_raw.csv`. The CSV has the following long format: `key,lang,text,timestamp`.

Your task is to:
1. **Deduplicate and Clean**: Identify records with the same `key` and `lang`. Keep only the translation with the highest (most recent) `timestamp`.
2. **Reshape (Long to Wide)**: Transform the data into a wide format where each row represents a unique `key` and columns represent the target languages. The target languages we care about are `en`, `fr`, and `es`.
3. **Save Full Wide Format**: Write the reshaped data to `/home/user/translations_wide.csv`. Include the header `key,en,fr,es`. Sort the rows alphabetically by `key`. If a translation is missing for a specific language, leave the field empty (e.g., `ERR_404,Not Found,,No Encontrado`).
4. **Data Sampling**: The QA team needs a small, complete subset for manual review. Extract exactly the first 2 keys (alphabetically) that possess a translation for **all three** languages (`en`, `fr`, and `es`). Save this sample to `/home/user/sample_qa.csv` with the same header and format as the wide file.

Do not use external dependencies or libraries other than standard C libraries (e.g., `<stdio.h>`, `<stdlib.h>`, `<string.h>`).