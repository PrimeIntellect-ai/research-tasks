You are a localization engineer tasked with updating the translation files for a mobile application. The translation team has uploaded a new batch of strings in a wide-format CSV to a remote shared directory, and you need to process them into localized Android string XML files.

Please complete the following workflow:

1. **Local-Remote Transfer**:
   The translations are located on a simulated remote mount at `/tmp/remote_l10n/translations.csv`. Copy this file into your local working directory: `/home/user/workspace/`.

2. **Data Reshaping (Python)**:
   Write a Python script at `/home/user/workspace/process.py` that reads the copied `translations.csv`. The input CSV is in wide format with the first column `string_id` and subsequent columns representing different language locales (e.g., `en`, `es`, `fr`). 
   Use Python (e.g., `pandas`) to melt this wide-format data into a long-format CSV saved at `/home/user/workspace/translations_long.csv`. 
   The long-format CSV must have exactly three columns in this order: `string_id`, `locale`, and `value`. It should not include an index column.

3. **Template-Based Text Generation**:
   A Jinja2 template is provided at `/home/user/workspace/strings.xml.j2`. 
   Extend your Python script (`process.py`) to read the long-format data and generate an XML file for each locale using the Jinja2 template.
   For each locale found in the CSV (e.g., `en`, `es`, `fr`), create a directory structure like `/home/user/workspace/output/values-<locale>/` and write the generated XML to `/home/user/workspace/output/values-<locale>/strings.xml`.

For example, the English translations should be written to `/home/user/workspace/output/values-en/strings.xml`.

Ensure your script runs successfully and all dependencies (like `pandas` and `Jinja2`) are installed in your environment before execution. You can use standard bash commands and pip to set up your environment.