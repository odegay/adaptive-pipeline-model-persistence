import os
import logging
from flask import Flask, request, jsonify
from google.cloud import firestore
from adpipsvcfuncs import fetch_gcp_secret

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)  # Capture DEBUG, INFO, WARNING, ERROR, CRITICAL
if not root_logger.handlers:
    # Create console handler and set its log level to DEBUG
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # Add the handler to the root logger
    root_logger.addHandler(ch)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Capture DEBUG, INFO, WARNING, ERROR, CRITICAL

app = Flask(__name__)

db = firestore.Client()
if db is None:
    logger.error(f"Error: Unable to connect to firestore database")
    raise Exception("Error: Unable to connect to firestore database")
logger.info(f"Connected to firestore database db: {db}")

# Fetching API key from GCP secret manager
api_key = fetch_gcp_secret('adaptive-pipeline-API-token')

def check_api_key(request):
    token = request.headers.get('Authorization')
    IP_address = request.remote_addr
    if token != api_key:
        logger.error(f"Error: Unauthorized access from IP: {IP_address}")
        return jsonify({"success": False, "error": "Not found"}), 404
    return None    

@app.route("/hb")
def service_working_confirmation():        
    logger.info(f"Recieved debug heartbeat request")
    return f"Adaptive pipeline model persistence service is working"

@app.route('/create', methods=['POST'])
def create():
    logger.info(f"Recieved create request with data: {request.json}")
    try:
        response = check_api_key(request)
        if response:
            return response
        data = request.json
        ref = db.collection('adaptive-pipelines').add(data)
        logger.info(f"Document created with ID: {ref[1].id}")
        return jsonify({"success": True, "id": ref[1].id}), 200
    except Exception as e:
        logger.info(f"Error: {str(e)}")
        logger.error(f"Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/read/<doc_id>', methods=['GET'])
def read(doc_id):
    logger.info(f"Recieved read request for doc_id: {doc_id}")
    try:
        response = check_api_key(request)
        if response:
            return response
        doc = db.collection('adaptive-pipelines').document(doc_id).get()
        if doc.exists:
            logger.info(f"Document found: {doc.to_dict()}")
            return jsonify(doc.to_dict()), 200
        else:
            logger.info(f"Document not found")
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        logger.info(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/update/<doc_id>', methods=['PUT'])
def update(doc_id):
    logger.info(f"Recieved update request for doc_id: {doc_id} with data: {request.json}")
    try:
        response = check_api_key(request)
        if response:
            return response
        data = request.json
        db.collection('adaptive-pipelines').document(doc_id).update(data)        
        logger.info(f"Document updated successfully")
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.info(f"Error: {str(e)}")
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/delete/<doc_id>', methods=['DELETE'])
def delete(doc_id):
    try:
        logger.info(f"Recieved delete request for doc_id: {doc_id}")
        response = check_api_key(request)
        if response:
            return response
        db.collection('adaptive-pipelines').document(doc_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
