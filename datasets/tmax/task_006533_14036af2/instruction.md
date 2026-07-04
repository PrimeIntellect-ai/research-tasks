You are a configuration manager tasked with tracking changes across two different environments. The raw configuration dumps are messy, containing unstructured notes and inconsistently formatted values.

You have been provided with two configuration dumps:
- `/home/user/old_state.txt`
- `/home/user/new_state.txt`

Each line in these files represents a configuration parameter and follows this exact pattern:
`SERVICE[<service_name>] param:<key_name> | val:<value_string> // <optional_notes>`

Your task is to extract, normalize, and compare the configurations to identify what has changed (additions, removals, and modifications).

### Step 1: Extraction & Normalization
Extract the `<service_name>`, `<key_name>`, and `<value_string>` from each line. 
You must normalize the `<value_string>` using the following rules, in order:
1. Strip any surrounding double quotes (`"`) from the value string (e.g., `"value"` becomes `value`). Note: Quotes will only appear at the very beginning and/or end of the extracted value string before stripping.
2. Convert the entire string to lowercase.
3. Replace all hyphens (`-`) and underscores (`_`) with spaces (` `).
4. Collapse any consecutive multiple spaces into a single space.
5. Trim any leading and trailing spaces from the resulting string.

*(For example, `"  SCRAM-SHA_256  "` becomes `scram sha 256`)*

### Step 2: Comparison
Compare the normalized old configuration against the normalized new configuration. A key is uniquely identified by the combination of its `service_name` and `key_name`.
- If a key exists in the new state but not the old state, its status is `added`.
- If a key exists in the old state but not the new state, its status is `removed`.
- If a key exists in both but the *normalized* values differ, its status is `modified`.
- If the *normalized* values are identical, ignore the key (it is unchanged).

### Step 3: Output Generation
Generate a JSON file at `/home/user/config_diff.json` containing the differences. The JSON structure must exactly match this format:

```json
{
  "service_name": {
    "key_name": {
      "status": "added|removed|modified",
      "old_value": "normalized_old_value_or_null",
      "new_value": "normalized_new_value_or_null"
    }
  }
}
```
If a key is `added`, `old_value` must be `null`.
If a key is `removed`, `new_value` must be `null`.

Write a script in Python, Perl, Ruby, or Bash to process the data and produce the required JSON file.