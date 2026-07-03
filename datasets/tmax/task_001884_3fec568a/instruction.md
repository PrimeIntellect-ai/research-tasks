You need to implement a configuration sanitiser and converter in Go. 

We have a system that receives binary configuration files, but some of them have been corrupted or contain blacklisted signatures. You need to write a Go program `/home/user/filter.go` that processes a directory of binary config files, filters out the bad ones, and safely converts the good ones to JSON.

1. Review the image at `/app/schema.png`. It contains the specification for the binary format, including the required magic bytes at the beginning of a valid file, and the blacklist signature that indicates an "evil" configuration. You will need to use an OCR tool (like `tesseract`) to read the image.
2. Your Go program must be executable via: `go run /home/user/filter.go <input_dir> <output_dir>`.
3. For each file in `<input_dir>`, your program must:
   - Check if the file starts with the valid magic bytes specified in the image. If not, reject it.
   - Check if the file contains the evil signature anywhere in its contents. If it does, reject it.
   - If it passes both checks, extract the payload (everything after the magic bytes).
   - Convert the payload (which is valid UTF-8 text) into a JSON object: `{"config_data": "<payload_text>"}`.
   - Atomically write the resulting JSON to `<output_dir>/<original_filename>.json` (hint: write to a temporary file first, then use a bulk file renaming or atomic move operation).

Your solution will be tested against a hidden corpus of clean and evil files. A perfect pass requires 100% of clean files to be successfully converted and written to the output directory, and 100% of evil files to be rejected (no output file created).