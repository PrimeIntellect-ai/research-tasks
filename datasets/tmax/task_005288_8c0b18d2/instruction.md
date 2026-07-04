You are stepping into the role of a storage administrator. To save disk space, our organization previously archived thousands of old Write-Ahead Logs (WAL) and GCode manufacturing files using a proprietary in-house tool. Unfortunately, the developer left, and we only have the stripped binary left: `/app/fast-extractor`. 

Recently, we discovered that `/app/fast-extractor` has severe vulnerabilities: it does not validate file paths during extraction, making it susceptible to directory traversal attacks (e.g., writing to `/etc` or using `../`), and it crashes when parsing malformed UTF-16 configuration headers. 

Before we process the remaining historical archives on our production storage array, we need a reliable way to filter out corrupted or malicious archives. 

Your task is to write a standalone detection program. 
1. Analyze the `/app/fast-extractor` binary (or reverse-engineer the archive format) to understand how it parses the custom archive format. 
2. Write an executable script or compiled program located at `/home/user/detector`. 
3. Your detector must take exactly one argument (the path to an archive file) and analyze it. 
4. If the archive is completely safe to extract, your detector must exit with status code `0`. 
5. If the archive contains path traversal payloads (e.g., filenames starting with `/`, containing `../` or `..\`), malformed config headers, or structural anomalies that would crash the extractor, it must exit with status code `1` (or any non-zero value).

You may write the detector in any language you prefer. Ensure `/home/user/detector` is marked as executable. You have a stripped binary to analyze, and you should ensure your detector handles character encoding conversions accurately, as the archive headers use a specific encoding.