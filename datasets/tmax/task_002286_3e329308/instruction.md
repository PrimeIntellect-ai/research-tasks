You are a data analyst tasked with processing customer support logs. An automated phone system has saved a recent escalated customer voicemail to `/app/call_audio.wav`. 

You need to extract the customer's ID from this voicemail and then run a data analysis pipeline over our historical CSV logs to summarize this customer's past interactions.

**Step 1: Transcription**
Use the pre-installed transcription tool to transcribe the audio file.
* Tool path: `/opt/whisper/main`
* Model path: `/opt/whisper/models/ggml-base.en.bin`
The voicemail contains a phrase like "My customer ID is [5-digit-number]". Identify this number.

**Step 2: Query Construction & Optimization (Go)**
We have two large datasets:
* `/app/data/tickets.csv` (columns: `ticket_id`, `customer_id`, `agent_id`, `duration_mins`)
* `/app/data/agents.csv` (columns: `agent_id`, `department`, `rating`)

There is a naive Go script at `/home/user/analyze.go` that joins these files to find the total ticket duration and average agent rating per department for a specific customer. However, the current implementation uses nested loops (O(N^2) complexity) and takes far too long to run.

Your task is to rewrite `/home/user/analyze.go` so that it:
1. Accepts the 5-digit customer ID (extracted from the audio) as its first command-line argument.
2. Uses an efficient O(N) Hash Join approach (using Go maps) to process the CSV files.
3. Computes the same aggregation: group by `department`, calculate the sum of `duration_mins` and the average of `rating` for the agents who handled this customer's tickets.
4. Outputs the final aggregated data as a JSON file to `/home/user/result.json` in this exact format:
```json
{
  "customer_id": "12345",
  "departments": {
    "Billing": {
      "total_duration": 145,
      "avg_rating": 4.2
    }
  }
}
```

**Step 3: Build and Execute**
Compile your optimized Go program to `/home/user/analyzer`. Run it with the transcribed customer ID to generate `/home/user/result.json`.

*Note: Your rewritten Go program will be evaluated on its execution speed. You must achieve a speedup of at least 10x compared to the naive implementation.*