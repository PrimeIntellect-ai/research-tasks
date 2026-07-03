You are an AI assistant acting as a localization engineer. You need to process a batch of translation updates. The system generated a buggy JSON-Lines file, and you must clean it, impute missing metrics using mathematical distance, and output a structured XML file.

Here is the situation:
You have two input files in `/home/user/`:
1. `translations.jsonl`: Contains incoming translation updates. However, the system that produced it had a bug: it double-escaped unicode characters (e.g., it wrote literal `\\u00e9` instead of the single backslash `\u00e9` or the character `é`), making some lines fail standard parsing or display incorrectly. It also contains duplicate entries for the same `id`, and is missing the `confidence` score for several translations.
2. `tm.csv`: A trusted Translation Memory file containing `source` and `target` columns.

Your objectives:
1. **Clean and Normalize:** Read `translations.jsonl`. Use a regular expression to find and properly decode the double-escaped unicode sequences into their actual characters (e.g., `\\u00e9` becomes `é`). 
2. **Deduplicate:** If multiple entries share the same `id`, keep only the last one appearing in the file.
3. **Impute Missing Confidences:** For any deduplicated entry missing a `confidence` score (or where it is `null`), you must compute a score using the Normalized Levenshtein Similarity against the sources in `tm.csv`.
   - Compare the cleaned `source` text of the translation entry against all `source` texts in `tm.csv`.
   - Find the minimum Levenshtein distance ($D$).
   - Compute similarity as: $Similarity = 1 - \frac{D}{\max(|S_{trans}|, |S_{tm}|)}$
     where $|S_{trans}|$ is the string length of the translation source, and $|S_{tm}|$ is the length of the matched TM source.
   - Set the `confidence` to the maximum similarity found, rounded to 3 decimal places.
4. **Output to XML:** Write the cleaned, imputed, and deduplicated data to `/home/user/updated_translations.xml`.

The XML must exactly follow this format, sorted by `id` (as integers):
```xml
<translations>
  <translation id="1" confidence="0.990">
    <source>Hello world</source>
    <target>Bonjour le monde</target>
  </translation>
  ...
</translations>
```
Make sure all strings are properly XML-escaped. Write a Python script to accomplish this pipeline, install any packages you need, and execute it to generate the final XML file.