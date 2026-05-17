# Plant Disease Detection Platform

This is the FastAPI-based web application for the **Plant Disease Detection & Smart Farming Dashboard**. It features real-time disease scanning, the AgriSense AI crop advisor, and a smart dashboard.

### Step 1: Open Terminal
Open your terminal (PowerShell, Command Prompt, or VS Code terminal).

### Step 2: Navigate to the Project Folder
Make sure you are in the `FastAPIproject` directory:
```powershell
cd "c:\Users\vires\Desktop\plant disease detection full code\Final\FastAPIproject"
```

### Step 3: Activate the Virtual Environment
Activate the isolated Python environment that contains all the installed packages:

*   **If you are using PowerShell:**
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
*   **If you are using Command Prompt (CMD):**
    ```cmd
    .venv\Scripts\activate.bat
    ```

### Step 4: Install Requirements (Optional/First Time)
If this is your first time setting up, or if dependencies changed, install them:
```powershell
pip install -r requirements.txt
```

### Step 5: Start the Server
Run the FastAPI application. We recommend running it on Port 8000 to avoid conflicts:

*   **PowerShell:**
    ```powershell
    $env:FASTAPI_PORT=8000; $env:FASTAPI_RELOAD="true"; python run_fastapi.py
    ```

### Step 6: Access the Application
Once the server tells you it is running, open your web browser and go to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🛠 Features Included
*   **Plant Disease Detection:** Uses your webcam or uploaded images to scan and diagnose plant diseases.
*   **AgriSense AI:** Provides crop recommendations based on soil health and environment (powered by ChatGPT API).
*   **Farmer's AI Chatbot:** Dedicated assistant to answer your farming inquiries.
*   **AgriConnect Marketplace:** Direct connection to buyers and suppliers.
*   **Dashboard:** Tracks environment levels and farm metrics.
