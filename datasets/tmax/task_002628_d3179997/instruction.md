You are a DevOps engineer troubleshooting a brittle log ingestion pipeline. A custom C utility used to parse formatted logs, `log_processor`, has been crashing intermittently. 

Here is the source code for the utility, located at `/home/user/log_processor.c`:

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void parse_log_line(char *line) {
    // Expected format: TIMESTAMP|SEVERITY|MESSAGE
    char *delim1 = strchr(line, '|');
    if (!delim1) return;
    *delim1 = '\0';
    
    char *delim2 = strchr(delim1 + 1, '|');
    if (!delim2) return;
    *delim2 = '\0';
    
    char *timestamp = line;
    char *severity = delim1 + 1;
    char *message = delim2 + 1;
    
    // Strip trailing newline from message
    int len = strlen(message);
    if (len > 0 && message[len-1] == '\n') {
        message[len-1] = '\0';
        len--;
    }
    
    // Check for line continuation escape character at the end of the message
    if (message[len-1] == '\\') {
        printf("CONTINUATION: %s\n", timestamp);
    } else {
        printf("PROCESSED: [%s] %s\n", severity, message);
    }
}

int main() {
    char buffer[512];
    while (fgets(buffer, sizeof(buffer), stdin)) {
        parse_log_line(buffer);
    }
    return 0;
}
```

The system takes standard input and processes it line by line. Most logs pass perfectly, but occasionally the pipeline halts due to a segmentation fault when an edge-case formatted log line is received. 

Your tasks are:
1. Identify the edge-case vulnerability in the C code that causes the intermittent segmentation fault / memory violation.
2. Create a minimal reproducible input string that triggers this crash reliably, and save it to a file exactly at `/home/user/crash_input.txt`. The file should contain exactly one line of input.
3. Fix the logic in the C code to handle this edge case gracefully without crashing. Save the repaired source code to `/home/user/fixed_processor.c`.
4. Compile your fixed code into an executable located at `/home/user/fixed_processor`. It must process valid logs exactly as before, but simply ignore or safely process the edge-case line without crashing.

You do not need root access. You may use `gcc`, `gdb`, and standard bash utilities.