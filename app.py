from flask import Flask, jsonify, request
import os
from models import db, Asset,User,Scanned
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity



app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1209600 
jwt = JWTManager(app)

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
    date_created = request.json.get('date_created')

    asset = Asset(asset_id=asset_id, name=name, description=description, condition=condition, category=category, space=space, status=status)
    db.session.add(asset)
    db.session.commit()
    return jsonify({'message': 'Asset created successfully'}), 201

@app.route('/asset/<asset_id>', methods=['PATCH'])
def update_asset(asset_id):
    asset = Asset.query.filter_by(asset_id=asset_id).first()
    if asset is None:
        return jsonify({'message': 'Asset not found'}), 404
    name = request.json.get('name')
    description = request.json.get('description')
    condition = request.json.get('condition')
    category = request.json.get('category')
    space = request.json.get('space')
    status = request.json.get('status')
    asset.name = name
    asset.description = description
    asset.condition = condition
    asset.category = category
    asset.space = space
    asset.status = status
    
    db.session.commit()
    return jsonify({'message': 'Asset updated successfully'}), 200
@app.route('/asset/<asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    asset = Asset.query.filter_by(asset_id=asset_id).first()
    if asset is None:
        return jsonify({'message': 'Asset not found'}), 404
    db.session.delete(asset)
    db.session.commit()
    return jsonify({'message': 'Asset deleted successfully'}), 200

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



@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]}), 200



@app.route('/user', methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Invalid email'}), 401
    if user.password != password:
        return jsonify({'message': 'Invalid password'}), 401
    access_token = create_access_token(identity=user.email, expires_delta=False)
    return jsonify({'access_token': access_token}), 200


@app.route('/user', methods=['POST'])
def create_user():
    email = request.json.get('email')
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'message': 'User already exists'}), 400
    username = request.json.get('username')
    password = request.json.get('password')

    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201



@app.route('/protected/user', methods=['GET'])
@jwt_required()
def protected_user():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

 
@app.route('/edituser/<email>', methods=['PATCH'])
def edit_user(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'message': 'Email address not found'}), 404
    username = request.json.get('username')
    password = request.json.get('password')
    phone_number = request.json.get('phone_number')
    user.username = username
    user.password = password
    user.phone_number = phone_number
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


@app.route('/deleteuser/<email>', methods=['DELETE'])
def delete_user(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'message': 'Email address not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200



@app.route('/scanned', methods=['POST'])
def create_scanned():
    
    asset_id_param = request.json.get('asset_id')
    id_param = request.json.get('id')   
     
    if not asset_id_param or not id_param:
        return jsonify({'error': 'Missing asset_id or id'}), 400

    asset = Asset.query.get(asset_id_param)
    user = User.query.get(id_param)

    if not asset :
        return jsonify({'error': 'Invalid asset_id'}), 400

    if not user:
        return jsonify({'error': 'Invalid user_id'}), 400
    scanned = Scanned(asset_id=asset_id_param, user_id=id_param)
    db.session.add(scanned)
    db.session.commit()

    return jsonify({'message': 'Scanned entry created successfully'}), 201



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