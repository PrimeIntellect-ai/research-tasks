You are a FinOps analyst responsible for optimizing cloud costs and building out the alerting stage of our internal CI/CD pipeline. 

We recently received a snapshot of our newly negotiated cloud compute rates, which is saved as an image at `/app/rates.png`. The image contains the hourly rates for three specific regions: `US_EAST`, `US_WEST`, and `EU_CENTRAL`.

Your task is to write an executable program at `/home/user/billing_alert` (you may use any programming language, but ensure it is properly chmod'd and has the correct shebang). This program will be executed by our CI/CD pipeline to process daily usage logs and generate an automated email payload.

Requirements for `/home/user/billing_alert`:
1. It must read standard input (`stdin`). The input will consist of an arbitrary number of lines representing usage. Each line contains a region name and an integer representing hours used, separated by a space (e.g., `US_EAST 45`).
2. It must calculate the total cost of the provided usage using the precise rates found in the `/app/rates.png` image. You may use OCR (e.g., `tesseract` is installed) to read the image, or simply read it yourself and hardcode the parsed rates into your script.
3. It must output a strictly formatted SMTP-ready email string to standard output (`stdout`) containing the exact total cost. The cost must be formatted to exactly two decimal places. 

The output format must be EXACTLY as follows:
```
From: finops@local
To: billing-alerts@local
Subject: Daily Cloud Cost Alert

Total Cost: $<total>
```
(Replace `<total>` with the calculated sum).

Our automated test suite will run your `/home/user/billing_alert` script against thousands of randomly generated usage logs and compare the output byte-for-byte against a reference oracle. Ensure your math is exact and your formatting perfectly matches the template.