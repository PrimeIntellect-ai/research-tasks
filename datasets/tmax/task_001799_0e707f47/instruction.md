You are acting as a localization engineer. We have received some translated text files from different regional teams, but they did not use consistent text encodings. You need to build an automated pipeline to process these files, generate localized web pages from a template, and store metadata in a database.

Here is your workspace setup:
You will find the following source files in `/home/user/locales/`:
- `ja.txt` (Encoded in `Shift_JIS`)
- `de.txt` (Encoded in `ISO-8859-1`)
- `ru.txt` (Encoded in `KOI8-R`)

Each text file contains exactly two lines:
Line 1: The localized Title
Line 2: The localized Content

You also have a template file at `/home/user/template.html`:
```html
<html>
<head><meta charset="UTF-8"></head>
<body>
    <h1>{{TITLE}}</h1>
    <p>{{CONTENT}}</p>
</body>
</html>
```

Perform the following steps:

1. **Python Text Processing & Templating**: Write a Python script at `/home/user/process.py` that reads each of the three text files using their respective correct encodings. 
   - For each language (ja, de, ru), replace `{{TITLE}}` and `{{CONTENT}}` in the template with the text from the files.
   - Save the resulting generated HTML files as `/home/user/output/ja.html`, `/home/user/output/de.html`, and `/home/user/output/ru.html`. These output files MUST be encoded in `UTF-8`.
   - The script must also generate a CSV file at `/home/user/output/metadata.csv` with a header row `lang,title_length,content_length`. For each language, output the language code (ja, de, ru) and the number of Unicode characters (NOT bytes) in the Title and Content respectively.

2. **Database Bulk Import**: Create a shell script `/home/user/pipeline.sh` that first executes your Python script. Then, using the `sqlite3` command-line tool, it should bulk import `/home/user/output/metadata.csv` into a new SQLite database located at `/home/user/locales.db`. 
   - The data should be imported into a table named `metadata` with columns `lang TEXT`, `title_length INTEGER`, and `content_length INTEGER`. 
   - Make sure `/home/user/pipeline.sh` is executable.

3. **Pipeline Scheduling**: Create a crontab-formatted file at `/home/user/locales_cron` that schedules your `/home/user/pipeline.sh` script to run every day at exactly 2:00 AM.

Ensure that running `./pipeline.sh` successfully creates the HTML files, the CSV, and fully populates the database.