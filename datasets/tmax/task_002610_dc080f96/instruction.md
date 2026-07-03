You are a data engineer building an ETL pipeline. We have a stream of JSON-lines event data, but our previous parser kept breaking on invalid unicode escape sequences injected by a rogue upstream system. 

The product manager left a voice memo detailing the exact aggregation rules and the required output template for our new Go-based pipeline. The audio file is located at `/app/requirements.wav`.

Write a Go program at `/home/user/processor.go` that reads a stream of JSON-lines from standard input and writes the aggregated results to standard output. 

The input JSON lines represent financial events and have the following schema:
`{"timestamp": "2023-05-10T14:12:33Z", "type": "sale", "amount": 25.50}`
`{"timestamp": "2023-05-10T14:18:00Z", "type": "refund", "amount": 5.00}`

Your program must:
1. Stream process standard input line by line to handle arbitrarily large files.
2. Group the events into time buckets based on the `timestamp` field. The exact bucket size and logic are dictated in the audio file. The bucket timestamp used for grouping must be the start time of the bucket.
3. Calculate the net revenue for each bucket (total `sale` amounts minus total `refund` amounts).
4. Output the results sorted by the bucket timestamp in chronological order, using the exact text template dictated in the audio.
5. Robustly handle invalid JSON lines (such as those containing broken unicode escapes like `\uZZZZ`) by silently dropping the malformed lines and continuing execution.

Your program should read until EOF, then print the aggregated, sorted results to standard output. Do not output any extra text. Make sure your Go code is self-contained in `/home/user/processor.go` and handles the requirements perfectly.