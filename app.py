from flask import Flask, jsonify, request
import os
from models import db, Asset
from flask_migrate import Migrate
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to moringa API'})
@app.route('/asset', methods=['POST'])
def create_assets():
    
    asset_id = request.json.get('asset_id')
    if Asset.query.filter_by(asset_id=asset_id).first() is not None:
        return jsonify({'message': 'Asset already exists'}), 400
    name = request.json.get('name')
    description = request.json.get('description')
    condition = request.json.get('condition')
    category = request.json.get('category')
    space = request.json.get('space')
    status = request.json.get('status')

    asset = Asset(asset_id=asset_id, name=name, description=description, condition=condition, category=category, space=space, status=status)
    db.session.add(asset)
    db.session.commit()
    return jsonify({'message': 'Asset created successfully'}), 201

@app.route('/assets', methods=['GET'])
def get_assets():
    assets = Asset.query.all()
    return jsonify({'assets': [asset.to_dict() for asset in assets]}), 200  

@app.route('/asset/<asset_id>', methods=['GET'])
def get_asset(asset_id):
    asset = Asset.query.filter_by(asset_id=asset_id).first()
    if asset is None:
        return jsonify({'message': 'Asset not found'}), 404
    return jsonify({'asset': asset.to_dict()}), 200