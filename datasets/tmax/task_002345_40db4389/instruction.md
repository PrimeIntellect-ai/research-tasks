You are managing the configuration deployment pipeline for a fleet of servers. Before applying configuration changes, we must validate the historical drift metrics using a specific mathematical policy.

Your task is to create a filter in C that classifies configuration drift logs based on a policy dictated in an audio recording.

1. **Extract the Policy**:
   An audio file is located at `/app/policy.wav`. It contains a spoken policy defining a numerical threshold. Determine this threshold. You may use any tools available to you to extract the spoken text.

2. **Create the Sanitiser Program**:
   Write a C program at `/home/user/sanitiser.c` and compile it to `/home/user/sanitiser`.
   The program must accept a single command-line argument: the path to a CSV file.
   
   The CSV files contain configuration drift metrics with the format:
   `timestamp,metric_value` (both are numeric, `metric_value` is a float). The file has no header.

3. **Validation Logic**:
   Your program must read the CSV sequentially and compute a rolling average of `metric_value` over a window size of **3**. 
   - For the 1st row, the window size is 1 (just the current value).
   - For the 2nd row, the window size is 2 (the current and previous value).
   - For the 3rd row and beyond, the window size is 3 (the current and the two previous values).
   
   For each row, calculate the absolute difference between the current `metric_value` and the rolling average for that row.
   
   - If this absolute difference is **strictly greater** than the threshold extracted from the audio file at any point, the program must reject the file by exiting with status code `1`.
   - If the file is fully processed and no difference exceeds the threshold, the program must accept the file by exiting with status code `0`.

You are provided with a corpus of configuration logs in `/app/corpus/clean/` (which your program must accept) and `/app/corpus/evil/` (which your program must reject). Ensure your program correctly classifies these examples.