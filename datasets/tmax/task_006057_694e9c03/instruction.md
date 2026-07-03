As a storage administrator, you need to monitor disk space usage based on a custom file system's Write-Ahead Log (WAL) and compare it against user quotas.

You are provided with two files in `/home/user/`:
1. `quotas.csv`: A comma-separated values file containing user storage quotas. Each line has the format `user_id,quota_bytes` (both are integers).
2. `allocations.wal`: A binary Write-Ahead Log tracking disk space allocations and deallocations. The file consists of a continuous sequence of 16-byte records. Each record is structured as follows (all in Little-Endian byte order):
   - Bytes 0-7: `timestamp` (unsigned 64-bit integer)
   - Bytes 8-11: `user_id` (unsigned 32-bit integer)
   - Bytes 12-15: `delta_bytes` (signed 32-bit integer, representing bytes allocated if positive, or freed if negative)

Your task is to write a C program that calculates the current total storage used by each user (starting from 0) by processing all records in `allocations.wal`. The program should then compare each user's total usage against their quota defined in `quotas.csv`.

For any user whose total usage strictly exceeds their quota, output a violation record to an XML file at `/home/user/violations.xml`. 

The XML file must exactly match this format, with violations sorted by `user_id` in ascending order:
```xml
<violations>
    <violation user_id="101" used="1050" quota="1000"/>
    <violation user_id="103" used="600" quota="500"/>
</violations>
```

Requirements:
- Write your C program in `/home/user/check_quotas.c`
- Compile it to `/home/user/check_quotas` (using GCC or Clang)
- Run it to generate `/home/user/violations.xml`
- You may use standard C library headers. No external libraries are required.