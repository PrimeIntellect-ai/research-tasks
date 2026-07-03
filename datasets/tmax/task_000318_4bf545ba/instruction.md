You are an incoming Data Scientist taking over a partially finished project. The previous engineer left abruptly, leaving behind raw data, a PyTorch model weights file, and a scanned sticky note with vital project parameters. 

Your goal is to extract the rules from the note, clean the dataset, reconstruct the model architecture, and deploy an HTTP API to serve both the cleaning statistics and model predictions.

**Initial Assets:**
1. **The Sticky Note (`/app/cleaning_rules.png`):** An image containing the handwritten cleaning protocol (outlier thresholds and imputation strategies) and the missing PyTorch model architecture hidden layer dimensions. You will need to use OCR (e.g., `pytesseract` and `Pillow` are available) to read this file.
2. **The Raw Dataset (`/home/user/data/raw_sensor_data.csv`):** A CSV containing sensor readings: `id`, `temperature`, `humidity`, and `pressure`.
3. **The Model Weights (`/home/user/model/weights.pth`):** A PyTorch `state_dict` for a Feed-Forward Neural Network.

**Your Tasks:**

**1. Data Cleaning:**
Read `/app/cleaning_rules.png` to find the cleaning rules. Apply these rules to `/home/user/data/raw_sensor_data.csv`. Keep track of:
- The exact number of rows dropped due to outlier rules.
- The exact number of rows where missing values were imputed.

**2. Model Reconstruction:**
The image also specifies the hidden layer sizes for the PyTorch model. 
- The model takes 3 inputs (temperature, humidity, pressure) and outputs 1 value.
- The architecture is a simple sequential MLP: `Linear(3, hidden_1) -> ReLU -> Linear(hidden_1, hidden_2) -> ReLU -> Linear(hidden_2, 1)`.
- Reconstruct this architecture using the sizes found in the image and load the `weights.pth`.

**3. API Deployment:**
Create and run a web server (e.g., using FastAPI or Flask) listening on `127.0.0.1:8080`. The server must run continuously in the background or foreground of your final terminal session.
The API must require authentication via the header: `Authorization: Bearer data_ops_2024`.

Implement two endpoints:
- `GET /stats`
  Returns a JSON response with the cleaning experiment tracking:
  `{"dropped_outliers": <int>, "imputed_missing": <int>}`

- `POST /predict`
  Accepts a JSON payload: `{"temperature": <float>, "humidity": <float>, "pressure": <float>}`.
  Passes these 3 features (in that exact order) as a tensor to your reconstructed PyTorch model and returns the prediction:
  `{"prediction": <float>}`

Make sure your API is up and running on port 8080 before you finish the task.