
from flask import Blueprint, jsonify, request
from models import Trek, StaffProfile, Booking, TrekStatus, Trekker, BookingStatus
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    total_treks = Trek.query.count()
    total_trekkers = Trekker.query.count()
    total_staff = StaffProfile.query.count()
    total_bookings = Booking.query.count()
    return jsonify({
        "total_trekkers": total_trekkers,
        "total_staff": total_staff,
        "total_treks": total_treks,
        "total_bookings": total_bookings
    })

@admin_bp.route('/Staff', methods=['GET'])
@jwt_required()
def get_users():
    users = StaffProfile.query.all()
    user_list = [{"id": user.id, "user_id": user.user_id, "contact_details": user.contact_details, "status": user.status.value} for user in users]
    return jsonify({"users": user_list})

@admin_bp.route('/trekkers', methods=['GET'])
@jwt_required()
def get_trekkers():
    trekkers = Trekker.query.all()
    trekker_list = [{"id": trekker.id, "user_id": trekker.user_id, "age": trekker.age} for trekker in trekkers]
    return jsonify({"trekkers": trekker_list})

@admin_bp.route('/treks', methods=['GET'])
@jwt_required()
def get_treks():
    treks = Trek.query.all()
    trek_list = [{"id": trek.id, "trek_name": trek.trek_name, "location": trek.location, "difficulty": trek.difficulty.value, "status": trek.status.value} for trek in treks]
    return jsonify({"treks": trek_list})

@admin_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    bookings = Booking.query.all()
    booking_list = [{"id": booking.id, "user_id": booking.user_id, "trek_id": booking.trek_id, "booking_date": booking.booking_date.isoformat(), "status": booking.status.value} for booking in bookings]
    return jsonify({"bookings": booking_list})

@admin_bp.route('/manage-trek/<int:trek_id>', methods=['PATCH'])
@jwt_required()
def manage_trek(trek_id):
    data = request.get_json()
    action = data.get('action')
    trek = Trek.query.get(trek_id)
    
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    
    if action == 'approve':
        trek.status = TrekStatus.APPROVED
    elif action == 'open':
        trek.status = TrekStatus.OPEN
    elif action == 'close':
        trek.status = TrekStatus.CLOSED
    elif action == 'complete':
        trek.status = TrekStatus.COMPLETED
    else:
        return jsonify({"error": "Invalid action"}), 400
    
    db.session.commit()
    return jsonify({"message": f"Trek {action}d successfully", "trek": {"id": trek.id, "status": trek.status.value}})

@admin_bp.route('/create-trek', methods=['POST'])
@jwt_required()
def create_trek():
    data = request.get_json()
    trek_name = data.get('trek_name')
    location = data.get('location')
    difficulty = data.get('difficulty')
    available_slots = data.get('available_slots')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    staff_name = data.get('staff_name')
    
    staff = User.query.filter_by(username=staff_name).first()
    if not staff:
        return jsonify({"error": "Staff member not found"}), 404

    new_trek = Trek(trek_name = trek_name, location = location, difficulty = difficulty, available_slots = available_slots, start_date = start_date, end_date = end_date, staff_id = staff.id)

    db.session.add(new_trek)
    db.session.commit()
    return jsonify({"message": "Trek created successfully", "trek": {"id": new_trek.id, "trek_name": new_trek.trek_name}}), 201

@admin_bp.route('/update-trek/<int:trek_id>', methods=['PUT'])
@jwt_required()
def update_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    
    data = request.get_json()
    trek.trek_name = data.get('trek_name', trek.trek_name)
    trek.location = data.get('location', trek.location)
    trek.difficulty = data.get('difficulty', trek.difficulty)
    trek.available_slots = data.get('available_slots', trek.available_slots)
    trek.start_date = data.get('start_date', trek.start_date)
    trek.end_date = data.get('end_date', trek.end_date)
    staff_name = data.get('staff_name')
    
    if staff_name:
        staff = User.query.filter_by(username=staff_name).first()
        if staff:
            trek.staff_id = staff.id

    db.session.commit()
    return jsonify({"message": "Trek updated successfully", "trek": {"id": trek.id, "trek_name": trek.trek_name}})

@admin_bp.route('/delete-trek/<int:trek_id>', methods=['DELETE'])
@jwt_required()
def delete_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    
    db.session.delete(trek)
    db.session.commit()
    return jsonify({"message": "Trek deleted successfully"})


@admin_bp.route('/manage-booking/<int:booking_id>', methods=['PATCH'])
@jwt_required()
def manage_booking(booking_id):
    data = request.get_json()
    action = data.get('action')
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    
    if action == 'cancel':
        booking.status = BookingStatus.CANCELLED
    elif action == 'complete':
        booking.status = BookingStatus.COMPLETED
    else:
        return jsonify({"error": "Invalid action"}), 400
    db.session.commit()
    return jsonify({"message": f"Booking {action}d successfully", "booking": {"id": booking.id, "status": booking.status}})

@admin_bp.route('/approve-staff', methods=['PATCH'])
@jwt_required()
def approve_staff():
    data = request.get_json()
    staff_id = data.get('staff_id')
    staff_profile = StaffProfile.query.get(staff_id)
    
    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404
    
    staff_profile.status = ProfileStatus.ACTIVE
    db.session.commit()
    return jsonify({"message": "Staff profile approved successfully", "staff_profile": {"id": staff_profile.id, "status": staff_profile.status}})

@admin_bp.route('/blacklist-staff', methods=['PATCH'])
@jwt_required()
def reject_staff():
    data = request.get_json()
    staff_id = data.get('staff_id')
    staff_profile = StaffProfile.query.get(staff_id)
    
    if not staff_profile:
        return jsonify({"error": "Staff profile not found"}), 404

    staff_profile.blacklisted = True
    db.session.commit()
    return jsonify({"message": "Staff profile blacklisted successfully", "staff_profile": {"id": staff_profile.id, "blacklisted": staff_profile.blacklisted}})

@admin_bp.route('/blacklist-trekker', methods=['PATCH'])
@jwt_required()
def blacklist_trekker():
    data = request.get_json()
    trekker_id = data.get('trekker_id')
    trekker = Trekker.query.get(trekker_id)
    
    if not trekker:
        return jsonify({"error": "Trekker not found"}), 404

    trekker.blacklisted = True
    db.session.commit()
    return jsonify({"message": "Trekker blacklisted successfully", "trekker": {"id": trekker.id, "blacklisted": trekker.blacklisted}})