You are acting as a localization engineer. We are overhauling our translation pipeline. Previously, our naive CSV tools silently dropped rows containing embedded newlines or crashed on broken Unicode. 

We need you to build a robust C-based CSV filter and gap-filler.

**Step 1: Extract Fallback Mappings**
We lost the original configuration file for locale fallbacks. Fortunately, we have a screenshot of it at `/app/fallback_config.png`. 
1. Use `tesseract` (which is pre-installed) to extract the text from this image.
2. The image contains fallback rules in the format `SourceLocale -> TargetLocale` (e.g., `es-AR -> es-ES`).
3. Parse this extracted text into a structured file at `/home/user/fallbacks.csv` containing comma-separated `SourceLocale,TargetLocale` pairs.

**Step 2: Build the CSV Sanitizer**
Write a C program at `/home/user/loc_sanitizer.c` and compile it to `/home/user/loc_sanitizer`.

The program must have the following signature and behavior:
`./loc_sanitizer /home/user/fallbacks.csv < input.csv > output.csv`

Requirements:
1. **CSV Parsing:** It must correctly parse standard CSV files (comma delimited). Critically, it must support double-quoted fields that contain embedded newlines and commas. 
2. **UTF-8 Validation:** The pipeline receives text from unverified crowdsourced translators. You must validate the UTF-8 encoding of the translation string (the third column). If *any* column in a row contains invalid UTF-8 bytes, the program must **drop the entire row** (do not print it).
3. **Gap Filling (Joins):** The input CSV has three columns: `MessageID,Locale,Translation`. If the `Translation` column is completely empty, the program should look up the `Locale` in the `fallbacks.csv` data. If a fallback locale exists, it should append a comment `[FALLBACK_APPLIED]` to the empty translation field. (Assume we just want to mark it for the next stage).
4. **Output:** Valid rows must be printed to stdout in standard CSV format.

**Data Format Details:**
Input CSV headers: `MessageID,Locale,Translation`
Rows can span multiple lines if the `Translation` contains a newline inside quotes.

*Note:* You do not need to process the whole file in parallel, but your CSV parser must accurately maintain state across newlines.