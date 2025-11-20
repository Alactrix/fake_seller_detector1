from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.features import calculate_score

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    if not url.startswith("http"):
        url = "https://" + url

    try:
        score, reasons = calculate_score(url)
        return jsonify({
            "url": url,
            "score": score,
            "reasons": reasons
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)