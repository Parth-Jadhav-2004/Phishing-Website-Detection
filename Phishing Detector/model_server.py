from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import re
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)  # Allow requests from Chrome extension

# Load the trained XGBoost model
model = pickle.load(open("XGBoostClassifier.pickle.dat", "rb"))

# Feature extraction function
def extract_features(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    shorteners = ["bit.ly", "goo.gl", "tinyurl", "t.co", "ow.ly", "is.gd", "buff.ly"]

    features = {
        "Have_IP": 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        "Have_At": 1 if "@" in url else 0,
        "URL_Length": len(url),
        "URL_Depth": path.count('/'),
        "Redirection": url.count('//') - 1,
        "https_Domain": 1 if "https" in url else 0,
        "TinyURL": 1 if any(shortener in url for shortener in shorteners) else 0,
        "Prefix/Suffix": 1 if "-" in domain else 0,
        "DNS_Record": 1,  # Placeholder (adjust based on real DNS lookup)
        "Web_Traffic": 5,  # Placeholder (use Alexa API for real traffic)
        "Domain_Age": 365,  # Placeholder (use WHOIS lookup for real age)
        "Domain_End": 100,  # Placeholder (days until domain expiration)
        "iFrame": 0,  # Placeholder (check HTML content if needed)
        "Mouse_Over": 0,  # Placeholder (check for hover-based redirects)
        "Right_Click": 0,  # Placeholder (check if right-click is disabled)
        "Web_Forwards": 0  # Placeholder (detect multiple redirects)
    }

    # Convert features into DataFrame
    feature_order = [
        "Have_IP", "Have_At", "URL_Length", "URL_Depth", "Redirection",
        "https_Domain", "TinyURL", "Prefix/Suffix", "DNS_Record", "Web_Traffic",
        "Domain_Age", "Domain_End", "iFrame", "Mouse_Over", "Right_Click", "Web_Forwards"
    ]

    df_features = pd.DataFrame([features])[feature_order]

    return df_features

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    features = extract_features(url)
    prediction = model.predict(features)[0]
    result = "Phishing" if prediction == 1 else "Legitimate"

    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
