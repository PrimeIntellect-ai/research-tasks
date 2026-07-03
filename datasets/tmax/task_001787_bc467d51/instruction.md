You are a localization engineer tasked with updating translations for a legacy application. The application generates a log file containing raw English UI strings, some of which contain slight typos or variations from the official translation database.

Your goal is to build an ETL script that extracts these strings, maps them to an existing Spanish translation database, and outputs a clean JSON file. 

Here are the requirements:
1. **Vendored Package:** You must use the `polib` library to parse the translation files. The source code for this library has been vendored at `/app/polib-1.2.0`. However, the previous engineer mentioned that this vendored version has a small bug preventing it from parsing files correctly (it throws a `TypeError` when evaluating translations). You must find and fix this bug in the vendored package, then install it in your environment.
2. **Data Extraction:** Read the file `/home/user/loc_task/ui_strings.txt`. Each line contains a log entry. Extract the actual UI string which is strictly enclosed in double quotes after the phrase `UI_EVENT:`. 
3. **Translation Mapping:** Load the Spanish translation file located at `/home/user/loc_task/es_ES.po` using the fixed `polib` library.
4. **Fuzzy Matching:** Iterate through the extracted UI strings. Try to find an exact match in the `.po` file (`msgid`). If an exact match is not found, use Python's built-in `difflib.get_close_matches` (use `n=1, cutoff=0.85`) to find the closest matching `msgid` in the `.po` file.
5. **Output:** Generate a JSON file at `/home/user/loc_task/translated_ui.json`. The JSON should be a dictionary where the keys are the *original extracted strings* (from the text file) and the values are the corresponding Spanish translations (`msgstr`). If no match (exact or fuzzy) is found, map the key to `null`.

Ensure your final output file `/home/user/loc_task/translated_ui.json` is properly formatted. Automated tests will evaluate the accuracy of your mapping against a ground-truth reference.