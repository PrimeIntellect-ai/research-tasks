As a site administrator, you need to automate the onboarding of new users from a scanned registration matrix. You have received an image file located at `/app/user_matrix.png` which contains a printed table of users with three columns: `USER_ID`, `DEPT`, and `LEVEL` (separated by spaces or tabs). 

Your task is to:
1. Extract the text from the image `/app/user_matrix.png`. (The `tesseract` OCR tool is installed on the system).
2. Use shell text processing tools (awk, sed, grep) to clean up the OCR output and remove any headers or garbage lines. Only lines containing a numeric `USER_ID` should be processed.
3. Write a C program named `generate_config.c` in `/home/user/` that reads the cleaned text data. For each user row, the C program must compute and generate two specific configuration strings and output them to `/home/user/final_config.txt`.

For each user, the C program should write:
- An email alias configuration line: `alias: user<USER_ID>@<DEPT>.domain.com` (Note: the `<DEPT>` must be converted to strictly lowercase).
- A network routing configuration line: `route: 10.<LEVEL>.0.<USER_ID>`

The output file `/home/user/final_config.txt` must have exactly these two lines per user, in that order, for every user successfully parsed. 

Your C program must be compiled to an executable named `/home/user/generate_config` and run to produce the output file. A grading script will compare your `/home/user/final_config.txt` against the ground truth data originally encoded in the image. You must achieve a high accuracy score to pass.