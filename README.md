# eCFR Analyzer

A web application that analyzes the Electronic Code of Federal Regulations (eCFR) data using the official [eCFR API](https://www.ecfr.gov/). This tool provides visualizations of regulation data, including word counts per agency and historical changes tracking.

## Features

- **Agency Word Count Analysis**: Visualizes the volume of regulations by counting words per agency
- **Title Status Overview**: Tracks and displays the current status of all CFR titles
- **Historical Changes Tracker**: Tracks and displays regulation updates over time
- **Agency Hierarchy**: Visualizes the organizational structure of regulatory agencies
- **Corrections Analysis**: Tracks and analyzes corrections made to regulations
- **Interactive Charts**: Uses Chart.js for dynamic data visualization
- **Real-time Data**: Fetches current data from the official eCFR API

## Prerequisites

- Python 3.8+
- Web browser (Chrome, Firefox, Safari, etc.)
- Internet connection (for accessing the eCFR API)
- Redis (for production deployment)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/eCFR-Analyzer.git
   cd eCFR-Analyzer
   ```

2. Create and activate a virtual environment:
   ```bash
   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # For Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Required configurations in .env:
   - FLASK_APP: Set to backend/app.py
   - SECRET_KEY: Your secret key
   - PORT: Default is 5000
   - REDIS_URL: Required for production
   - LOG_LEVEL: Default is INFO

Note: If you cannot access the eCFR API, the application will fall back to sample data for demonstration purposes.

## Usage

1. Start the Flask backend server:
   ```bash
   flask run
   ```
   The server will start on the port specified in your .env file (default: 5000)

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. The dashboard will display:
   - Word count analysis per agency
   - Title status overview
   - Historical regulation updates
   - Cumulative regulation changes
   - Agency hierarchy
   - Corrections analysis

Note: For full functionality, you may need to register your IP address with the eCFR API.

## Project Structure

```
eCFR-Analyzer/
├── backend/
│   ├── app.py              # Flask application with API endpoints
│   └── config.py           # Environment and application configuration
├── frontend/
│   └── static/
│       └── index.html     # Main webpage with Chart.js from CDN
├── requirements.txt        # Python dependencies
├── .env.example           # Template for required environment variables
└── README.md             # Project documentation
```

## API Endpoints

- `/api/ecfr`: Returns raw eCFR data from the official API
- `/api/word_counts`: Returns word count analysis per agency
- `/api/historical`: Returns historical changes data over time
- `/api/agency_hierarchy`: Returns hierarchical structure of agencies and their relationships
- `/api/corrections_analysis`: Returns analysis of corrections data including:
  - Corrections by title
  - Corrections by date
  - Types of corrective actions
- `/api/title_status`: Returns detailed status information for each CFR title including:
  - Latest amendments
  - Processing status
  - Up-to-date information

## Technical Details

- **Backend**: Python Flask server with Redis caching (production)
- **Frontend**: HTML, JavaScript with Chart.js
- **Data Source**: Official eCFR API (www.ecfr.gov)

## Data Sources

- Data provided from [Electronic Code of Federal Regulations (eCFR)](https://www.ecfr.gov/)
- API registration may be required for full functionality
