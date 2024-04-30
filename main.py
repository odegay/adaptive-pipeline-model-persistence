from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase Admin
cred = credentials.Certificate("path/to/your/firebase-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/create', methods=['POST'])
def create():
    try:
        data = request.json
        ref = db.collection('your-collection').add(data)
        return jsonify({"success": True, "id": ref[1].id}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/read/<doc_id>', methods=['GET'])
def read(doc_id):
    try:
        doc = db.collection('your-collection').document(doc_id).get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/update/<doc_id>', methods=['PUT'])
def update(doc_id):
    try:
        data = request.json
        db.collection('your-collection').document(doc_id).update(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/delete/<doc_id>', methods=['DELETE'])
def delete(doc_id):
    try:
        db.collection('your-collection').document(doc_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
