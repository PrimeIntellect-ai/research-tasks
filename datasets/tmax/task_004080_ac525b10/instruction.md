You are a data scientist working in a restricted environment with only basic shell tools available.

We have received an image containing historical trend data at `/app/historical_trend.png`. 

Your task is to:
1. Extract the tabular data (Year and Value) from the image.
2. Use standard Linux command-line tools (like `awk`, `bash`, `bc`) to perform a least-squares linear regression (curve fitting) on the extracted data to find the best fit line ($Value = m \times Year + c$).
3. Use your derived model to forecast the `Value` for the upcoming Years: 6, 7, 8, 9, and 10.
4. Save your predicted values for these 5 years to `/home/user/forecast.txt`. The file should contain exactly 5 lines, with one numeric predicted value per line, corresponding to years 6 through 10 in ascending order.

No Python or specialized statistical software is allowed; you must rely entirely on Bash-compatible tools. Tesseract OCR is available for extracting text from the image. 

Your predictions will be evaluated based on their Mean Squared Error (MSE) compared to the exact least-squares analytical solution. To succeed, your predictions must yield an MSE of less than 0.05.