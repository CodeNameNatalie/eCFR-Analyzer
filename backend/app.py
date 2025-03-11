# backend/app.py

import requests
import re
from collections import defaultdict
from flask import Flask, jsonify, send_from_directory, request
from datetime import datetime, timedelta
import os

# Get the absolute path to the frontend directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
static_dir = os.path.join(frontend_dir, 'static')

app = Flask(__name__, static_folder=static_dir)

# eCFR API base URL and endpoints
ECFR_BASE_URL = "https://www.ecfr.gov"
AGENCIES_ENDPOINT = f"{ECFR_BASE_URL}/api/admin/v1/agencies.json"
TITLES_ENDPOINT = f"{ECFR_BASE_URL}/api/versioner/v1/titles.json"
CORRECTIONS_ENDPOINT = f"{ECFR_BASE_URL}/api/admin/v1/corrections.json"
SEARCH_ENDPOINT = f"{ECFR_BASE_URL}/api/search/v1/results"

def make_api_request(url):
    """
    Make an API request with proper error handling
    """
    try:
        response = requests.get(url)
        if response.status_code == 403:
            return {
                "error": "API Access Required",
                "message": "You need to register your IP address to access the eCFR API. Please visit https://www.ecfr.gov/reader-aids/ecfr-developer-resources/rest-api-interactive-documentation and complete the registration process."
            }, 403
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return {
            "error": "API Error",
            "message": str(e)
        }, 500

# Sample data for development/testing
SAMPLE_DATA = {
    "agencies": [
        {
            "name": "Department of Agriculture",
            "children": [
                {"name": "Agricultural Marketing Service", "titles": [7]}
            ],
            "titles": [7]
        },
        {
            "name": "Department of Commerce",
            "children": [],
            "titles": [15]
        }
    ]
}

def fetch_ecfr_data():
    """
    Download the current eCFR data from the public API.
    Falls back to sample data if API access is not available.
    """
    try:
        # Get agencies data
        agencies_data, error = make_api_request(AGENCIES_ENDPOINT)
        if error:
            print(f"Using sample data due to API error: {error}")
            return SAMPLE_DATA.get("agencies", [])

        # Get titles data
        titles_data, error = make_api_request(TITLES_ENDPOINT)
        if error:
            print(f"Using sample data due to API error: {error}")
            return SAMPLE_DATA.get("agencies", [])

        # Combine the data
        regulations = []
        
        # Process agencies
        for agency in agencies_data.get('agencies', []):
            agency_name = agency.get('name', 'Unknown')
            cfr_refs = agency.get('cfr_references', [])
            
            # Get the associated titles for this agency
            for ref in cfr_refs:
                title_num = ref.get('title')
                # Find matching title data
                for title in titles_data.get('titles', []):
                    if title.get('number') == title_num:
                        regulations.append({
                            'agency': agency_name,
                            'text': f"Title {title_num} - {title.get('name', '')}",
                            'last_updated': title.get('latest_amended_on')
                        })
                        break

        return regulations
    except Exception as e:
        print(f"Error fetching eCFR data: {str(e)}")
        return SAMPLE_DATA.get("agencies", [])

def analyze_word_counts(regulations):
    """
    Compute the word count per agency.
    """
    word_counts = defaultdict(int)
    for reg in regulations:
        agency = reg.get('agency', 'Unknown')
        text = reg.get('text', '')
        words = re.findall(r'\w+', text)
        word_counts[agency] += len(words)
    return dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))

def historical_changes(regulations):
    """
    Analyze historical changes by date.
    """
    changes = defaultdict(int)
    for reg in regulations:
        update_date = reg.get('last_updated')
        if update_date:
            try:
                date_obj = datetime.fromisoformat(update_date)
                date_key = date_obj.strftime("%Y-%m-%d")
                changes[date_key] += 1
            except ValueError:
                changes["unknown"] += 1
        else:
            changes["unknown"] += 1
    return dict(sorted(changes.items()))

@app.route("/api/ecfr")
def api_ecfr():
    data = fetch_ecfr_data()
    return jsonify(data)

@app.route("/api/word_counts")
def api_word_counts():
    data = fetch_ecfr_data()
    counts = analyze_word_counts(data)
    return jsonify(counts)

@app.route("/api/historical")
def api_historical():
    data = fetch_ecfr_data()
    changes = historical_changes(data)
    return jsonify(changes)

@app.route("/api/agency_hierarchy")
def api_agency_hierarchy():
    """Get agency hierarchy data for visualization"""
    try:
        data, error = make_api_request(AGENCIES_ENDPOINT)
        if error:
            if error == 403:
                return jsonify({"name": "API Access Required", "children": [], "message": data["message"]}), 200
            return jsonify(SAMPLE_DATA), 200

        # Transform data into hierarchical format
        hierarchy = {
            "name": "All Agencies",
            "children": []
        }
        
        for agency in data.get('agencies', []):
            agency_node = {
                "name": agency.get('name'),
                "children": [],
                "titles": [ref.get('title') for ref in agency.get('cfr_references', [])]
            }
            
            # Add children agencies if any
            for child in agency.get('children', []):
                child_node = {
                    "name": child.get('name'),
                    "titles": [ref.get('title') for ref in child.get('cfr_references', [])]
                }
                agency_node["children"].append(child_node)
            
            hierarchy["children"].append(agency_node)
        
        return jsonify(hierarchy)
    except Exception as e:
        return jsonify(SAMPLE_DATA), 200

@app.route("/api/corrections_analysis")
def api_corrections_analysis():
    """Get corrections data for visualization"""
    try:
        response = requests.get(CORRECTIONS_ENDPOINT)
        response.raise_for_status()
        corrections_data = response.json()
        
        # Analyze corrections
        corrections_by_title = defaultdict(int)
        corrections_by_date = defaultdict(int)
        corrective_actions = defaultdict(int)
        
        for correction in corrections_data.get('ecfr_corrections', []):
            title = correction.get('title')
            date = correction.get('error_corrected')
            action = correction.get('corrective_action')
            
            corrections_by_title[str(title)] += 1
            corrections_by_date[date] += 1
            corrective_actions[action] += 1
        
        return jsonify({
            "by_title": dict(corrections_by_title),
            "by_date": dict(corrections_by_date),
            "by_action": dict(corrective_actions)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/title_status")
def api_title_status():
    """Get title status information"""
    try:
        response = requests.get(TITLES_ENDPOINT)
        response.raise_for_status()
        titles_data = response.json()
        
        # Process title status
        status_data = []
        for title in titles_data.get('titles', []):
            status_data.append({
                "number": title.get('number'),
                "name": title.get('name'),
                "latest_amendment": title.get('latest_amended_on'),
                "latest_issue": title.get('latest_issue_date'),
                "up_to_date_as_of": title.get('up_to_date_as_of'),
                "processing": title.get('processing_in_progress', False)
            })
        
        return jsonify(status_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return send_from_directory(static_dir, "index.html")

if __name__ == "__main__":
    # For development only; use a production server for deployment.
    app.run(debug=True)
