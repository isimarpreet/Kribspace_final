from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqliteconnect
import google_ai_nlp
import os


app = Flask(__name__, static_url_path='/KRIBSPACE-PROTO/static/index.html', static_folder='static')
CORS(app)  # Enable CORS

@app.route('/')
def serve_index():
    app.logger.info('Serving index.html')
    return send_from_directory('static', 'index.html')

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        natural_query = data.get('query')
        if not natural_query:
            return jsonify({"error": "No query provided"}), 400
        sql_query = google_ai_nlp.process_query(natural_query)
        results = sqliteconnect.execute_query(sql_query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
