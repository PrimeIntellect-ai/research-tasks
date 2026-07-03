You are an automation specialist tasked with building a high-throughput data anonymization service. We have a proprietary Go library for masking Personally Identifiable Information (PII) that was recently updated, but the source code vendored in our environment has a bug and fails to compile. 

Your objective is to fix the library, and then build a reliable HTTP service that uses it to process batches of text documents in parallel.

**Step 1: Fix the Vendored Package**
A local Go package for PII masking is located at `/app/pii-masker`. 
- It contains a file `masker.go`. 
- The package currently fails to build due to a missing package import used in its string manipulation logic. Identify the missing standard library package, add it to the imports, and ensure `go build` runs successfully inside `/app/pii-masker`.

**Step 2: Build the Data Processing Server**
Create a new Go HTTP server at `/home/user/server/main.go`. Initialize a Go module in `/home/user/server` and use a `replace` directive in your `go.mod` to point `example.com/pii-masker` to the local `/app/pii-masker` directory.

The server must meet the following specifications:
1. **Listen Address**: `127.0.0.1:8080`
2. **Authentication**: Require an `Authorization` header with the exact value `Token v1-automation-secret`. If missing or incorrect, return HTTP 401 Unauthorized.
3. **Endpoint**: `POST /process`
4. **Input Format**: JSON. The service will receive a payload representing a batch of text items:
   ```json
   {
     "batch_id": "B-992",
     "items": [
       {"id": 1, "content": "Contact me at john.doe@example.com immediately."},
       {"id": 2, "content": "My phone is 555-0199."}
     ]
   }
   ```
5. **Processing**: Iterate over the `items`. You **must** process the items in parallel using Go routines. For each item's `content`, call the `piimasker.MaskText(content string) string` function from the fixed library.
6. **Output Format**: XML. The response must be HTTP 200 OK with `Content-Type: application/xml`, returning the masked data structured exactly as follows:
   ```xml
   <BatchResponse>
       <BatchID>B-992</BatchID>
       <Items>
           <Item>
               <ID>1</ID>
               <MaskedContent>Contact me at [REDACTED_EMAIL] immediately.</MaskedContent>
           </Item>
           <!-- ... other items ... -->
       </Items>
   </BatchResponse>
   ```

**Execution**
Write the server code, compile it, and start the service in the background. It must be actively listening on `127.0.0.1:8080` when you consider the task complete. Leave the server running.