from flask import Flask, jsonify, request
import os
from models import db,  Scanned, Request, User
from flask_migrate import Migrate
import requests
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app)
DB_CONFIG = {
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("DB_PORT")
    }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"


db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to moringa API'})


@app.route('/scanned', methods=['POST'])
def create_scanned():
    name = request.json.get('name')
    user_id=request.json.get('user_id')
    scanned = Scanned(name=name, user_id=user_id)
    db.session.add(scanned)
    db.session.commit()
    return jsonify({'message': 'Scanned entry created successfully'}), 201
@app.route('/scanned/<int:scanned_id>', methods=['PATCH'])
def update_scanned(scanned_id):
    expo_token = request.args.get('expo_token')
    scanned = Scanned.query.get(scanned_id)
    if not scanned:
        return jsonify({'error': 'Scanned entry not found'}), 404
    status = request.json.get('status')
    scanned.status = status
    db.session.commit()
    
    if status == 'approved':
        url = 'https://api.exp.host/v2/push/send'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'to': expo_token,
            'sound': 'default',
            'title': 'Approved',
            'body': 'Asset request has been approved',
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to send notification'}), 500
    elif status == 'rejected':
        url = 'https://api.exp.host/v2/push/send'
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'to': expo_token,
            'sound': 'default',
            'title': 'Rejected',
            'body': 'Asset request has been cancelled',
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to send notification'}), 500
    return jsonify({'message': 'Scanned entry updated successfully'}), 200
@app.route('/scanned/<int:scanned_id>', methods=['DELETE'])
def delete_scanned(scanned_id):
    scanned = Scanned.query.get(scanned_id)
    if not scanned:
        return jsonify({'error': 'Scanned entry not found'}), 404
    db.session.delete(scanned)
    db.session.commit()
    return jsonify({'message': 'Scanned entry deleted successfully'}), 200

@app.route('/scanned', methods=['GET'])
def get_scanned_history():
    """
    Get scanned history
    """
    scanned_entries = Scanned.query.all()
    return jsonify([scanned.to_dict() for scanned in scanned_entries])

@app.route('/scanned/<int:scanned_id>', methods=['GET'])
def get_scanned_entry(scanned_id):
    """
    Get a single scanned entry
    """
    scanned = Scanned.query.get(scanned_id)
    if scanned:
        return jsonify(scanned.to_dict())
    return jsonify({'error': 'Scanned entry not found'}), 404


@app.route('/requests', methods=['POST'])
def create_request():
    asset_id = request.json.get('asset_id')
    user_id = request.json.get('user_id')
    user_name = request.json.get('user_name')
    asset_name = request.json.get('asset_name')
    my_request = Request(asset_id=asset_id, user_id=user_id, user_name=user_name, asset_name=asset_name)
    db.session.add(my_request)
    db.session.commit()
    return jsonify({'message': 'Request created successfully'}), 201

@app.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    request = Request.query.get(request_id)
    if request is None:
        return jsonify({'message': 'Request not found'}), 404
    return jsonify(request.to_dict()), 200

@app.route('/requests/<int:request_id>/approve', methods=['PATCH'])
def approve_request(request_id):
    my_request = Request.query.get(request_id)
    if my_request is None:
        return jsonify({'message': 'Request not found'}), 404
    my_request.status = 'approved'
    db.session.commit()
    return jsonify({'message': 'Request approved successfully'}), 200

@app.route('/requests/<int:request_id>/reject', methods=['PATCH'])
def reject_request(request_id):
    my_request = Request.query.get(request_id)
    if my_request is None:
        return jsonify({'message': 'Request not found'}), 404
    my_request.status = 'rejected'
    db.session.commit()
    return jsonify({'message': 'Request rejected successfully'}), 200

@app.route('/requests/<int:request_id>', methods=['DELETE'])    
def delete_request(request_id):
    my_request = Request.query.get(request_id)
    if my_request is None:
        return jsonify({'message': 'Request not found'}), 404
    db.session.delete(my_request)
    db.session.commit()
    return jsonify({'message': 'Request deleted successfully'}), 200
@app.route('/requests', methods=['GET'])
def get_requests():
    my_requests = Request.query.all()
    return jsonify([my_request.to_dict() for my_request in my_requests]), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6010)
    
