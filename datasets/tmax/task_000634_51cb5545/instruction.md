You are an incident responder investigating a series of obfuscated web attacks. You have an offline investigation environment with a vendored Go package located at `/app/vendor/urlesc` (the source for `github.com/PuerkitoBio/urlesc`). This package is supposed to handle the unescaping of malicious URLs extracted from our security logs. 

However, we suspect an insider or attacker previously tampered with this vendored code on our server. Specifically, the unescaping logic is failing to decode the `+` character into a space character (` `), which is causing our automated payload analysis to miss critical XSS vectors.

Your task consists of two parts:

1. **Fix the Vendored Package:**
   Inspect the source code of the vendored package at `/app/vendor/urlesc/urlesc.go`. Identify the perturbation where the conversion of `+` to a space was disabled or removed, and fix it so that it correctly decodes `+` to a space character.

2. **Develop the Payload Extractor:**
   Write a Go program at `/home/user/investigate.go`. Your program must do the following:
   - Read a single URL-encoded string from standard input (stdin) until EOF.
   - Use the fixed package (`github.com/PuerkitoBio/urlesc`) to unescape the entire input string.
   - Treat the resulting unescaped string as an HTTP query string (e.g., `id=123&payload=<script>alert(1)</script>&token=abc`).
   - Parse this query string and extract the exact value of the `payload` parameter.
   - Print EXACTLY the value of the `payload` parameter to stdout (using `fmt.Print`, with no trailing newline). 
   - If the `payload` parameter is missing, or if any error occurs during unescaping or parsing, print EXACTLY the string `ERROR` to stdout.

You must compile your program to an executable named `/home/user/investigate`. 
*(Hint: You will likely need to initialize a Go module in `/home/user` and use the `replace` directive in your `go.mod` to point `github.com/PuerkitoBio/urlesc` to the local `/app/vendor/urlesc` path.)*

An automated fuzzing suite will test your compiled `/home/user/investigate` binary by piping thousands of randomly generated, obfuscated query strings into its stdin. Your binary's output must be bit-for-bit identical to our trusted incident response oracle binary.