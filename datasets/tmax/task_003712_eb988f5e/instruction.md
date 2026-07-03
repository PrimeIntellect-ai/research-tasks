You are a localization engineer tasked with preparing a translation update. 

We have a large export of translation strings in a JSON-lines format located at `/home/user/locales.jsonl`. However, the export tool had a bug and generated invalid unicode escape sequences in some of the strings (e.g., missing hex digits like `\u202` instead of `\u2022`). Because of this, standard JSON parsers like `jq` or Python's default `json.loads` will crash or throw errors when reading these lines.

Your task is to write a script (using Bash, Awk, Perl, Python, etc.) that processes this file line-by-line (to support large-file streaming) and extracts the `id`, `en`, and `fr` fields. 

You need to create an output file at `/home/user/missing_fr.tsv` with the following requirements:
1. It must be a Tab-Separated Values (TSV) file.
2. The first line must be the header: `id[TAB]en[TAB]fr`
3. You must extract the `id`, `en`, and `fr` string values from each line. 
4. If the `fr` field is completely missing from the JSON line, or if its value is an empty string `""`, you must impute the value by setting it to `[TODO] ` followed by the `en` value (e.g., `[TODO] Save`).
5. Include all keys in the output TSV, even if they had valid `fr` translations.
6. Handle the broken unicode escapes gracefully (e.g., by extracting the raw string text without attempting to strictly decode the invalid unicode, or by fixing/stripping the invalid escapes before parsing). 

Ensure your final output is perfectly formatted as a TSV.