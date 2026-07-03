You are a localization engineer managing a time-series translation database for a global application. Your goal is to process an incoming stream of translation logs, reshape them, and deploy an internal API to query localized timelines.

We have pre-vendored a third-party package, `github.com/dustin/go-humanize`, at `/app/go-humanize`. However, an upstream commit introduced a deliberate bug into the package that prevents it from compiling correctly.

Your objectives:

1. **Fix the Vendored Package**: 
   Navigate to `/app/go-humanize` and identify the perturbation. A recent patch to `times.go` or `go.mod` broke the build (a deliberate syntax error or missing directive). Fix it so the package compiles.

2. **Data Cleaning and Reshaping**:
   You have a raw dataset at `/home/user/data/loc_events.csv`. It is in a "long" format with columns: `timestamp, event_id, lang_code, raw_text, translated_text`.
   - Clean the text: Normalize all `translated_text` to Unicode NFC. Deduplicate rows keeping the latest `timestamp` for any `(event_id, lang_code)` combination.
   - Reshape the data into a "wide" format TSV: `timestamp, event_id, en, es, fr, zh`. Fill missing translations with the string `"MISSING"`.
   - Sort the resulting rows chronologically by `timestamp`, then alphabetically by `event_id`.
   - Save this file to `/home/user/processed/wide_events.tsv`.

3. **Template-Based Server Generation**:
   Write a Go HTTP server in `/home/user/server/main.go` that imports your fixed `/app/go-humanize` module and reads the `wide_events.tsv` file into memory.
   - The server must listen on `127.0.0.1:8080`.
   - It must implement an endpoint `GET /timeline?event_id=<id>&lang=<lang_code>`.
   - Require an exact Authorization header: `Authorization: Bearer loc-eng-token`.
   - On a valid request, it should return a plain-text localized response generated using Go's `text/template`. The template should say (in English, for example):
     `Event <event_id> occurred at <timestamp>. Translation: <translated_text>. This was <humanized_time> ago.`
     Use `go-humanize` to generate the relative `<humanized_time>` (e.g., "3 days ago") using the current system time as the baseline. 
   - If the translation is missing or language isn't found, return HTTP 404.

Start the server in the background so it is actively listening on `127.0.0.1:8080` when you conclude your task.