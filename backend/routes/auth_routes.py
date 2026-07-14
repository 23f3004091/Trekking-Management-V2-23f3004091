
from models import User, UserRole, ProfileStatus, Trek, StaffProfile, Trekker
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from extensions import db

auth_bp = Blueprint('auth', __name__)


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
    
    trekker_profile = Trekker(user_id=new_user.id, age=25, blacklisted=False)
    db.session.add(trekker_profile)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/register-staff', methods=['POST'])
def register_staff():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    contact_details = data.get('contact_details', '')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username, email=email, role=UserRole.TREK_STAFF)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    staff_profile = StaffProfile(user_id=new_user.id, contact_details=contact_details, status=ProfileStatus.PENDING)
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

    if user.role == UserRole.TREK_STAFF:
        staff_profile = StaffProfile.query.filter_by(user_id=user.id).first()
        if staff_profile.status == ProfileStatus.PENDING:
            return jsonify({"error": "Profile is waiting for approval by admin"}), 403
        elif staff_profile.status == ProfileStatus.REJECTED:
            return jsonify({"error": "Profile has been rejected by admin"}), 403
        elif staff_profile.status == ProfileStatus.APPROVED and staff_profile.blacklisted:
            return jsonify({"error": "Staff is blacklisted"}), 403
        
    if user.role == UserRole.TREKKER:
        trekker_profile = Trekker.query.filter_by(user_id=user.id).first()
        if trekker_profile.blacklisted:
            return jsonify({"error": "Trekker is blacklisted"}), 403
        
        
    claims = {"role": user.role.value, "username": user.username}
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=claims)
    access_token = create_access_token(identity=str(user.id),
                                       additional_claims=claims)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    user = User.query.get(int(current_user))
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    claims = {"role": user.role.value, "username": user.username}
    
    new_access_token = create_access_token(identity=current_user, fresh=False, additional_claims=claims)
    new_refresh_token = create_refresh_token(identity=current_user, additional_claims = claims)
    
    return jsonify({
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }), 200