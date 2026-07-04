You are an MLOps engineer tasked with implementing a new automated model evaluation pipeline. 

The lead researcher has dictated the specification for a custom evaluation metric, referred to as the "Demographic Risk Metric", in an audio memo. This audio file is located at `/app/metric_dictation.wav`.

Your task:
1. Setup whatever tools you need to transcribe the audio file and extract the exact business logic and mathematical formula for the Demographic Risk Metric.
2. Implement this metric as a command-line tool written in Go.
3. The Go program must be compiled into a standalone executable located exactly at `/home/user/evaluator`.
4. The executable must accept exactly three command-line arguments in this specific order:
   - Argument 1: `predictions` (a comma-separated list of floating-point numbers)
   - Argument 2: `ground_truths` (a comma-separated list of floating-point numbers)
   - Argument 3: `ages` (a comma-separated list of integers)
   You can assume all three comma-separated lists will always contain the exact same number of elements (between 1 and 1000).
5. The program must output *only* the final computed metric to standard output, formatted exactly as requested in the audio dictation. Do not include any extra text, logging, or whitespace.

Requirements:
- Your solution must be written in Go. 
- You should handle basic parsing of the comma-separated strings.
- The output must rigorously follow the mathematical rules and rounding requirements laid out in the audio recording.