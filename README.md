# eCFR Analyzer

A web application that analyzes the Electronic Code of Federal Regulations (eCFR) data using the official [eCFR API](https://www.ecfr.gov/). This tool provides visualizations of regulation data, including word counts per agency and historical changes tracking.

## Features

- **Agency Word Count Analysis**: Visualizes the volume of regulations by counting words per agency
- **Historical Changes Tracker**: Tracks and displays regulation updates over time
- **Interactive Charts**: Uses Chart.js for dynamic data visualization
- **Real-time Data**: Fetches current data from the official eCFR API

## Prerequisites

- Python 3.x
- Web browser (Chrome, Firefox, Safari, etc.)
- Internet connection (for accessing the eCFR API)

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
   cd backend
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask backend server:
   ```bash
   cd backend
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. The dashboard will display:
   - A bar chart showing word counts per agency
   - A line chart showing historical regulation changes

## Project Structure

```
eCFR-Analyzer/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── venv/              # Virtual environment
├── frontend/
│   ├── static/
│   │   ├── index.html     # Main webpage
│   │   └── chart.min.js   # Chart.js library
│   └── assets/            # Static assets (images, css, etc.)
└── README.md
```

## API Endpoints

- `/api/ecfr`: Returns raw eCFR data
- `/api/word_counts`: Returns word count analysis per agency
- `/api/historical`: Returns historical changes data

## Technical Details

- **Backend**: Python Flask server
- **Frontend**: HTML, JavaScript with Chart.js
- **Data Source**: Official eCFR API (www.ecfr.gov)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Data provided by the [Electronic Code of Federal Regulations (eCFR)](https://www.ecfr.gov/)
- Visualization powered by [Chart.js](https://www.chartjs.org/)
