You are a data engineer tasked with building a robust ETL pipeline component in C++ to process network telemetry data.

We receive incremental telemetry batches representing network edges. You need to write a C++ program that acts as a data sanitiser and filter.

First, there is a voicemail from the lead architect left at `/app/voicemail.wav`. You will need to transcribe or listen to this audio file (you may use Python's `SpeechRecognition` or `pydub`, or any available transcription tools in the environment) to understand the reverse-engineered data model and the specific anomaly detection rules. The audio contains critical information regarding which fields represent the true source and destination nodes, what window functions to apply, and how to identify anomalous graph updates.

Second, you must implement the sanitiser in C++ (`/home/user/sanitiser.cpp`). This program must take a single command-line argument: the path to a CSV file containing a batch of network edges.
The program must:
1. Parse the CSV file.
2. Materialize the graph projection (you may embed SQLite via `<sqlite3.h>` or build in-memory data structures).
3. Implement the necessary index strategy if using a DB to ensure fast analytical aggregations.
4. Compute the window functions and/or graph shortest paths as specified in the voicemail to determine if the batch is "clean" or "anomalous".
5. Return an exit code of `0` if the batch is clean (should be accepted), and an exit code of `1` if the batch is anomalous (should be rejected).

To test your implementation, we have provided two corpora of CSV payloads:
- `/app/corpora/clean/`: Contains 50 valid telemetry batches. Your program MUST accept all of these (exit 0).
- `/app/corpora/evil/`: Contains 50 anomalous telemetry batches. Your program MUST reject all of these (exit 1).

You must compile your program to `/home/user/sanitiser`. Make sure you test it against both corpora to ensure 100% accuracy. The automated verification will run your binary against a hidden set of clean and evil files generated with the exact same rules.