You are a localization engineer tasked with building a tool to match new, untranslated strings against an existing Translation Memory (TM) to find the best fuzzy matches and track translation confidence over time. 

You must implement a mini-pipeline using **Make** and **Go** in the `/home/user` directory.

Here is your setup:
1. A translation memory file at `/home/user/tm.json` containing known translations.
2. A list of new strings to translate at `/home/user/new_strings.txt`.

**Pipeline Requirements**:
You must create a `Makefile` with a default `all` target that orchestrates the following pipeline:

**Stage 1: Cleaning (Shell/Make)**
The `Makefile` should read `/home/user/new_strings.txt` and produce `/home/user/cleaned.txt`.
The cleaning rules are:
- Convert all characters to lowercase.
- Remove leading and trailing whitespace.
- Collapse multiple consecutive spaces inside the string into a single space.
- Deduplicate the strings while **preserving the original order of their first appearance**.

**Stage 2: Fuzzy Matching and Rolling Statistics (Go)**
Create a Go program (e.g., `matcher.go`) that Make compiles and runs. It should read `cleaned.txt` and `tm.json`.
For every string in `cleaned.txt` (in order), the Go program must:
1. Find the best match in `tm.json` by computing the **Levenshtein distance** between the cleaned string and the `source` strings in the TM. If there's a tie for the minimum distance, choose the one that appears *first* in `tm.json`.
2. Compute a **rolling average** of these minimum Levenshtein distances using a window size of **3**. (For the first string, the average is just its distance; for the second, the average of the first two; from the third onwards, the average of the current and two previous distances).

**Output format**:
The Go program should output a CSV file to `/home/user/localization_report.csv` with exactly this header:
`CleanedSource,BestMatchTarget,Distance,RollingAvg`

- `CleanedSource`: The cleaned string.
- `BestMatchTarget`: The `target` value of the best matching TM entry.
- `Distance`: The integer Levenshtein distance.
- `RollingAvg`: The rolling average of the distance, formatted to exactly two decimal places (e.g., `0.00`, `0.33`, `2.00`).

Build the complete orchestration so that just typing `make` in `/home/user` runs the entire pipeline and generates the final CSV.