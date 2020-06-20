from application import app, processing
from flask import request


@app.route('/api', methods=['POST'])
def api():
    response = processing.process_request(request.json)
    if not response:
        return "ok", 200
    return response, 200
