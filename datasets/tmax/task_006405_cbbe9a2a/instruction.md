You are a localization engineer tasked with preparing a translation file for a European market while ensuring GDPR compliance by masking sensitive data. 

You need to write a C++ program that reads an English localization CSV file, processes the text using regex and mathematical transformations, and generates an XML file.

**Input File:**
`/home/user/locales/en_US.csv`
This file is a CSV with three columns: `key`, `text`, and `comment`. It contains a header row.

**Your C++ program must perform the following operations for each row (excluding the header):**

1. **Data Masking (Regex):** 
   In the `comment` column, find any email addresses and anonymize them by replacing the entire local part (everything before the `@`) with `***`. 
   For example, `john.doe@example.com` becomes `***@example.com`.

2. **Mathematical Transformation & Localization (Regex):**
   In the `text` column, find any US currency amounts formatted as `$X.XX` or `$X` (e.g., `$150.00` or `$5`).
   Extract the numeric value, multiply it by exactly `0.85` (the conversion rate to Euros), and round to 2 decimal places using standard half-up rounding.
   Replace the original dollar string with the new Euro amount appended with the `€` symbol. 
   For example, `$100.00` should become `85.00€`. `$1.50` (1.50 * 0.85 = 1.275) should become `1.28€`.

3. **Template-based Generation:**
   Output the processed rows into a new XML file located at `/home/user/locales/es_ES.xml`.
   The file must have `<locale>` as its root element, and each row should be formatted exactly like this:
   `  <string id="KEY" notes="MASKED_COMMENT">TRANSLATED_TEXT</string>`
   *(Note the two spaces of indentation for each string element).*

**Requirements:**
- Save your C++ source code to `/home/user/process.cpp`.
- Compile it to an executable at `/home/user/process` (e.g., using `g++ -std=c++17 /home/user/process.cpp -o /home/user/process`).
- Run your executable to generate the required `/home/user/locales/es_ES.xml` file.