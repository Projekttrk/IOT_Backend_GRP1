from application import app
import processing
from flask import request

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    processing.process_request(data)
    return 'ok', 200