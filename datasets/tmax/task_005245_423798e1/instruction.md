You are a localization engineer tasked with building a high-performance translation API for a monitoring dashboard.

We have an internal, proprietary translation engine provided as a compiled binary at `/app/loc_translator`. This binary is stripped of debugging symbols and takes two arguments: the target locale and a base64-encoded English string. It prints the translated string to stdout.
Example usage: `/app/loc_translator "fr-FR" "V2VsY29tZQ=="` (base64 for "Welcome").

Your task is to write a Go application that starts an HTTP server on `127.0.0.1:9090`. 
The server must expose a single endpoint: `POST /localize`.

The endpoint will receive a JSON payload representing sparse events in a time-series, for example:
```json
{
  "locale": "es-ES",
  "start_time": 1700000000,
  "end_time": 1700000030,
  "interval": 10,
  "events": {
    "1700000000": "Welcome",
    "1700000020": "Warning"
  }
}
```

Requirements for the `/localize` endpoint:
1. **Constraint Validation:** The server must validate that the `locale` is either `es-ES` or `fr-FR`. If any other locale is provided, return an HTTP 400 Bad Request status code.
2. **Resampling and Gap-filling:** Generate a continuous timeline of timestamps from `start_time` to `end_time` (inclusive), incrementing by `interval` seconds. If a timestamp exists in `events`, use the associated string. If a timestamp is missing, fill the gap with the default string: `"Idle"`.
3. **Parallel Processing:** You must invoke the `/app/loc_translator` binary to translate the English strings for the timeline. Because the binary can be slow, you must perform these translations in parallel using Go routines.
4. **Template-based Generation:** The HTTP response body must be plain text (Content-Type: text/plain), generated using Go's `text/template` package. The format for each timestamp must exactly match:
`[{{.Timestamp}}] {{.TranslatedText}}`
Ensure the output lines are ordered chronologically.

Write your Go code, save it to `/home/user/server.go`, and start the server in the background so it is ready to accept requests.