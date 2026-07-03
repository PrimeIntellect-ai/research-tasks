I need you to help me fix a regression in a data processing pipeline. We process geospatial coordinate logs, but a recent update broke our parser. We have a vendored package called `geoparse` located at `/app/geoparse` which contains the latest code, but it's failing on edge cases. 

I've also provided a local git repository at `/home/user/geoparse-repo` that contains the last 200 commits of the parser's history. Somewhere in those 200 commits, a regression was introduced. 

The original parser correctly handled:
1. Standard geographic coordinates (e.g., `45.123456789, -122.987654321`) retaining high precision.
2. Slightly corrupted logs containing stray trailing whitespace or missing decimal leading zeros (e.g., `  -.987  `).

The current buggy version in `/app/geoparse` truncates floating-point precision prematurely (using `round(x, 4)`) and crashes with a `ValueError` on corrupted logs containing stray tabs or missing leading zeros.

Your task is to:
1. Identify the commit in `/home/user/geoparse-repo` that introduced the precision truncation and the crash on corrupted logs.
2. Fix the logic in the vendored package at `/app/geoparse`.
3. Create a final, standalone script at `/home/user/fixed_parser.py` that takes a single string argument (the coordinate string) and prints the parsed floating-point tuple `(lat, lon)` with full original precision (up to 9 decimal places) and robust whitespace/format handling. If the input is completely invalid (not two comma-separated numbers), print `INVALID`.

The final script will be tested against thousands of randomly generated coordinate pairs, including malformed ones.