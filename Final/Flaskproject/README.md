# Plant Disease Detection & AgriSense AI

A comprehensive AI-powered agricultural platform designed to monitor plant health, detect diseases, and provide expert crop recommendations.

## 🚀 Key Features

### 1. **Plant Disease Detection**
- Upload or capture images of plant leaves to identify diseases using deep learning.
- Receive immediate diagnostic results and treatment suggestions.

### 2. **AgriSense AI: Smart Advisor**
- **Dynamic Recommendations:** Integrates with the **OpenRouter API (DeepSeek)** to provide context-aware crop suggestions based on real-time sensor data.
- **Interactive Chatbot:** A modern, premium chat interface with message bubbles and avatars for follow-up agricultural advice.
- **Smart Data Sync:** Automatically pulls Temperature, Humidity, Soil Moisture, and pH from the monitor dashboard.

### 3. **Monitor Dashboard**
- Real-time visualization of environmental sensor data.
- Geographical mapping of field locations.

### 4. **Today's Forecast**
- Live weather integration to help farmers plan their daily activities.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual Environment (`venv`) 추천

### Steps
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd "plant disease detection full code/Final/Flaskproject"
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```powershell
   python run.py
   ```
   The application will be available at `http://127.0.0.1:5000`.

## 📂 Project Structure
- `project/`: Main application directory containing Flask routes and models.
- `project/templates/`: HTML templates for the UI.
- `project/static/`: CSS, JavaScript, and asset files.
- `run.py`: Entry point for the Flask server.

---
*Developed for intelligent agricultural management.*
