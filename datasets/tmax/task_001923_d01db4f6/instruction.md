You are acting as a localization engineer. We have a set of untranslated UI strings and a large translation memory (TM) file. We need to find the closest fuzzy match for each untranslated string using a C program.

Your task is to write a C program `/home/user/fuzzy_updater.c` and compile it to `/home/user/fuzzy_updater`.

The program must do the following:
1. Open and parse `/home/user/untranslated.txt`. Each line contains a localization key and an English string in the format: `KEY="English String"`.
2. Use POSIX regular expressions (`<regex.h>`) to extract the `KEY` and the `English String`. Skip any lines that do not strictly match this format.
3. For each valid extracted string, stream through the translation memory file `/home/user/tm.tsv`. The TM file is large, so you must read it line-by-line (do not load the whole file into memory).
4. Each line in `tm.tsv` is tab-separated: `English_TM\tSpanish_TM`.
5. Compute the Levenshtein distance (case-sensitive) between the extracted `English String` and the `English_TM` from the file. 
6. Find the Spanish translation with the lowest Levenshtein distance for each key. If there's a tie, keep the first one encountered.
7. Output the merged results to `/home/user/updated_translations.tsv`.

The output file `/home/user/updated_translations.tsv` must be tab-separated and formatted exactly like this for each valid key:
`KEY\tOriginal_English\tBest_Match_Spanish\tDistance`

Example output line:
`ERR_NO_FILE\tFile not found\tEl archivo no se encuentra\t2`

Constraints:
- Use standard C libraries (`stdio.h`, `string.h`, `stdlib.h`, `regex.h`).
- Do not use external libraries (e.g., PCRE or glib) other than standard libc.
- Compile your code using `gcc /home/user/fuzzy_updater.c -o /home/user/fuzzy_updater`.
- Run your program to generate `/home/user/updated_translations.tsv`.