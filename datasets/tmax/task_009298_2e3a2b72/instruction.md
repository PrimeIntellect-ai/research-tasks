You are a localization engineer managing a Translation Memory (TM) database. You've received a large batch of translation updates from multiple vendors, but the data is noisy. Some vendors have submitted duplicate translations, and others have used faulty Machine Translation (MT) scripts that produce output of abnormal lengths.

Your task is to build a multi-stage Python data pipeline to deduplicate the dataset, compute rolling statistics, and detect anomalous translations based on character length ratios.

The input file is located at `/home/user/tm_updates.jsonl`. Each line is a JSON object with the following keys:
- `id`: A unique string identifier.
- `timestamp`: An ISO-8601 formatted datetime string.
- `source_lang`: The language code of the source text.
- `target_lang`: The language code of the target text.
- `source_text`: The original string.
- `target_text`: The translated string.

Write and execute a Python script that performs the following pipeline exactly as specified:

**Phase 1: Hash-Based Deduplication**
1. Deduplicate the records across the entire dataset.
2. Two records are considered duplicates if they have the same MD5 hash for the concatenated string: `<source_lang>_|<target_lang>_|<source_text>`.
3. When duplicates are found, keep ONLY the record with the most recent (latest) `timestamp`. Discard the older ones.

**Phase 2: Filtering and Sorting**
1. Filter the deduplicated dataset to keep ONLY records where `source_lang` is `"en"` and `target_lang` is `"fr"`.
2. Sort the remaining records strictly in ascending chronological order based on their `timestamp`.

**Phase 3: Rolling Statistics and Changepoint Detection**
1. For each translation, calculate the length ratio: `R = length(target_text) / length(source_text)`. (Lengths are based on the number of characters).
2. For each record $i$ in the sorted timeline, calculate the rolling mean ($\mu$) and sample standard deviation ($s$) of the length ratios of the *strictly preceding* records, up to a maximum window of 30 previous records. (Do not include the current record $i$ in its own window).
3. If a record has fewer than 10 preceding records in its window, do NOT flag it (it requires at least 10 prior records to establish a baseline).
4. A record is flagged as an anomaly if its ratio $R_i$ satisfies: $|R_i - \mu| > 3 \times s$.

**Phase 4: Output**
Write the `id` of every anomalous translation you find to a file at `/home/user/flagged_translations.txt`, one ID per line, in the chronological order they were processed.