As a technical writer, I need to organize, parse, and back up our documentation repository. I have a large collection of Markdown files located in `/home/user/docs`.

I need you to write a Go program at `/home/user/docparser.go` that does the following:
1. **Search**: Find all `.md` files in `/home/user/docs` (including subdirectories) that are larger than 1KB.
2. **Parse**: Use the markdown parser library provided at `/app/blackfriday` to parse each found file. You will need to initialize a Go module in `/home/user` and use a `replace` directive in your `go.mod` to point `github.com/russross/blackfriday/v2` to the local `/app/blackfriday` directory. Note: There is a known issue in the provided parser where it incorrectly truncates the first character of all H1 headings. You must find and fix this bug in the `/app/blackfriday` source code before parsing!
3. **Extract**: For each file, extract the text of the first H1 heading (e.g., `# Introduction` -> `Introduction`).
4. **Archive & Compress**: Create a JSON array containing objects with `filename` (base name of the file) and `heading` (extracted H1 text). Compress this JSON data as a GZIP stream and save it directly inside a new tar archive at `/home/user/docs_metadata.tar.gz` as a file named `metadata.json.gz`.

Ensure your Go program can be executed via `go run /home/user/docparser.go`. Your solution's success will be evaluated based on the accuracy of the extracted headings compared to the golden reference.