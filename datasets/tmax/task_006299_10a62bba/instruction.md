I am a technical writer trying to organize some legacy documentation drafts. The drafts were exported by an old internal system into a custom compressed binary file, and I need you to extract the public documentation, format it as JSON, and then re-compress it using the same custom format for archival.

Here is the exact workflow I need you to perform:

**1. Decompress the Archive**
There is a custom compressed binary archive at `/home/user/doc_dumps/archive.rle`. 
It uses a custom Run-Length Encoding (RLE). The file consists of 2-byte pairs:
- The first byte (unsigned 8-bit integer) represents the `count` (how many times the character repeats).
- The second byte represents the ASCII `character`.
For example, the bytes `0x03 0x41` represent the string "AAA".
Write a Python script to decompress this file into a text string.

**2. Parse the Multi-line Logs**
The decompressed text contains multi-line documentation records separated by exact markers. The format is exactly:
```
===DOC-START===
Author: <author_name>
Date: <YYYY-MM-DD>
Tags: <tag1, tag2, ...>

<multi-line content>
===DOC-END===
```
Parse these records. Note that `<multi-line content>` may contain blank lines and spans multiple lines until `===DOC-END===`.

**3. Filter and Convert**
I only want the records that include the tag `public` (case-insensitive, ignoring leading/trailing whitespace around tags). 
Format the filtered records into a single JSON array of objects, like this:
```json
[
  {
    "author": "Alice",
    "date": "2023-10-01",
    "tags": ["public", "api"],
    "content": "This is the API documentation.\nIt spans multiple lines."
  }
]
```
Ensure the tags array contains cleanly stripped lowercase strings. The `content` must preserve the exact line breaks from the original text (excluding the empty line immediately following the `Tags:` line and the newline immediately preceding `===DOC-END===`). Save this JSON to `/home/user/public_docs.json` (formatted with an indentation of 2 spaces).

**4. Re-compress**
Take the exact JSON string generated in step 3 and compress it using the same custom RLE format described in step 1. For simplicity during encoding, simply write `count=1` for every character (e.g., "AB" becomes `0x01 'A' 0x01 'B'`), unless you prefer to optimize identical contiguous characters up to a count of 255.
Save this new binary file to `/home/user/public_docs.rle`.

Please use Python to complete these tasks.