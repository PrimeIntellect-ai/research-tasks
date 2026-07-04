You are a support engineer investigating a crash in our Go-based mathematical processing service. The service calculates complex operations but recently crashed when receiving a specific request. We managed to capture the network traffic during the incident.

Your task is to collect diagnostics by completing the following steps:

1. Analyze the packet capture file located at `/home/user/capture.pcap`. Find the payload of the single TCP packet destined for port `9000`. 
2. Extract the raw ASCII payload of this packet and save it exactly as is to `/home/user/crash_input.txt`.
3. Create a minimal reproducible example (MRE) in Go to demonstrate the failure. Write a Go program at `/home/user/mre.go` that:
   - Reads the contents of `/home/user/crash_input.txt`.
   - Attempts to unmarshal the payload into the following struct using the standard `encoding/json` package:
     ```go
     type MathRequest struct {
         Operation string   `json:"op"`
         Arguments []uint64 `json:"args"`
     }
     ```
   - Prints *only* the resulting error message from the unmarshal attempt to standard output (do not print anything if it succeeds, but we know it will fail because the input is corrupted).
4. Run your `mre.go` program and redirect its output to `/home/user/diagnostic.log`.

Make sure all files are placed exactly where specified in the `/home/user` directory.