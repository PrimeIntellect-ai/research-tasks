You are a Site Reliability Engineer (SRE). A custom uptime monitoring service (`/home/user/uptime_monitor`) has crashed unexpectedly, generating a core dump. The source code for this binary has been lost, and the binary was compiled without DWARF debug information (though basic symbols remain).

We suspect the crash was caused by a floating-point precision loss issue that resulted in a fatal arithmetic exception (e.g., division by zero). Before the crash, the program loaded a secret authentication token into heap memory.

Your task is to analyze the binary and the core dump using standard Linux command-line tools to determine the exact circumstances of the crash. 

Please investigate and create a report file at `/home/user/incident_report.txt` containing exactly the following three lines in this precise format:

```text
SECRET_TOKEN=<the extracted secret string from the core dump>
CRASH_UPTIME=<the integer representation of the float uptime value at the exact moment of the crash>
CRASH_FUNC=<the name of the function where the crash occurred>
```

**Constraints and details:**
* The core dump is located at `/home/user/core`.
* The binary is located at `/home/user/uptime_monitor`.
* The secret token begins with `SRE_MONITOR_SECRET_`.
* The `CRASH_UPTIME` should be the whole number value (no decimals) of the `float` variable that lost precision, triggering the arithmetic exception. You will need to inspect registers or the stack in the core dump, and understand single-precision IEEE 754 limits.
* Do not use any external scripts; use standard tools like `gdb`, `strings`, `objdump`, etc.