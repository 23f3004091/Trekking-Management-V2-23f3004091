
from models import User, UserRole, ProfileStatus, Trek, StaffProfile
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user, fresh=False)
    new_refresh_token = create_refresh_token(identity=current_user)
    
    return jsonify({
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }), 200

@auth_bp.route('/register-trekker', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    # role = data.get('role', UserRole.TREKKER)  # Default role is TREKKER

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400
    
    new_user = User(username=username, email=email, role=UserRole.TREKKER)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/register-staff', methods=['POST'])
def register_staff():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    contact_details = data.get('contact_details', '')
    status = data.get('status', ProfileStatus.ACTIVE)  # Default status is ACTIVE

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username, email=email, role=UserRole.TREK_STAFF)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    staff_profile = StaffProfile(user_id=new_user.id, contact_details=contact_details, status=status)
    db.session.add(staff_profile)
    db.session.commit()

    return jsonify({"message": "Staff registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    claims = {"role": user.role.value, "username": user.username}
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=claims)
    access_token = create_access_token(identity=str(user.id),
                                       additional_claims=claims)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
